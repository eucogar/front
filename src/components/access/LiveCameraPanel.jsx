import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import { Camera, CameraOff, ScanLine } from 'lucide-react';
import { buttonClass } from '../../constants/ui';

const LiveCameraPanel = forwardRef(function LiveCameraPanel(_props, ref) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [dimensions, setDimensions] = useState(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');

  const stop = () => {
    streamRef.current?.getTracks().forEach(track => track.stop());
    streamRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    setRunning(false);
  };

  const start = async () => {
    setError('');
    if (!navigator.mediaDevices?.getUserMedia) {
      setError('El navegador no permite usar la cámara en esta dirección. Abre el sistema con HTTPS y vuelve a intentarlo.');
      return false;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
          facingMode: { ideal: 'environment' },
          width: { ideal: 1920 },
          height: { ideal: 1080 },
        },
      });
      streamRef.current = stream;
      videoRef.current.srcObject = stream;
      await videoRef.current.play();
      setDimensions({ width: videoRef.current.videoWidth, height: videoRef.current.videoHeight });
      setRunning(true);
      return true;
    } catch (cameraError) {
      const messages = {
        NotAllowedError: 'Permite el acceso a la cámara en el navegador y vuelve a iniciarla.',
        NotFoundError: 'No se encontró una cámara disponible en este dispositivo.',
        NotReadableError: 'La cámara está siendo usada por otra aplicación.',
      };
      setError(messages[cameraError.name] || `No se pudo iniciar la cámara: ${cameraError.message}`);
      return false;
    }
  };

  const capture = () => new Promise((resolve, reject) => {
    const video = videoRef.current;
    if (!streamRef.current || !video || video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA) {
      reject(new Error('Inicia la cámara y espera a que aparezca la imagen en vivo.'));
      return;
    }
    const roiWidth = Math.min(video.videoWidth * 0.88, video.videoHeight * 0.55 * 3);
    const roiHeight = roiWidth / 3;
    const x = (video.videoWidth - roiWidth) / 2;
    const y = (video.videoHeight - roiHeight) / 2;
    const canvas = document.createElement('canvas');
    canvas.width = Math.round(roiWidth);
    canvas.height = Math.round(roiHeight);
    canvas.getContext('2d').drawImage(video, x, y, roiWidth, roiHeight, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
      if (!blob) reject(new Error('No se pudo capturar el recuadro de la cámara.'));
      else resolve(new File([blob], `captura-placa-${Date.now()}.jpg`, { type: 'image/jpeg' }));
    }, 'image/jpeg', 0.94);
  });

  useImperativeHandle(ref, () => ({ start, stop, capture, isRunning: () => Boolean(streamRef.current) }));
  useEffect(() => () => {
    streamRef.current?.getTracks().forEach(track => track.stop());
  }, []);

  return (
    <section className="space-y-3 rounded-2xl border border-slate-800 bg-slate-900 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="font-semibold text-white">Cámara en vivo</h2>
          <p className="mt-1 text-xs text-slate-400">Centra una sola placa dentro del recuadro.</p>
        </div>
        {running ? (
          <button type="button" onClick={stop} className="inline-flex items-center gap-2 rounded-xl border border-slate-700 px-3 py-2 text-sm text-slate-200 hover:bg-slate-800"><CameraOff size={16} /> Apagar cámara</button>
        ) : (
          <button type="button" onClick={start} className={buttonClass}><Camera size={16} /> Iniciar cámara</button>
        )}
      </div>

      <div className="relative overflow-hidden rounded-xl bg-black">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className="block h-auto max-h-[62vh] w-full object-contain"
          style={{ aspectRatio: dimensions ? `${dimensions.width} / ${dimensions.height}` : '16 / 9' }}
          onLoadedMetadata={event => setDimensions({ width: event.currentTarget.videoWidth, height: event.currentTarget.videoHeight })}
        />
        {!running && <div className="absolute inset-0 grid place-items-center px-5 text-center text-sm text-slate-400">La vista de la cámara aparecerá aquí.</div>}
        {running && <div className="pointer-events-none absolute left-1/2 top-1/2 flex w-[88%] -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-lg border-2 border-emerald-300 shadow-[0_0_0_9999px_rgba(2,6,23,0.32)]" style={{ aspectRatio: '3 / 1' }}><ScanLine className="text-emerald-300/70" size={24} /></div>}
      </div>
      {error && <p role="alert" className="rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">{error}</p>}
      <p className="text-xs leading-5 text-slate-500">En celular, abre esta página por HTTPS, permite la cámara y usa la cámara trasera. En desarrollo, el teléfono y el computador deben estar en la misma red Wi-Fi.</p>
    </section>
  );
});

export default LiveCameraPanel;
