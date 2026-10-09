import { useEffect, useRef, useState } from 'react';
import { accessService } from '../../services/accessService';
import { userService } from '../../services/userService';
import { getApiError } from '../../api/axiosClient';
import { buttonClass, fieldClass } from '../../constants/ui';
import PageTitle from '../../components/common/PageTitle';
import Notice from '../../components/common/Notice';
import { hasPreviewAccess } from '../../routes/ProtectedRoute';

export default function RegisterAccessPage() {
  const [identificacion, setIdentificacion] = useState('');
  const [placa, setPlaca] = useState('');
  const [imagen, setImagen] = useState(null);
  const [usuarios, setUsuarios] = useState([]);
  const inputImagen = useRef(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (hasPreviewAccess()) return undefined;
    let activo = true;
    userService.listarUsuarios()
      .then(data => { if (activo) setUsuarios(Array.isArray(data) ? data.filter(usuario => usuario.estado) : []); })
      .catch(() => {});
    return () => { activo = false; };
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    setResult(null);
    if (hasPreviewAccess()) {
      setError('El modo vista previa no guarda movimientos. Inicia sesion con la API conectada.');
      return;
    }
    if (!identificacion.trim()) {
      setError('Ingresa la cedula del usuario.');
      return;
    }
    if (!imagen && !placa.trim()) {
      setError('Carga una foto para reconocer la placa o escribela manualmente.');
      return;
    }

    setLoading(true);
    try {
      let data;
      if (imagen) {
        const payload = new FormData();
        payload.append('identificacion', identificacion.trim());
        payload.append('imagen', imagen);
        try {
          const response = await accessService.detectarYRegistrar(payload);
          data = { ...(response?.data ?? response), identificacion: identificacion.trim() };
        } catch (visionError) {
          const status = visionError?.response?.status;
          if (!placa.trim() || ![422, 502, 503, 504].includes(status)) throw visionError;
          const response = await accessService.registrarAcceso({
            identificacion: identificacion.trim(),
            placa: placa.trim().toUpperCase(),
          });
          data = { ...(response?.data ?? response), identificacion: identificacion.trim(), placa: placa.trim().toUpperCase() };
        }
      } else {
        const response = await accessService.registrarAcceso({
          identificacion: identificacion.trim(),
          placa: placa.trim().toUpperCase(),
        });
        data = { ...(response?.data ?? response), identificacion: identificacion.trim(), placa: placa.trim().toUpperCase() };
      }

      setResult(data);
      if ((data?.codigo ?? data?.Codigo ?? data?.code) > 0) {
        setIdentificacion('');
        setPlaca('');
        setImagen(null);
        if (inputImagen.current) inputImagen.current.value = '';
      }
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <PageTitle eyebrow="Control vehicular" title="Registrar entrada o salida" />
      <p className="mb-6 max-w-2xl text-sm leading-6 text-slate-400">La cedula identifica al usuario. Puedes reconocer la placa con una foto o escribirla manualmente. El backend registra entrada o salida segun el ultimo movimiento abierto.</p>
      <Notice error={error} success={result?.mensaje || result?.Mensaje || result?.message} />
      <form onSubmit={submit} className="max-w-xl space-y-4 rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <label className="block text-sm text-slate-300">Cedula / identificacion<input list="usuarios-activos" className={`${fieldClass} mt-2`} required maxLength={20} value={identificacion} onChange={event => setIdentificacion(event.target.value)} /></label>
        <datalist id="usuarios-activos">{usuarios.map(usuario => <option key={usuario.identificacion} value={usuario.identificacion}>{usuario.nombres} {usuario.apellidos}</option>)}</datalist>
        <label className="block text-sm text-slate-300">Placa (alternativa manual)<input className={`${fieldClass} mt-2 uppercase`} maxLength={10} value={placa} onChange={event => setPlaca(event.target.value.toUpperCase())} placeholder="ABC12D" /></label>
        <p className="text-xs text-slate-500">La cedula se envia con la placa en ambos casos. Si la foto no permite reconocerla y escribiste la placa, se registra la placa manual.</p>
        <label className="block text-sm text-slate-300">Foto de la placa (opcional)<input ref={inputImagen} className={`${fieldClass} mt-2`} type="file" accept="image/jpeg,image/png,image/webp" capture="environment" onChange={event => setImagen(event.target.files?.[0] || null)} /></label>
        {imagen && <p className="text-xs text-slate-400">Imagen seleccionada: {imagen.name}</p>}
        {result?.identificacion && <p className="rounded-lg bg-slate-800 p-3 text-sm text-slate-200">CC registrada: <strong className="text-emerald-300">{result.identificacion}</strong></p>}
        {(result?.placa || result?.Placa) && <p className="rounded-lg bg-slate-800 p-3 text-sm text-slate-200">Placa procesada: <strong className="text-emerald-300">{result.placa || result.Placa}</strong></p>}
        <button className={buttonClass} disabled={loading}>{loading ? 'Procesando...' : 'Registrar movimiento'}</button>
      </form>
    </>
  );
}
