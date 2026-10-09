import { Component } from 'react';

export default class AppErrorBoundary extends Component {
  state = { error: null };

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error('Frontend render error:', error, info);
  }

  render() {
    if (!this.state.error) return this.props.children;

    return (
      <main className="grid min-h-screen place-items-center bg-slate-950 px-5 text-slate-100">
        <section className="w-full max-w-xl rounded-2xl border border-red-500/30 bg-slate-900 p-6">
          <p className="mb-2 text-xs font-bold uppercase tracking-widest text-red-300">Error de interfaz</p>
          <h1 className="text-xl font-semibold">No se pudo mostrar esta pantalla</h1>
          <p className="mt-3 break-words text-sm text-slate-300">{this.state.error.message || 'Ocurrió un error inesperado al dibujar la página.'}</p>
          <button onClick={() => window.location.reload()} className="mt-5 rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold hover:bg-emerald-500">Recargar la aplicación</button>
        </section>
      </main>
    );
  }
}
