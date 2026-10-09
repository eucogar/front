import { useState } from 'react';
import { BarChart3, Bike, ClipboardList, LayoutDashboard, LogOut, Plus, ShieldCheck, Users } from 'lucide-react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { hasPreviewAccess } from '../routes/ProtectedRoute';

const navigation = [
  { to: '/dashboard', label: 'Resumen', icon: LayoutDashboard, end: true },
  { to: '/dashboard/analitica', label: 'Analítica', icon: BarChart3 },
  { to: '/dashboard/usuarios', label: 'Usuarios', icon: Users },
  { to: '/dashboard/roles', label: 'Roles', icon: ShieldCheck },
  { to: '/dashboard/accesos', label: 'Registros de acceso', icon: ClipboardList },
  { to: '/dashboard/registrar', label: 'Registrar entrada / salida', icon: Plus },
];

export default function DashboardLayout() {
  const navigate = useNavigate();
  const [sessionUser] = useState(() => {
    if (hasPreviewAccess()) return { nombreCompleto: 'Vista previa', rol: 'Modo diseño' };
    try { return JSON.parse(localStorage.getItem('user') || '{}'); } catch { return {}; }
  });

  const exit = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('previewMode');
    navigate('/login', { replace: true });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 md:flex">
      <aside className="border-b border-slate-800 bg-slate-900 p-5 md:min-h-screen md:w-64 md:border-b-0 md:border-r">
        <div className="mb-7 flex items-center gap-3">
          <div className="rounded-xl bg-emerald-600 p-2"><Bike /></div>
          <div><div className="font-bold">Acceso UPC</div><div className="text-xs text-slate-400">Parqueadero de motos</div></div>
        </div>
        <nav className="flex gap-2 overflow-x-auto md:flex-col">
          {navigation.map(({ to, label, icon: Icon, end }) => (
            <NavLink key={to} to={to} end={end} className={({ isActive }) => `flex shrink-0 items-center gap-3 rounded-xl px-3 py-2.5 text-sm ${isActive ? 'bg-emerald-500/15 text-emerald-300' : 'text-slate-300 hover:bg-slate-800'}`}>
              <Icon size={18} />{label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-7 flex items-center justify-between border-t border-slate-800 pt-4">
          <div className="min-w-0"><div className="truncate text-sm font-medium">{sessionUser.nombreCompleto || 'Usuario'}</div><div className="text-xs text-slate-400">{sessionUser.rol || 'Sesión activa'}</div></div>
          <button onClick={exit} title="Cerrar sesión" className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white"><LogOut size={18} /></button>
        </div>
      </aside>

      <main className="min-w-0 flex-1 p-5 md:p-9">
        {hasPreviewAccess() && <div className="mb-6 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-amber-400/30 bg-amber-400/10 px-4 py-3 text-sm text-amber-100"><span><strong>Modo vista previa.</strong> Datos de demostración; no se consulta ni modifica el backend.</span><button onClick={exit} className="rounded-lg border border-amber-200/30 px-3 py-1.5 text-xs font-semibold hover:bg-amber-300/10">Salir de la vista previa</button></div>}
        <Outlet />
      </main>
    </div>
  );
}
