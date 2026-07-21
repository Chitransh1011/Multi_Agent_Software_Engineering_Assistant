import React from 'react'
import { NavLink, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Generate from './pages/Generate'
import Conversations from './pages/Conversations'

const navItems = [
  { to: '/', label: 'Overview', icon: '◇' },
  { to: '/generate', label: 'New run', icon: '✦' },
  { to: '/conversations', label: 'Run history', icon: '◫' },
]

function Logo() {
  return <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-300 to-blue-500 text-lg font-black text-slate-950 shadow-lg shadow-cyan-500/20">A</div>
}

export default function App() {
  return (
    <div className="app-shell">
      <div className="fixed inset-0 -z-10 overflow-hidden">
        <div className="absolute -left-28 top-0 h-96 w-96 rounded-full bg-cyan-500/10 blur-3xl" />
        <div className="absolute right-0 top-1/3 h-80 w-80 rounded-full bg-blue-600/10 blur-3xl" />
      </div>
      <header className="sticky top-0 z-30 border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
        <div className="app-container flex h-[76px] items-center justify-between gap-5">
          <NavLink to="/" className="flex items-center gap-3" aria-label="AgentFlow home">
            <Logo />
            <div><div className="font-bold tracking-tight text-white">AgentFlow</div><div className="text-[11px] font-medium tracking-wide text-slate-500">AI ENGINEERING STUDIO</div></div>
          </NavLink>
          <nav className="flex items-center gap-1 rounded-xl border border-white/10 bg-white/[0.03] p-1" aria-label="Main navigation">
            {navItems.map((item) => <NavLink key={item.to} to={item.to} end={item.to === '/'} className={({ isActive }) => `flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold transition sm:px-4 ${isActive ? 'bg-white/10 text-white shadow-sm' : 'text-slate-400 hover:text-slate-100'}`}><span className="hidden text-cyan-300 sm:inline">{item.icon}</span>{item.label}</NavLink>)}
          </nav>
          <div className="hidden items-center gap-2 text-xs font-medium text-emerald-300 md:flex"><span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_10px] shadow-emerald-400" />Multi-agent system</div>
        </div>
      </header>
      <main className="app-container py-10 sm:py-14"><Routes><Route path="/" element={<Home />} /><Route path="/generate" element={<Generate />} /><Route path="/conversations" element={<Conversations />} /></Routes></main>
    </div>
  )
}
