import { useEffect, useState } from 'react';
import { RefreshCw, Search, ShieldCheck } from 'lucide-react';
import { roleService } from '../../services/roleService';
import { getApiError } from '../../api/axiosClient';
import { previewRoles } from '../../data/previewData';
import { buttonClass, fieldClass } from '../../constants/ui';
import PageTitle from '../../components/common/PageTitle';
import Notice from '../../components/common/Notice';
import { hasPreviewAccess } from '../../routes/ProtectedRoute';

export default function RolesPage() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');

  const loadRoles = async () => {
    setLoading(true);
    setError('');
    if (hasPreviewAccess()) {
      setRoles(previewRoles);
      setLoading(false);
      return;
    }
    try {
      const result = await roleService.obtenerRoles();
      setRoles(Array.isArray(result) ? result : []);
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadRoles(); }, []);
  const visibleRoles = roles.filter(role => `${role.rolNombre} ${role.rolDescripcion || ''}`.toLowerCase().includes(search.toLowerCase()));

  return (
    <>
      <PageTitle eyebrow="Administración" title="Roles del sistema">
        <button className={buttonClass} onClick={loadRoles}><RefreshCw size={16} />Actualizar</button>
      </PageTitle>
      <Notice error={error} />
      <p className="mb-5 max-w-2xl text-sm leading-6 text-slate-400">Consulta los perfiles que se pueden asignar a cada usuario. La API disponible ofrece el catálogo de roles en modo lectura.</p>
      <div className="mb-4 max-w-sm">
        <div className="relative"><Search className="absolute left-3 top-3 h-4 w-4 text-slate-500" /><input className={`${fieldClass} pl-9`} placeholder="Buscar rol" value={search} onChange={event => setSearch(event.target.value)} /></div>
      </div>
      {loading ? <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-sm text-slate-400">Cargando roles…</div>
        : visibleRoles.length === 0 ? <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-sm text-slate-400">No hay roles que coincidan con la búsqueda.</div>
          : <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{visibleRoles.map(role => (
            <article key={role.rolId} className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <div className="mb-4 flex items-start justify-between gap-3"><div className="rounded-xl bg-emerald-500/10 p-2.5 text-emerald-300"><ShieldCheck size={20} /></div><span className={`rounded-full px-2.5 py-1 text-xs font-medium ${role.rolEstado ? 'bg-emerald-500/10 text-emerald-300' : 'bg-slate-700 text-slate-300'}`}>{role.rolEstado ? 'Activo' : 'Inactivo'}</span></div>
              <h2 className="font-semibold text-white">{role.rolNombre}</h2>
              <p className="mt-2 min-h-10 text-sm leading-5 text-slate-400">{role.rolDescripcion || 'Sin descripción registrada.'}</p>
              <div className="mt-4 border-t border-slate-800 pt-3 text-xs text-slate-500">ID: <span className="font-mono">{role.rolId}</span></div>
            </article>
          ))}</div>}
    </>
  );
}
