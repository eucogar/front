export default function PageTitle({ eyebrow, title, children }) {
  return (
    <header className="mb-7 flex flex-wrap items-end justify-between gap-4">
      <div>
        <div className="mb-1 text-xs font-bold uppercase tracking-[.18em] text-emerald-400">{eyebrow}</div>
        <h1 className="text-2xl font-bold text-white md:text-3xl">{title}</h1>
      </div>
      {children}
    </header>
  );
}
