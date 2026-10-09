import React, { useState } from 'react';
import { AlertCircle, Bike, Loader2, Lock, User } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';
import { getApiError } from '../../api/axiosClient';

export function LoginPage() {
  const [usuario, setUsuario] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await authService.login({ usuario: usuario.trim(), password });
      const payload = response?.data;
      if (response?.code !== 200 || !payload?.token) {
        throw new Error(response?.message || 'El servidor no devolvió una sesión válida.');
      }
      localStorage.removeItem('previewMode');
      localStorage.setItem('token', payload.token);
      localStorage.setItem('user', JSON.stringify({ nombreCompleto: payload.nombreCompleto, rol: payload.rol }));
      navigate('/dashboard', { replace: true });
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.setItem('previewMode', 'true');
    navigate('/dashboard', { replace: true });
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-950 via-gray-950 to-green-950 px-4 relative overflow-hidden">
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-emerald-600/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-green-700/20 rounded-full blur-3xl pointer-events-none" />
      <section className="max-w-md w-full bg-gray-900/90 backdrop-blur-2xl border border-emerald-500/30 rounded-3xl shadow-2xl p-8 relative z-10">
        <header className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-emerald-600 to-green-700 text-white mb-4 shadow-lg"><Bike className="w-10 h-10" /></div>
          <h1 className="text-2xl font-black text-white">Acceso Motocicletas <span className="text-emerald-400">UPC</span></h1>
          <p className="text-xs text-emerald-300/80 mt-2 tracking-wide uppercase">Universidad Popular del Cesar · Sistema Inteligente</p>
        </header>
        {error && <div role="alert" className="mb-6 p-4 rounded-2xl bg-red-500/10 border border-red-500/20 flex items-center gap-3 text-red-300 text-sm"><AlertCircle className="w-5 h-5 shrink-0" />{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-5">
          <label className="block text-xs font-semibold text-emerald-300 uppercase tracking-wider">Usuario
            <span className="relative mt-2 block"><User className="absolute left-3.5 top-3.5 w-5 h-5 text-emerald-500/70" /><input autoComplete="username" value={usuario} onChange={(e) => setUsuario(e.target.value)} className="w-full pl-11 pr-4 py-3.5 bg-gray-950/70 border border-emerald-500/30 rounded-2xl text-white focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm" required /></span>
          </label>
          <label className="block text-xs font-semibold text-emerald-300 uppercase tracking-wider">Contraseña
            <span className="relative mt-2 block"><Lock className="absolute left-3.5 top-3.5 w-5 h-5 text-emerald-500/70" /><input type="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full pl-11 pr-4 py-3.5 bg-gray-950/70 border border-emerald-500/30 rounded-2xl text-white focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm" required /></span>
          </label>
          <button disabled={loading} className="w-full py-4 bg-gradient-to-r from-emerald-600 to-green-600 text-white font-bold rounded-2xl flex items-center justify-center gap-2 disabled:opacity-60">{loading ? <><Loader2 className="w-5 h-5 animate-spin" />Validando...</> : 'Ingresar al sistema'}</button>
        </form>
        <button type="button" onClick={handlePreview} className="mt-3 w-full rounded-2xl border border-emerald-500/30 px-4 py-3 text-sm font-semibold text-emerald-200 transition hover:bg-emerald-500/10">Ver diseño sin iniciar sesión</button>
        <p className="mt-2 text-center text-xs text-gray-500">Modo de demostración con datos de ejemplo; no crea una sesión ni llama al backend.</p>
        <p className="mt-8 text-center text-xs text-gray-400 border-t border-gray-800 pt-4">Proyecto de Grado · Ingeniería de Sistemas 2026</p>
      </section>
    </main>
  );
}

export default LoginPage;
