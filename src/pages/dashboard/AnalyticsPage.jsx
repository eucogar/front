import { useEffect, useMemo, useState } from 'react';
import { BarChart3, Bike, Clock3, RefreshCw, TrendingUp } from 'lucide-react';
import PageTitle from '../../components/common/PageTitle';
import Notice from '../../components/common/Notice';
import { accessService } from '../../services/accessService';
import { getApiError } from '../../api/axiosClient';
import { previewAccesses } from '../../data/previewData';
import { hasPreviewAccess } from '../../routes/ProtectedRoute';

const isoDate = (date) => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
const today = new Date();
const monthAgo = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 29);
const blankMetrics = { totalEntradas: 0, ocupacionActual: 0, maximaOcupacion: 0, fechaHoraMaximaOcupacion: null, horaPico: null, diaPico: '', entradasPorHora: Array.from({ length: 24 }, (_, indice) => ({ indice, etiqueta: `${String(indice).padStart(2, '0')}:00`, cantidad: 0 })), entradasPorDia: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'].map((etiqueta, indice) => ({ etiqueta, indice, cantidad: 0 })) };

function summarizePreview(start, end) {
  const from = new Date(`${start}T00:00:00`);
  const until = new Date(`${end}T23:59:59.999`);
  const rows = previewAccesses.map(row => ({ ...row, plate: row.placa.trim().toUpperCase(), entry: new Date(row.fechaHoraEntrada), exit: row.fechaHoraSalida ? new Date(row.fechaHoraSalida) : null }));
  const entries = rows.filter(row => row.entry >= from && row.entry <= until);
  const hours = blankMetrics.entradasPorHora.map(x => ({ ...x }));
  const days = blankMetrics.entradasPorDia.map(x => ({ ...x }));
  entries.forEach(row => { hours[row.entry.getHours()].cantidad += 1; days[(row.entry.getDay() + 6) % 7].cantidad += 1; });
  const events = [];
  rows.filter(row => row.entry < until && (!row.exit || row.exit > from)).forEach(row => {
    const startAt = row.entry < from ? from : row.entry;
    const endAt = row.exit && row.exit < until ? row.exit : until;
    if (endAt > startAt) events.push({ at: startAt, plate: row.plate, change: 1 }, { at: endAt, plate: row.plate, change: -1 });
  });
  const counts = new Map(); let active = 0; let max = 0; let peak = null;
  events.sort((a, b) => a.at - b.at).forEach(event => {
    const next = (counts.get(event.plate) || 0) + event.change;
    if (next <= 0) { if (counts.has(event.plate)) active -= 1; counts.delete(event.plate); }
    else { if (!counts.has(event.plate)) active += 1; counts.set(event.plate, next); }
    if (active > max) { max = active; peak = event.at; }
  });
  return { ...blankMetrics, totalEntradas: entries.length, ocupacionActual: new Set(rows.filter(row => !row.exit).map(row => row.plate)).size, maximaOcupacion: max, fechaHoraMaximaOcupacion: peak, horaPico: entries.length ? hours.reduce((best, x) => x.cantidad > best.cantidad ? x : best, hours[0]).indice : null, diaPico: entries.length ? days.reduce((best, x) => x.cantidad > best.cantidad ? x : best, days[0]).etiqueta : '', entradasPorHora: hours, entradasPorDia: days };
}

function MetricCard({ icon: Icon, label, value, detail }) {
  return <article className="rounded-2xl border border-slate-800 bg-slate-900 p-5"><div className="flex items-center justify-between"><p className="text-sm text-slate-400">{label}</p><Icon size={19} className="text-emerald-400" /></div><p className="mt-3 text-3xl font-bold text-white">{value}</p><p className="mt-1 text-xs text-slate-500">{detail}</p></article>;
}

function Bars({ title, subtitle, data, highlightIndex, formatLabel }) {
  const maximum = Math.max(1, ...data.map(row => row.cantidad));
  return <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
    <div className="mb-5"><h2 className="font-semibold text-white">{title}</h2><p className="mt-1 text-xs text-slate-400">{subtitle}</p></div>
    <div className="flex h-52 items-end gap-1 border-b border-slate-700 pb-2 sm:gap-2">{data.map(row => <div key={row.indice} title={`${row.etiqueta}: ${row.cantidad}`} className="flex h-full min-w-0 flex-1 flex-col items-center justify-end gap-2"><span className="text-[10px] text-slate-400">{row.cantidad || ''}</span><div className={`w-full max-w-8 rounded-t ${row.indice === highlightIndex ? 'bg-emerald-400' : 'bg-sky-500/70'}`} style={{ height: `${row.cantidad ? Math.max(5, row.cantidad / maximum * 76) : 0}%` }} /><span className="truncate text-[9px] text-slate-500 sm:text-[10px]">{formatLabel(row)}</span></div>)}</div>
  </section>;
}

export default function AnalyticsPage() {
  const [fechaInicio, setFechaInicio] = useState(isoDate(monthAgo));
  const [fechaFin, setFechaFin] = useState(isoDate(today));
  const [metrics, setMetrics] = useState(blankMetrics);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loaded, setLoaded] = useState(false);

  const loadMetrics = async (event) => {
    event?.preventDefault(); setError('');
    if (!fechaInicio || !fechaFin || fechaInicio > fechaFin) { setError('Selecciona un rango de fechas válido.'); return; }
    setLoading(true);
    try {
      const result = hasPreviewAccess() ? summarizePreview(fechaInicio, fechaFin) : await accessService.consultarAnalitica(fechaInicio, fechaFin);
      setMetrics({ ...blankMetrics, ...result }); setLoaded(true);
    } catch (requestError) { setError(getApiError(requestError)); }
    finally { setLoading(false); }
  };
  useEffect(() => { loadMetrics(); }, []);

  const hourLabel = useMemo(() => metrics.horaPico == null ? '—' : `${String(metrics.horaPico).padStart(2, '0')}:00`, [metrics.horaPico]);
  const peakMoment = metrics.fechaHoraMaximaOcupacion ? new Date(metrics.fechaHoraMaximaOcupacion).toLocaleString('es-CO', { dateStyle: 'medium', timeStyle: 'short' }) : 'Sin ocupación en el rango';
  return <>
    <PageTitle eyebrow="Indicadores del parqueadero de motos" title="Analítica de ocupación" />
    <p className="mb-5 max-w-3xl text-sm leading-6 text-slate-400">Consulta las horas y días con más ingresos y la máxima cantidad de motos que coincidieron dentro del parqueadero.</p>
    <Notice error={error} />
    <form onSubmit={loadMetrics} className="mb-6 flex flex-wrap items-end gap-3 rounded-2xl border border-slate-800 bg-slate-900 p-4">
      <label className="text-xs text-slate-400">Desde<input type="date" className="mt-1 block rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100" value={fechaInicio} max={fechaFin || undefined} onChange={e => setFechaInicio(e.target.value)} /></label>
      <label className="text-xs text-slate-400">Hasta<input type="date" className="mt-1 block rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100" value={fechaFin} min={fechaInicio || undefined} onChange={e => setFechaFin(e.target.value)} /></label>
      <button className="flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-emerald-500 disabled:opacity-60" disabled={loading}><RefreshCw size={16} className={loading ? 'animate-spin' : ''} />{loading ? 'Consultando…' : 'Consultar'}</button>
    </form>
    <section aria-label="Indicadores principales" className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <MetricCard icon={TrendingUp} label="Entradas en el periodo" value={loaded ? metrics.totalEntradas : '—'} detail="Cada movimiento de entrada registrado" />
      <MetricCard icon={Bike} label="Motos dentro ahora" value={loaded ? metrics.ocupacionActual : '—'} detail="Motos con placa única y sin salida registrada" />
      <MetricCard icon={Bike} label="Máxima ocupación de motos" value={loaded ? metrics.maximaOcupacion : '—'} detail={peakMoment} />
      <MetricCard icon={Clock3} label="Pico de ingresos" value={loaded ? hourLabel : '—'} detail={loaded ? (metrics.diaPico ? `Día con más entradas: ${metrics.diaPico}` : 'Sin ingresos en el rango') : 'Hora y día con mayor flujo'} />
    </section>
    <div className="grid gap-5 xl:grid-cols-2">
      <Bars title="Entradas por hora" subtitle="Hora local registrada en el sistema" data={metrics.entradasPorHora} highlightIndex={metrics.horaPico} formatLabel={row => row.indice % 3 === 0 ? row.etiqueta : ''} />
      <Bars title="Entradas por día de la semana" subtitle="Día de la semana de cada entrada" data={metrics.entradasPorDia} highlightIndex={metrics.entradasPorDia.find(x => x.etiqueta === metrics.diaPico)?.indice} formatLabel={row => row.etiqueta.slice(0, 3)} />
    </div>
    <p className="mt-4 text-xs leading-5 text-slate-500">La ocupación simultánea cuenta placas únicas de motos entre la hora de entrada y la hora de salida. Los movimientos sin salida registrada cuentan como motos dentro.</p>
  </>;
}
