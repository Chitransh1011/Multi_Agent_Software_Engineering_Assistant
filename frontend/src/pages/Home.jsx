import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getStats, health } from '../api'

const agentStages = [
  ['01', 'Plan', 'Breaks requests into an execution plan'],
  ['02', 'Research', 'Retrieves relevant context when needed'],
  ['03', 'Build', 'Creates implementation-ready outputs'],
  ['04', 'Review', 'Checks quality and retries if required'],
  ['05', 'Deliver', 'Produces a clear final response'],
]

function Stat({ label, value, caption }) { return <div className="glass-card rounded-2xl p-5"><div className="text-sm text-slate-400">{label}</div><div className="mt-2 text-3xl font-bold tracking-tight text-white">{value}</div><div className="mt-2 text-xs text-slate-500">{caption}</div></div> }

export default function Home() {
  const [server, setServer] = useState('checking')
  const [stats, setStats] = useState(null)
  useEffect(() => {
    health().then(() => setServer('online')).catch(() => setServer('offline'))
    getStats().then((response) => setStats(response.data)).catch(() => setStats(null))
  }, [])
  const statusStyle = server === 'online' ? 'bg-emerald-400' : server === 'offline' ? 'bg-rose-400' : 'bg-amber-300 animate-pulse'
  return <div className="space-y-12">
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900 via-slate-900 to-cyan-950/50 px-6 py-10 shadow-2xl shadow-slate-950/40 sm:px-10 sm:py-14">
      <div className="absolute -right-12 -top-16 h-64 w-64 rounded-full border border-cyan-300/10" /><div className="absolute right-14 top-16 h-32 w-32 rounded-full border border-blue-300/10" />
      <div className="relative max-w-3xl"><div className="eyebrow flex items-center gap-2"><span className={`h-2 w-2 rounded-full ${statusStyle}`} />Backend {server}</div><h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">From a prompt to a <span className="text-cyan-300">reviewed outcome.</span></h1><p className="mt-5 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">AgentFlow coordinates specialized AI agents through a transparent, persisted engineering workflow—planning, research, implementation, review, and delivery.</p><div className="mt-8 flex flex-wrap gap-3"><Link to="/generate" className="primary-button">Start an agent run <span>→</span></Link><Link to="/conversations" className="secondary-button">Explore run history</Link></div></div>
    </section>
    <section><div className="mb-5 flex items-end justify-between"><div><p className="eyebrow">Live workspace</p><h2 className="text-xl font-bold text-white">Execution snapshot</h2></div><span className="text-xs text-slate-500">Database-backed metrics</span></div><div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"><Stat label="Conversations" value={stats?.total_conversations ?? '—'} caption="All recorded workflow runs" /><Stat label="Success rate" value={stats ? `${stats.success_rate}%` : '—'} caption={`${stats?.completed_conversations ?? 0} completed runs`} /><Stat label="Avg. latency" value={stats ? `${Math.round(stats.average_latency_ms)} ms` : '—'} caption="Across all agent stages" /><Stat label="Artifacts created" value={stats?.total_messages ?? '—'} caption="Agent messages persisted" /></div>{!stats && <p className="mt-3 text-xs text-slate-500">Metrics become available when the database service is running.</p>}</section>
    <section className="glass-card rounded-3xl p-6 sm:p-8"><div className="mb-8 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between"><div><p className="eyebrow">How it works</p><h2 className="text-2xl font-bold text-white">A deliberate agent pipeline</h2></div><p className="max-w-sm text-sm leading-6 text-slate-400">Each run is tracked from the incoming request to its final artifacts, messages, and execution history.</p></div><div className="grid gap-3 md:grid-cols-5">{agentStages.map(([number, title, text], index) => <div key={title} className="relative rounded-2xl border border-white/10 bg-slate-950/40 p-4"><div className="mb-5 flex items-center justify-between"><span className="text-xs font-bold text-cyan-300">{number}</span>{index < 4 && <span className="hidden text-slate-600 md:block">→</span>}</div><h3 className="font-bold text-white">{title}</h3><p className="mt-2 text-xs leading-5 text-slate-400">{text}</p></div>)}</div></section>
  </div>
}
