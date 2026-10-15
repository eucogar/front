import { useRef, useState } from 'react';
import { Check, ScanLine } from 'lucide-react';
import { accessService } from '../../services/accessService';
import { visionService } from '../../services/visionService';
import { getApiError } from '../../api/axiosClient';
import { buttonClass, fieldClass } from '../../constants/ui';
import PageTitle from '../../components/common/PageTitle';
import Notice from '../../components/common/Notice';
import LiveCameraPanel from '../../components/access/LiveCameraPanel';
import { hasPreviewAccess } from '../../routes/ProtectedRoute';

const PLATE_PATTERN = /^[A-Z]{3}\d{2}[A-Z]$/;

export default function LiveCameraAccessPage() {
  const cameraRef = useRef(null);
  const [identificacion, setIdentificacion] = useState('');
  const [placa, setPlaca] = useState('');
  const [detectando, setDetectando] = useState(false);
  const [registrando, setRegistrando] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const detectar = async () => {
    setError('');
    setSuccess('');
    setPlaca('');
    if (!identificacion.trim()) {
      setError('Escribe el número de identificación y pulsa Enter.');
      return;
    }

    setDetectando(true);
    try {
      if (!cameraRef.current?.isRunning()) {
        const iniciada = await cameraRef.current?.start();
        if (!iniciada) return;
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      }
      const captura = await cameraRef.current.capture();
      const lectura = (await visionService.detectarPlaca(captura)).trim().toUpperCase();
      if (!PLATE_PATTERN.test(lectura)) {
        setError(lectura ? `La lectura “${lectura}” no cumple el formato de placa de motocicleta. Ajusta el recuadro e inténtalo de nuevo.` : 'No se detectó una placa. Centra la matrícula en el recuadro y pulsa Enter para reintentar.');
        return;
      }
      setPlaca(lectura);
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setDetectando(false);
    }
  };

  const registrar = async () => {
    setError('');
    setSuccess('');
    if (!identificacion.trim()) {
      setError('Ingresa la identificación antes de confirmar.');
      return;
    }
    if (!PLATE_PATTERN.test(placa.trim().toUpperCase())) {
      setError('Confirma o corrige la placa para que tenga 3 letras, 2 números y una letra final.');
      return;
    }
    if (hasPreviewAccess()) {
      setError('La vista previa no registra movimientos. Inicia sesión para confirmar la entrada o salida.');
      return;
    }

    setRegistrando(true);
    try {
      const data = await accessService.registrarAcceso({
        identificacion: identificacion.trim(),
        placa: placa.trim().toUpperCase(),
      });
      setSuccess(data?.mensaje || data?.Mensaje || data?.message || 'Movimiento registrado correctamente.');
      setIdentificacion('');
      setPlaca('');
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setRegistrando(false);
    }
  };

  return (
    <>
      <PageTitle eyebrow="Control vehicular" title="Acceso con cámara en vivo" />
      <p className="mb-6 max-w-3xl text-sm leading-6 text-slate-400">Escribe o escanea la identificación en el campo y pulsa Enter. El sistema analiza una captura del recuadro; revisa la placa y confirma el movimiento antes de enviarlo al backend.</p>
      <Notice error={error} success={success} />

      <div className="grid max-w-6xl gap-5 xl:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)]">
        <LiveCameraPanel ref={cameraRef} />

        <section className="h-fit space-y-4 rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <label className="block text-sm text-slate-300">
            Cédula / identificación
            <input
              className={`${fieldClass} mt-2`}
              value={identificacion}
              onChange={event => setIdentificacion(event.target.value.replace(/[^\d]/g, '').slice(0, 20))}
              onKeyDown={event => {
                if (event.key === 'Enter') {
                  event.preventDefault();
                  detectar();
                }
              }}
              inputMode="numeric"
              enterKeyHint="search"
              autoComplete="off"
              maxLength={20}
              placeholder="Escribe la identificación"
            />
          </label>

          <button type="button" onClick={detectar} className={`${buttonClass} w-full`} disabled={detectando || registrando}>
            <ScanLine size={17} /> {detectando ? 'Leyendo recuadro…' : 'Detectar placa (Enter)'}
          </button>

          <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Revisa la lectura antes de guardar</p>
            <label className="mt-3 block text-sm text-slate-300">
              Placa detectada
              <input
                className={`${fieldClass} mt-2 text-lg font-bold uppercase tracking-widest`}
                value={placa}
                onChange={event => setPlaca(event.target.value.replace(/[^a-z\d]/gi, '').toUpperCase().slice(0, 6))}
                maxLength={6}
                placeholder="ABC12D"
                autoComplete="off"
              />
            </label>
            <p className="mt-2 text-xs text-slate-500">Puedes corregir un carácter antes de confirmar. El registro no se envía al backend hasta pulsar el botón verde.</p>
          </div>

          <button type="button" onClick={registrar} className={`${buttonClass} w-full`} disabled={registrando || detectando || !PLATE_PATTERN.test(placa)}>
            <Check size={17} /> {registrando ? 'Registrando…' : 'Confirmar entrada / salida'}
          </button>
          <p className="text-xs leading-5 text-slate-500">El backend decide si corresponde entrada o salida según el último movimiento abierto de esa placa.</p>
        </section>
      </div>
    </>
  );
}
