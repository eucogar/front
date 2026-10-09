import { NavLink } from 'react-router-dom';

export default function SummaryCard({ icon: Icon, title, text, to }) {
  return (
    <NavLink to={to} className="rounded-2xl border border-slate-800 bg-slate-900 p-5 transition hover:border-emerald-500/50">
      <Icon className="mb-4 text-emerald-400" />
      <h2 className="mb-1 font-semibold text-white">{title}</h2>
      <p className="text-sm text-slate-400">{text}</p>
    </NavLink>
  );
}
