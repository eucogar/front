import { useEffect, useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight, Search } from 'lucide-react';
import { accessService } from '../../services/accessService';
import { getApiError } from '../../api/axiosClient';
import { previewAccesses } from '../../data/previewData';
import { buttonClass, fieldClass } from '../../constants/ui';
import PageTitle from '../../components/common/PageTitle';
import Notice from '../../components/common/Notice';
import { formatDate } from '../../utils/formatDate';
import { hasPreviewAccess } from '../../routes/ProtectedRoute';

const emptyFilters = { fechaEntrada: '', fechaSalida: '', placa: '', identificacion: '', estado: '' };

export default function AccessHistoryPage() {
  const [filters, setFilters] = useState(emptyFilters);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);

  const search = async (event) => {
    event?.preventDefault();
    setPage(1);
    setLoading(true);
    setError('');
    if (hasPreviewAccess()) {
      const matches = previewAccesses.filter(row => (!filters.placa || row.placa.toLowerCase().includes(filters.placa.toLowerCase())) && (!filters.identificacion || row.identificacion.includes(filters.identificacion)) && (!filters.estado || row.estadoAcceso === filters.estado) && (!filters.fechaEntrada || row.fechaHoraEntrada.slice(0, 10) === filters.fechaEntrada) && (!filters.fechaSalida || (row.fechaHoraSalida && row.fechaHoraSalida.slice(0, 10) === filters.fechaSalida)));
      setRows(matches);
      setLoading(false);
      return;
    }
    try {
      setRows(await accessService.consultarFiltros({ ...filters, fechaEntrada: filters.fechaEntrada || null, fechaSalida: filters.fechaSalida || null, placa: filters.placa || null, identificacion: filters.identificacion || null, estado: filters.estado || null }));
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { search(); }, []);
  const updateFilter = (key, value) => setFilters(current => ({ ...current, [key]: value }));
  const pageCount = Math.max(1, Math.ceil(rows.length / pageSize));
  const visibleRows = useMemo(() => rows.slice((page - 1) * pageSize, page * pageSize), [rows, page, pageSize]);
  const firstRow = rows.length === 0 ? 0 : (page - 1) * pageSize + 1;
  const lastRow = Math.min(page * pageSize, rows.length);
  const pageNumbers = pageCount <= 7
    ? Array.from({ length: pageCount }, (_, index) => index + 1)
    : [...new Set([1, page - 1, page, page + 1, pageCount].filter(number => number >= 1 && number <= pageCount))];

  return (
    <>
      <PageTitle eyebrow="Parqueadero de motos" title="Registros de acceso" />
      <Notice error={error} />
      <form onSubmit={search} className="mb-5 grid gap-3 rounded-2xl border border-slate-800 bg-slate-900 p-4 sm:grid-cols-2 lg:grid-cols-3">
        {[["fechaEntrada", "Fecha de entrada", "date"], ["fechaSalida", "Fecha de salida", "date"], ["placa", "Placa", "text"], ["identificacion", "Identificación", "text"]].map(([key, label, type]) => <label key={key} className="text-xs text-slate-400">{label}<input type={type} className={`${fieldClass} mt-1`} value={filters[key]} onChange={event => updateFilter(key, event.target.value)} /></label>)}
        <label className="text-xs text-slate-400">Estado<select className={`${fieldClass} mt-1`} value={filters.estado} onChange={event => updateFilter('estado', event.target.value)}><option value="">Todos</option><option value="ENTRADA">Entrada</option><option value="SALIDA">Salida</option></select></label>
        <div className="flex items-end"><button className={buttonClass} disabled={loading}><Search size={16} />{loading ? 'Consultando…' : 'Aplicar filtros'}</button></div>
      </form>
      <section className="overflow-hidden rounded-2xl border border-slate-800">
        <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900 px-4 py-3">
          <p className="text-sm text-slate-400">{rows.length ? `Mostrando ${firstRow}–${lastRow} de ${rows.length} registros` : '0 registros'}</p>
          <label className="flex items-center gap-2 text-xs text-slate-400">Filas por página<select className="rounded-lg border border-slate-700 bg-slate-950 px-2 py-1.5 text-sm text-slate-200" value={pageSize} onChange={event => { setPageSize(Number(event.target.value)); setPage(1); }}><option value={10}>10</option><option value={25}>25</option><option value={50}>50</option><option value={100}>100</option></select></label>
        </div>
        <div className="overflow-x-auto"><table className="w-full min-w-[800px] text-left text-sm"><thead className="bg-slate-950/60 text-xs uppercase text-slate-400"><tr>{['Identificación', 'Nombre', 'Placa', 'Entrada', 'Salida', 'Estado'].map(label => <th key={label} className="px-4 py-3">{label}</th>)}</tr></thead><tbody>
        {loading && <tr><td colSpan="6" className="p-6 text-center text-slate-400">Cargando registros…</td></tr>}
        {!loading && visibleRows.map((row, index) => <tr key={`${row.identificacion}-${row.fechaHoraEntrada}-${(page - 1) * pageSize + index}`} className="border-t border-slate-800"><td className="px-4 py-3">{row.identificacion}</td><td className="px-4 py-3">{row.nombreCompleto}</td><td className="px-4 py-3">{row.placa}</td><td className="px-4 py-3">{formatDate(row.fechaHoraEntrada)}</td><td className="px-4 py-3">{formatDate(row.fechaHoraSalida)}</td><td className="px-4 py-3"><span className="rounded-full bg-emerald-500/10 px-2.5 py-1 text-xs text-emerald-300">{row.estadoAcceso}</span></td></tr>)}
        {!loading && rows.length === 0 && <tr><td colSpan="6" className="p-6 text-center text-slate-500">Sin registros coincidentes.</td></tr>}
        </tbody></table></div>
        {rows.length > 0 && <nav aria-label="Paginación de registros" className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-800 bg-slate-900 px-4 py-3">
          <p className="text-xs text-slate-500">Página {page} de {pageCount}</p>
          <div className="flex items-center gap-1">
            <button type="button" aria-label="Primera página" title="Primera página" disabled={page === 1 || loading} onClick={() => setPage(1)} className="rounded-lg border border-slate-700 p-2 text-slate-300 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"><ChevronsLeft size={16} /></button>
            <button type="button" aria-label="Página anterior" title="Página anterior" disabled={page === 1 || loading} onClick={() => setPage(value => Math.max(1, value - 1))} className="rounded-lg border border-slate-700 p-2 text-slate-300 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"><ChevronLeft size={16} /></button>
            {pageNumbers.map((number, index) => <span key={number} className="flex items-center gap-1">{index > 0 && number - pageNumbers[index - 1] > 1 && <span className="px-1 text-slate-500">…</span>}<button type="button" aria-current={page === number ? 'page' : undefined} disabled={loading} onClick={() => setPage(number)} className={`min-w-9 rounded-lg px-2.5 py-2 text-sm ${page === number ? 'bg-emerald-600 font-semibold text-white' : 'text-slate-300 hover:bg-slate-800'}`}>{number}</button></span>)}
            <button type="button" aria-label="Página siguiente" title="Página siguiente" disabled={page === pageCount || loading} onClick={() => setPage(value => Math.min(pageCount, value + 1))} className="rounded-lg border border-slate-700 p-2 text-slate-300 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"><ChevronRight size={16} /></button>
            <button type="button" aria-label="Última página" title="Última página" disabled={page === pageCount || loading} onClick={() => setPage(pageCount)} className="rounded-lg border border-slate-700 p-2 text-slate-300 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"><ChevronsRight size={16} /></button>
          </div>
        </nav>}
      </section>
    </>
  );
}
