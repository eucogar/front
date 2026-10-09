import { useEffect, useState } from 'react';
import { BarChart3, Bike, ClipboardList, ShieldCheck, Users } from 'lucide-react';
import PageTitle from '../../components/common/PageTitle';
import SummaryCard from '../../components/dashboard/SummaryCard';
import Notice from '../../components/common/Notice';
import { accessService } from '../../services/accessService';
import { roleService } from '../../services/roleService';
import { userService } from '../../services/userService';
import { getApiError } from '../../api/axiosClient';
import { previewAccesses, previewRoles, previewUsers } from '../../data/previewData';
import { formatDate } from '../../utils/formatDate';
import { hasPreviewAccess } from '../../routes/ProtectedRoute';

const emptySummary = { users: 0, roles: 0, accesses: 0, inside: 0, recent: [] };

export default function OverviewPage() {
  const [summary, setSummary] = useState(emptySummary);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadSummary = async () => {
    setLoading(true);
    setError('');
    if (hasPreviewAccess()) {
      setSummary({
        users: previewUsers.length,
        roles: previewRoles.length,
        accesses: previewAccesses.length,
        inside: previewAccesses.filter(row => row.estadoAcceso === 'ENTRADA').length,
        recent: previewAccesses.slice(0, 5),
      });
      setLoading(false);
      return;
    }

    try {
      const [users, roles, accesses] = await Promise.all([
        userService.listarUsuarios(),
        roleService.obtenerRoles(),
        accessService.consultarFiltros({ fechaEntrada: null, fechaSalida: null, placa: null, identificacion: null, estado: null }),
      ]);
      const rows = Array.isArray(accesses) ? accesses : [];
      setSummary({
        users: Array.isArray(users) ? users.length : 0,
        roles: Array.isArray(roles) ? roles.length : 0,
        accesses: rows.length,
        inside: rows.filter(row => row.estadoAcceso === 'ENTRADA' || !row.fechaHoraSalida).length,
        recent: rows.slice(0, 5),
      });
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadSummary(); }, []);

  return (
    <>
      <PageTitle eyebrow="Panel de control" title="Resumen" />
      <Notice error={error} />
      <section aria-label="Resumen de datos" className="mb-7 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[
          ['Personas registradas', summary.users],
          ['Roles disponibles', summary.roles],
          ['Movimientos registrados', summary.accesses],
          ['Personas dentro', summary.inside],
        ].map(([label, value]) => (
          <article key={label} className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">{label}</p>
            <p className="mt-3 text-3xl font-bold text-white">{loading ? '—' : value}</p>
          </article>
        ))}
      </section>

      <div className="mb-7 grid gap-4 sm:grid-cols-2">
        <SummaryCard icon={Users} title="Gestión de usuarios" text="Consulta y administra las personas autorizadas." to="/dashboard/usuarios" />
        <SummaryCard icon={BarChart3} title="Analítica del parqueadero de motos" text="Consulta ingresos por hora y día, y la cantidad de motos dentro, por hora y por día." to="/dashboard/analitica" />
        <SummaryCard icon={ShieldCheck} title="Roles del sistema" text="Consulta los perfiles disponibles." to="/dashboard/roles" />
        <SummaryCard icon={ClipboardList} title="Historial de accesos" text="Filtra movimientos por fecha, placa, identificación o estado." to="/dashboard/accesos" />
        <SummaryCard icon={Bike} title="Registrar movimiento" text="Registra la entrada o salida de una motocicleta." to="/dashboard/registrar" />
      </div>

      <section className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
        <div className="flex items-center justify-between gap-3 border-b border-slate-800 px-5 py-4">
          <div><h2 className="font-semibold text-white">Movimientos recientes</h2><p className="mt-1 text-xs text-slate-400">Información cargada desde el backend.</p></div>
          <button className="rounded-lg border border-slate-700 px-3 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800" onClick={loadSummary} disabled={loading}>Actualizar</button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[650px] text-left text-sm">
            <thead className="bg-slate-950/60 text-xs uppercase text-slate-400"><tr>{['Identificación', 'Persona', 'Placa', 'Entrada', 'Estado'].map(label => <th key={label} className="px-5 py-3">{label}</th>)}</tr></thead>
            <tbody>
              {loading ? <tr><td colSpan="5" className="p-6 text-center text-slate-400">Cargando datos…</td></tr>
                : summary.recent.map((row, index) => <tr key={`${row.identificacion}-${row.fechaHoraEntrada}-${index}`} className="border-t border-slate-800"><td className="px-5 py-3">{row.identificacion}</td><td className="px-5 py-3">{row.nombreCompleto}</td><td className="px-5 py-3">{row.placa}</td><td className="px-5 py-3">{formatDate(row.fechaHoraEntrada)}</td><td className="px-5 py-3"><span className="rounded-full bg-emerald-500/10 px-2.5 py-1 text-xs text-emerald-300">{row.estadoAcceso}</span></td></tr>)}
              {!loading && summary.recent.length === 0 && <tr><td colSpan="5" className="p-6 text-center text-slate-500">Todavía no hay movimientos registrados.</td></tr>}
            </tbody>
          </table>
        </div>
        <p className="border-t border-slate-800 px-5 py-3 text-xs text-slate-500">El sistema alterna entre entrada y salida según el último registro abierto de cada persona.</p>
      </section>
    </>
  );
}
