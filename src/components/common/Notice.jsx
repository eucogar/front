export default function Notice({ error, success }) {
  if (!error && !success) return null;

  return (
    <div role="status" className={`mb-5 rounded-xl border p-3 text-sm ${error ? 'border-red-500/30 bg-red-500/10 text-red-300' : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300'}`}>
      {error || success}
    </div>
  );
}
