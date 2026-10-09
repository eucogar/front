import { useEffect, useMemo, useState } from 'react';
import { Plus, RefreshCw, Search } from 'lucide-react';
import { userService } from '../../services/userService';
import { roleService } from '../../services/roleService';
import { getApiError } from '../../api/axiosClient';
import { previewRoles, previewUsers } from '../../data/previewData';
import { buttonClass, fieldClass } from '../../constants/ui';
import PageTitle from '../../components/common/PageTitle';
import Notice from '../../components/common/Notice';
import { hasPreviewAccess } from '../../routes/ProtectedRoute';

const emptyForm = { identificacion: '', nombres: '', apellidos: '', correo: '', telefono: '', password: '', rol: '' };

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [search, setSearch] = useState('');
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const isStudentRole = roles.find(role => String(role.rolId) === String(form.rol))?.rolNombre?.trim().toLowerCase() === 'estudiante';

  const loadUsers = async () => {
    setLoading(true);
    setError('');
    if (hasPreviewAccess()) {
      setUsers(previewUsers);
      setRoles(previewRoles);
      setLoading(false);
      return;
    }
    try {
      const [userResult, roleResult] = await Promise.all([userService.listarUsuarios(), roleService.obtenerRoles()]);
      setUsers(Array.isArray(userResult) ? userResult : []);
      setRoles(Array.isArray(roleResult) ? roleResult : []);
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadUsers(); }, []);
  const filteredUsers = useMemo(() => users.filter(user => `${user.identificacion} ${user.nombres} ${user.apellidos} ${user.correo || ''}`.toLowerCase().includes(search.toLowerCase())), [users, search]);

  const editUser = async (user) => {
    setError('');
    if (!user.correo) {
      setError('Esta persona no tiene una cuenta del aplicativo. El backend actual no permite editarla desde este formulario.');
      return;
    }
    if (hasPreviewAccess()) {
      setEditing(true);
      setForm({ ...emptyForm, ...user, correo: user.correo || '', rol: user.rolId, password: '' });
      return;
    }
    try {
      const fullUser = await userService.obtenerPorIdentificacion(user.identificacion);
      setEditing(true);
      setForm({ ...emptyForm, ...(fullUser || user), correo: (fullUser || user).correo || '', rol: (fullUser || user).rolId || '', password: '' });
    } catch (requestError) {
      setError(getApiError(requestError));
    }
  };

  const saveUser = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');
    const isStudent = roles.find(role => String(role.rolId) === String(form.rol))?.rolNombre?.trim().toLowerCase() === 'estudiante';
    const payload = { identificacion: form.identificacion.trim(), nombres: form.nombres.trim(), apellidos: form.apellidos.trim(), correo: isStudent ? null : form.correo.trim(), telefono: form.telefono.trim(), rol: String(form.rol) };

    if (hasPreviewAccess()) {
      const selectedRole = roles.find(role => role.rolId === form.rol);
      const nextUser = { ...form, rolId: form.rol, rolNombre: selectedRole?.rolNombre || 'Estudiante', estado: true };
      setUsers(current => editing ? current.map(user => user.identificacion === form.identificacion ? { ...user, ...nextUser } : user) : [nextUser, ...current]);
      setSuccess(editing ? 'Cambios simulados en la vista previa.' : 'Usuario de demostración agregado.');
      setEditing(null);
      setForm(emptyForm);
      return;
    }

    try {
      if (editing) await userService.actualizarUsuario(payload);
      else await userService.crearUsuario({ ...payload, password: isStudent ? null : form.password });
      setSuccess(editing ? 'Usuario actualizado.' : 'Usuario creado.');
      setEditing(null);
      setForm(emptyForm);
      await loadUsers();
    } catch (requestError) {
      setError(getApiError(requestError));
    }
  };

  return (
    <>
      <PageTitle eyebrow="Administración" title="Usuarios"><button className={buttonClass} onClick={() => { setEditing(false); setForm(emptyForm); setError(''); }}><Plus size={17} />Nuevo usuario</button></PageTitle>
      <p className="mb-4 text-sm text-slate-400">Los estudiantes quedan autorizados para el control de acceso sin cuenta del aplicativo. Solo los roles que inician sesion requieren correo y contrasena.</p>
      <Notice error={error} success={success} />
      {editing !== null && <form onSubmit={saveUser} className="mb-6 grid gap-3 rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:grid-cols-2 lg:grid-cols-3">
        <h2 className="sm:col-span-2 lg:col-span-3 font-semibold">{editing ? 'Editar usuario' : 'Crear usuario'}</h2>
        {[["identificacion", "Identificacion"], ["nombres", "Nombres"], ["apellidos", "Apellidos"], ...(!isStudentRole ? [["correo", "Correo"]] : []), ["telefono", "Telefono"]].map(([key, label]) => <label key={key} className="text-xs text-slate-400">{label}<input type={key === 'correo' ? 'email' : 'text'} className={`${fieldClass} mt-1`} required={key !== 'telefono'} value={form[key] || ''} onChange={event => setForm({ ...form, [key]: event.target.value })} /></label>)}
        {!editing && !isStudentRole && <label className="text-xs text-slate-400">Contrasena<input type="password" minLength={8} className={`${fieldClass} mt-1`} required value={form.password} onChange={event => setForm({ ...form, password: event.target.value })} /></label>}
        <label className="text-xs text-slate-400">Rol<select className={`${fieldClass} mt-1`} required disabled={Boolean(editing)} value={form.rol} onChange={event => { const rol = event.target.value; const student = roles.find(item => String(item.rolId) === String(rol))?.rolNombre?.trim().toLowerCase() === 'estudiante'; setForm(current => ({ ...current, rol, ...(student ? { correo: '', password: '' } : {}) })); }}><option value="">Selecciona un rol</option>{roles.filter(role => role.rolEstado).map(role => <option key={role.rolId} value={role.rolId}>{role.rolNombre}</option>)}</select></label>
        <div className="flex items-end gap-2"><button className={buttonClass}>Guardar</button><button type="button" className="rounded-xl border border-slate-700 px-4 py-2.5 text-sm" onClick={() => setEditing(null)}>Cancelar</button></div>
      </form>}
      <div className="mb-4 flex gap-2"><div className="relative max-w-sm flex-1"><Search className="absolute left-3 top-3 h-4 w-4 text-slate-500" /><input className={`${fieldClass} pl-9`} placeholder="Buscar usuario" value={search} onChange={event => setSearch(event.target.value)} /></div><button className="rounded-xl border border-slate-700 px-3 text-slate-300" onClick={loadUsers} title="Actualizar"><RefreshCw size={17} /></button></div>
      <div className="overflow-x-auto rounded-2xl border border-slate-800"><table className="w-full min-w-[700px] text-left text-sm"><thead className="bg-slate-900 text-xs uppercase text-slate-400"><tr>{['Identificación', 'Nombre', 'Correo', 'Teléfono', 'Estado', ''].map(label => <th key={label} className="px-4 py-3">{label}</th>)}</tr></thead><tbody>
        {loading ? <tr><td colSpan="6" className="p-6 text-center text-slate-400">Cargando usuarios…</td></tr> : filteredUsers.map(user => <tr key={user.identificacion} className="border-t border-slate-800"><td className="px-4 py-3">{user.identificacion}</td><td className="px-4 py-3">{user.nombres} {user.apellidos}</td><td className="px-4 py-3">{user.correo || 'Sin cuenta del aplicativo'}</td><td className="px-4 py-3">{user.telefono || '—'}</td><td className="px-4 py-3">{user.estado ? 'Activo' : 'Inactivo'}</td><td className="px-4 py-3"><button disabled={!user.correo} title={!user.correo ? 'Persona autorizada sin cuenta del aplicativo' : 'Editar usuario'} onClick={() => editUser(user)} className="text-emerald-400 hover:underline disabled:cursor-not-allowed disabled:text-slate-600 disabled:no-underline">Editar</button></td></tr>)}
        {!loading && filteredUsers.length === 0 && <tr><td colSpan="6" className="p-6 text-center text-slate-500">No hay usuarios para mostrar.</td></tr>}
      </tbody></table></div>
    </>
  );
}
