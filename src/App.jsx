import React, { useState, useEffect, useRef } from 'react'
import {
  BarChart, Bar, LineChart, Line, AreaChart, Area,
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  ScatterChart, Scatter, XAxis, YAxis, ZAxis,
  CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  Cell, PieChart, Pie, ReferenceLine
} from 'recharts'
import {
  TrendingUp, Globe, Zap, Leaf, BarChart2,
  GitBranch, AlertCircle, CheckCircle2, Clock,
  ExternalLink, ChevronRight, Activity, Database,
  Shield, Target, ArrowUpRight, ArrowDownRight
} from 'lucide-react'

// ─── DATA ───────────────────────────────────────────────────────────────────

const GREEN_BONDS = [
  { year: 2015, amount: 1000, issuer: 'IREDA', type: 'psu' },
  { year: 2016, amount: 500,  issuer: 'Yes Bank', type: 'bank' },
  { year: 2017, amount: 2300, issuer: 'NTPC+CLP', type: 'psu' },
  { year: 2018, amount: 1400, issuer: 'Adani+ReNew', type: 'corporate' },
  { year: 2019, amount: 1950, issuer: 'Hero+PFC', type: 'psu' },
  { year: 2020, amount: 1200, issuer: 'IREDA', type: 'psu' },
  { year: 2021, amount: 700,  issuer: 'L&T Finance', type: 'bank' },
  { year: 2022, amount: 2900, issuer: 'REC+Tata Power', type: 'psu' },
  { year: 2023, amount: 26400,issuer: 'GoI+Greenko', type: 'sovereign' },
  { year: 2024, amount: 26850,issuer: 'GoI+NTPC+Others', type: 'sovereign' },
]

const SECTOR_CAPITAL = [
  { sector: 'Utility Renewables', need: 32, risk: 'Core+', maturity: 'Mature', color: '#34d399' },
  { sector: 'Grid & Transmission', need: 24, risk: 'Core', maturity: 'Mature', color: '#2dd4bf' },
  { sector: 'Industrial Decarb', need: 27.5, risk: 'Opportunistic', maturity: 'Early', color: '#fbbf24' },
  { sector: 'EV & Fleet', need: 14.8, risk: 'Core+', maturity: 'Scaling', color: '#60a5fa' },
  { sector: 'Battery Storage', need: 11.5, risk: 'Core+', maturity: 'Scaling', color: '#a78bfa' },
  { sector: 'Green Buildings', need: 8.2, risk: 'Core+', maturity: 'Mature', color: '#fb923c' },
]

const EMISSIONS = [
  { sector: 'Power', baseline: 1120, y2030: 860, y2050: 210, lever: 'Renewables + Storage' },
  { sector: 'Steel', baseline: 290, y2030: 240, y2050: 92, lever: 'H₂-DRI + Scrap-EAF' },
  { sector: 'Transport', baseline: 340, y2030: 255, y2050: 95, lever: 'Fleet Electrification' },
  { sector: 'Agriculture', baseline: 410, y2030: 372, y2050: 250, lever: 'Methane Reduction' },
  { sector: 'Cement', baseline: 210, y2030: 176, y2050: 78, lever: 'Clinker Sub + CCUS' },
  { sector: 'Buildings', baseline: 125, y2030: 96, y2050: 44, lever: 'Efficiency + Cooling' },
]

const NET_ZERO_MILESTONES = [
  { year: 2030, renewGW: 500, evShare: 30, carbonPrice: 3000, emissionsRed: 45, renewPower: 65 },
  { year: 2040, renewGW: 1000, evShare: 70, carbonPrice: 5500, emissionsRed: 65, renewPower: 85 },
  { year: 2050, renewGW: 1800, evShare: 95, carbonPrice: 8000, emissionsRed: 80, renewPower: 95 },
  { year: 2070, renewGW: 2500, evShare: 100, carbonPrice: 12000, emissionsRed: 100, renewPower: 99 },
]

const ESG_SCORES = [
  { ticker: 'INFY', name: 'Infosys', sector: 'IT', E: 82, S: 80, G: 88, composite: 83.4, coal: 0 },
  { ticker: 'TCS', name: 'TCS', sector: 'IT', E: 78, S: 82, G: 85, composite: 81.4, coal: 0 },
  { ticker: 'WIPRO', name: 'Wipro', sector: 'IT', E: 80, S: 75, G: 82, composite: 79.1, coal: 0 },
  { ticker: 'HCLTECH', name: 'HCL Tech', sector: 'IT', E: 76, S: 72, G: 80, composite: 76.2, coal: 0 },
  { ticker: 'SUNPHARMA', name: 'Sun Pharma', sector: 'Healthcare', E: 65, S: 68, G: 75, composite: 68.7, coal: 0 },
  { ticker: 'HDFCBANK', name: 'HDFC Bank', sector: 'Financials', E: 62, S: 70, G: 80, composite: 70, coal: 0 },
  { ticker: 'ICICIBANK', name: 'ICICI Bank', sector: 'Financials', E: 58, S: 65, G: 78, composite: 66.5, coal: 0 },
  { ticker: 'BAJFINSERV', name: 'Bajaj Finserv', sector: 'Financials', E: 55, S: 62, G: 78, composite: 63.8, coal: 0 },
  { ticker: 'AXISBANK', name: 'Axis Bank', sector: 'Financials', E: 55, S: 62, G: 74, composite: 62.5, coal: 0 },
  { ticker: 'MARUTI', name: 'Maruti Suzuki', sector: 'Con. Disc.', E: 52, S: 62, G: 74, composite: 61.4, coal: 0 },
  { ticker: 'LT', name: 'L&T', sector: 'Industrials', E: 50, S: 60, G: 75, composite: 60.5, coal: 0 },
  { ticker: 'ADANIPORTS', name: 'Adani Ports', sector: 'Industrials', E: 45, S: 50, G: 55, composite: 49.5, coal: 0 },
  { ticker: 'ASIANPAINT', name: 'Asian Paints', sector: 'Materials', E: 60, S: 65, G: 80, composite: 67.5, coal: 0 },
  { ticker: 'RELIANCE', name: 'Reliance', sector: 'Energy', E: 42, S: 55, G: 68, composite: 52.6, coal: 5 },
  { ticker: 'TATASTEEL', name: 'Tata Steel', sector: 'Materials', E: 40, S: 58, G: 72, composite: 52, coal: 0 },
  { ticker: 'JSWSTEEL', name: 'JSW Steel', sector: 'Materials', E: 35, S: 50, G: 66, composite: 46.8, coal: 0 },
  { ticker: 'HINDALCO', name: 'Hindalco', sector: 'Materials', E: 38, S: 48, G: 62, composite: 46.4, coal: 0 },
  { ticker: 'ULTRACEM', name: 'UltraTech', sector: 'Materials', E: 32, S: 52, G: 68, composite: 46.4, coal: 0 },
  { ticker: 'NTPCLTD', name: 'NTPC', sector: 'Utilities', E: 30, S: 55, G: 65, composite: 45.5, coal: 85 },
  { ticker: 'COALINDIA', name: 'Coal India', sector: 'Energy', E: 18, S: 52, G: 58, composite: 36.2, coal: 98 },
]

const DEAL_ECONOMICS = [
  { sector: 'Utility Renewables', deals: 18, ticket: 1450, feeBps: 85, feePool: 221.9, instrument: 'Project Finance' },
  { sector: 'Grid & Transmission', deals: 9, ticket: 2800, feeBps: 52, feePool: 131.0, instrument: 'Structured Term Loan' },
  { sector: 'Industrial Decarb', deals: 13, ticket: 2350, feeBps: 105, feePool: 320.8, instrument: 'Transition Finance' },
  { sector: 'Battery Storage', deals: 11, ticket: 1180, feeBps: 95, feePool: 123.3, instrument: 'Project Finance' },
  { sector: 'Green Buildings', deals: 24, ticket: 265, feeBps: 115, feePool: 73.1, instrument: 'Green Loan' },
  { sector: 'EV & Fleet', deals: 21, ticket: 180, feeBps: 140, feePool: 52.9, instrument: 'SLL' },
]

const INVESTMENT_NEEDS = [
  { period: '2025–30', need: 180, label: '$180B/yr' },
  { period: '2030–40', need: 260, label: '$260B/yr' },
  { period: '2040–50', need: 300, label: '$300B/yr' },
]

const ISSUES = [
  { id: 16, title: 'Companion notebooks for all remaining src/ modules', labels: ['documentation', 'notebook'] },
  { id: 15, title: 'RBI climate-risk capital impact model', labels: ['model-needed', 'policy', 'climate-risk'] },
  { id: 14, title: 'State-level ESG readiness overlay', labels: ['data-gap', 'policy', 'research-gap'] },
  { id: 13, title: 'Green buildings & municipal finance subsector', labels: ['model-needed', 'sector-expansion'] },
  { id: 12, title: 'Green MSME & fintech archetypes', labels: ['data-gap', 'sector-expansion'] },
  { id: 11, title: 'Model non-cash incentives & green credits', labels: ['model-needed', 'policy'] },
  { id: 10, title: 'BRSR disclosure quality overlay in bank views', labels: ['good first issue', 'data-gap'] },
  { id: 8, title: 'SGrB yield & greenium module', labels: ['data-gap', 'model-needed', 'notebook'] },
]

const COMMITS = [
  { sha: '73cad19', msg: 'Merge pull request #18: Add missing synthetic data files', date: '2026-05-25' },
  { sha: 'd389d26', msg: 'Add missing synthetic data files', date: '2026-05-22' },
  { sha: 'c04f10e', msg: 'docs: unified README combining research + commercial layer', date: '2026-04-07' },
  { sha: '762657c', msg: 'Add CONTRIBUTING.md, issue templates, missing core models', date: '2026-04-07' },
  { sha: 'ed69893', msg: 'docs: overhaul README with clean structure and key findings', date: '2026-04-05' },
]

// ─── HELPERS ────────────────────────────────────────────────────────────────

const LABEL_COLORS = {
  'documentation': '#60a5fa', 'notebook': '#a78bfa', 'good first issue': '#34d399',
  'model-needed': '#fbbf24', 'data-gap': '#fb923c', 'policy': '#2dd4bf',
  'climate-risk': '#f87171', 'research-gap': '#e879f9', 'testing': '#94a3b8',
  'sector-expansion': '#34d399',
}

const CustomTooltip = ({ active, payload, label, unit = '' }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'rgba(12,18,24,0.97)', border: '1px solid rgba(52,211,153,0.2)',
      borderRadius: 8, padding: '10px 14px', fontFamily: 'DM Mono, monospace', fontSize: 12
    }}>
      <div style={{ color: '#8faaa5', marginBottom: 6 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color || '#34d399', marginTop: 2 }}>
          {p.name}: <span style={{ color: '#e8f0ef' }}>{typeof p.value === 'number' ? p.value.toLocaleString() : p.value}{unit}</span>
        </div>
      ))}
    </div>
  )
}

// ─── COMPONENTS ─────────────────────────────────────────────────────────────

function Card({ children, style = {}, className = '' }) {
  return (
    <div className={className} style={{
      background: 'var(--bg1)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--r)',
      padding: '20px 22px',
      ...style
    }}>
      {children}
    </div>
  )
}

function SectionTitle({ children, sub }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <h2 style={{ fontFamily: 'var(--font-head)', fontSize: '1.35rem', fontWeight: 700, color: 'var(--text)', letterSpacing: '-0.01em' }}>
        {children}
      </h2>
      {sub && <p style={{ color: 'var(--text3)', fontSize: 12, marginTop: 4, fontFamily: 'var(--font-mono)' }}>{sub}</p>}
    </div>
  )
}

function KpiCard({ label, value, sub, icon: Icon, delta, color = 'var(--green)' }) {
  return (
    <Card style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>{label}</span>
        {Icon && <Icon size={16} color={color} />}
      </div>
      <div style={{ fontFamily: 'var(--font-head)', fontSize: '2rem', fontWeight: 800, color, lineHeight: 1 }}>{value}</div>
      {sub && <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)' }}>{sub}</div>}
      {delta !== undefined && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginTop: 2 }}>
          {delta >= 0 ? <ArrowUpRight size={12} color="var(--green)" /> : <ArrowDownRight size={12} color="var(--red)" />}
          <span style={{ fontSize: 11, fontFamily: 'var(--font-mono)', color: delta >= 0 ? 'var(--green)' : 'var(--red)' }}>
            {Math.abs(delta)}% vs prior
          </span>
        </div>
      )}
    </Card>
  )
}

// ─── SECTION: OVERVIEW ───────────────────────────────────────────────────────
function OverviewSection() {
  const totalIssuance = GREEN_BONDS.reduce((s, d) => s + d.amount, 0)
  const totalFeePool = DEAL_ECONOMICS.reduce((s, d) => s + d.feePool, 0)
  const totalCapitalNeed = SECTOR_CAPITAL.reduce((s, d) => s + d.need, 0)

  return (
    <section style={{ marginBottom: 48 }}>
      <SectionTitle sub="india · sustainable finance · transition research dashboard">
        India Transition Finance · Overview
      </SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 24 }}>
        <KpiCard label="Total Green Bond Issuance" value="₹65,100Cr" sub="2015–2024 cumulative" icon={TrendingUp} color="var(--green)" delta={41} />
        <KpiCard label="Annual Capital Need" value={`$${totalCapitalNeed.toFixed(0)}B`} sub="across 6 priority sectors" icon={Target} color="var(--teal)" />
        <KpiCard label="Estimated Fee Pool" value={`₹${totalFeePool.toFixed(0)}Cr`} sub="illustrative annual pipeline" icon={BarChart2} color="var(--amber)" />
        <KpiCard label="Net Zero Target" value="2070" sub="India NDC pathway" icon={Globe} color="var(--blue)" />
        <KpiCard label="2030 Renewable Target" value="500 GW" sub="under India NZ scenario" icon={Zap} color="var(--purple)" />
        <KpiCard label="Open Research Issues" value="14" sub="across v1.1 → v2.0 roadmap" icon={GitBranch} color="var(--red)" />
      </div>

      {/* Issuance Timeline */}
      <Card style={{ marginBottom: 16 }}>
        <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.95rem', fontWeight: 600, marginBottom: 16, color: 'var(--text)' }}>
          India Green Bond Issuance Timeline (₹ Crore)
        </div>
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={GREEN_BONDS}>
            <defs>
              <linearGradient id="gbGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#34d399" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#34d399" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis tickFormatter={v => `₹${(v/1000).toFixed(0)}K`} />
            <Tooltip content={<CustomTooltip />} />
            <Area type="monotone" dataKey="amount" name="Amount (₹Cr)" stroke="#34d399" fill="url(#gbGrad)" strokeWidth={2} dot={{ fill: '#34d399', r: 3 }} />
          </AreaChart>
        </ResponsiveContainer>
        <div style={{ display: 'flex', gap: 12, marginTop: 12, flexWrap: 'wrap' }}>
          {[{ label: 'Sovereign', color: '#60a5fa' }, { label: 'PSU', color: '#34d399' }, { label: 'Corporate', color: '#fbbf24' }, { label: 'Bank', color: '#a78bfa' }].map(t => (
            <div key={t.label} style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <div style={{ width: 8, height: 8, borderRadius: '50%', background: t.color }} />
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)' }}>{t.label}</span>
            </div>
          ))}
        </div>
      </Card>
    </section>
  )
}

// ─── SECTION: CAPITAL ALLOCATION ─────────────────────────────────────────────
function CapitalSection() {
  return (
    <section style={{ marginBottom: 48 }}>
      <SectionTitle sub="annual capital requirement by transition subsector (USD bn)">
        Sector Capital Allocation & Deal Economics
      </SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <Card>
          <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 14, color: 'var(--text)' }}>
            Annual Capital Need by Subsector (USD Bn)
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={SECTOR_CAPITAL} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" unit="B" />
              <YAxis type="category" dataKey="sector" width={130} tick={{ fontSize: 11, fontFamily: 'DM Mono, monospace', fill: '#8faaa5' }} />
              <Tooltip content={<CustomTooltip unit="B USD" />} />
              <Bar dataKey="need" name="Capital Need" radius={[0, 4, 4, 0]}>
                {SECTOR_CAPITAL.map((d, i) => <Cell key={i} fill={d.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card>
          <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 14, color: 'var(--text)' }}>
            Deal Economics: Fee Pool vs. Deal Volume (₹Cr)
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={DEAL_ECONOMICS}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="sector" tick={{ fontSize: 10, fontFamily: 'DM Mono, monospace', fill: '#8faaa5' }} angle={-25} textAnchor="end" height={60} />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Bar yAxisId="left" dataKey="feePool" name="Fee Pool (₹Cr)" fill="#fbbf24" opacity={0.85} radius={[4, 4, 0, 0]} />
              <Bar yAxisId="right" dataKey="deals" name="Deal Count" fill="#60a5fa" opacity={0.7} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Risk matrix table */}
        <Card style={{ gridColumn: '1 / -1' }}>
          <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 14, color: 'var(--text)' }}>
            Sector Risk–Maturity Matrix
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'var(--font-mono)', fontSize: 12 }}>
              <thead>
                <tr>
                  {['Subsector', 'Capital Need', 'Risk Profile', 'Market Maturity', 'Annual Deals', 'Avg Ticket (₹Cr)', 'Fee (bps)', 'Primary Instrument'].map(h => (
                    <th key={h} style={{ padding: '8px 12px', textAlign: 'left', color: 'var(--text3)', borderBottom: '1px solid var(--border)', fontWeight: 400, whiteSpace: 'nowrap' }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {DEAL_ECONOMICS.map((d, i) => {
                  const cap = SECTOR_CAPITAL.find(c => c.sector === d.sector)
                  const riskColor = { Core: 'var(--green)', 'Core+': 'var(--teal)', 'Opportunistic': 'var(--amber)' }[cap?.risk] || 'var(--text2)'
                  const matColor = { Mature: 'var(--green)', Scaling: 'var(--blue)', Early: 'var(--amber)' }[cap?.maturity] || 'var(--text2)'
                  return (
                    <tr key={i} style={{ borderBottom: '1px solid var(--border)', transition: 'background .15s' }}
                      onMouseEnter={e => e.currentTarget.style.background = 'var(--bg2)'}
                      onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                      <td style={{ padding: '10px 12px', color: 'var(--text)' }}>{d.sector}</td>
                      <td style={{ padding: '10px 12px', color: cap?.color || 'var(--text2)' }}>${cap?.need}B</td>
                      <td style={{ padding: '10px 12px' }}><span style={{ color: riskColor, background: riskColor + '15', padding: '2px 8px', borderRadius: 4 }}>{cap?.risk}</span></td>
                      <td style={{ padding: '10px 12px' }}><span style={{ color: matColor, background: matColor + '15', padding: '2px 8px', borderRadius: 4 }}>{cap?.maturity}</span></td>
                      <td style={{ padding: '10px 12px', color: 'var(--text2)' }}>{d.deals}</td>
                      <td style={{ padding: '10px 12px', color: 'var(--text2)' }}>₹{d.ticket.toLocaleString()}</td>
                      <td style={{ padding: '10px 12px', color: 'var(--amber)' }}>{d.feeBps} bps</td>
                      <td style={{ padding: '10px 12px', color: 'var(--text2)' }}>{d.instrument}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </section>
  )
}

// ─── SECTION: EMISSIONS & NET ZERO ────────────────────────────────────────────
function EmissionsSection() {
  return (
    <section style={{ marginBottom: 48 }}>
      <SectionTitle sub="India Net Zero 2070 scenario · sector emissions trajectories · MtCO₂e">
        Decarbonisation Pathways & Net Zero Milestones
      </SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 16, marginBottom: 16 }}>
        <Card>
          <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 14, color: 'var(--text)' }}>
            Sector Emissions: Baseline → 2030 → 2050 (MtCO₂e)
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={EMISSIONS}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="sector" tick={{ fontSize: 11, fontFamily: 'DM Mono, monospace', fill: '#8faaa5' }} />
              <YAxis unit=" Mt" />
              <Tooltip content={<CustomTooltip unit=" Mt" />} />
              <Legend />
              <Bar dataKey="baseline" name="2024 Baseline" fill="#f87171" opacity={0.8} radius={[3, 3, 0, 0]} />
              <Bar dataKey="y2030" name="2030 Target" fill="#fbbf24" opacity={0.8} radius={[3, 3, 0, 0]} />
              <Bar dataKey="y2050" name="2050 Target" fill="#34d399" opacity={0.9} radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card>
          <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 14, color: 'var(--text)' }}>
            Net Zero Pathway: Key Milestones
          </div>
          <ResponsiveContainer width="100%" height={160}>
            <LineChart data={NET_ZERO_MILESTONES}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line type="monotone" dataKey="renewGW" name="Renew. Cap (GW)" stroke="#34d399" strokeWidth={2} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="emissionsRed" name="Emissions ↓ (%)" stroke="#f87171" strokeWidth={2} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="evShare" name="EV Sales Share (%)" stroke="#60a5fa" strokeWidth={2} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>

          <div style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 8 }}>
            {INVESTMENT_NEEDS.map(d => (
              <div key={d.period} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 12px', background: 'var(--bg2)', borderRadius: 6 }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)' }}>{d.period}</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <div style={{ height: 4, borderRadius: 2, background: 'var(--green3)', width: 80, position: 'relative', overflow: 'hidden' }}>
                    <div style={{ position: 'absolute', left: 0, top: 0, height: '100%', background: 'var(--green)', width: `${(d.need / 300) * 100}%`, borderRadius: 2 }} />
                  </div>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--green)', fontWeight: 600 }}>{d.label}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Sector transition levers */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10 }}>
        {EMISSIONS.map(d => {
          const reduction = Math.round(((d.baseline - d.y2050) / d.baseline) * 100)
          return (
            <Card key={d.sector} style={{ padding: '14px 16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                <span style={{ fontFamily: 'var(--font-head)', fontSize: '0.85rem', fontWeight: 600 }}>{d.sector}</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--green)' }}>−{reduction}%</span>
              </div>
              <div style={{ height: 3, background: 'var(--bg3)', borderRadius: 2, marginBottom: 8 }}>
                <div style={{ height: '100%', background: 'var(--green)', borderRadius: 2, width: `${reduction}%` }} />
              </div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text3)' }}>
                {d.baseline} → {d.y2050} MtCO₂e · <span style={{ color: 'var(--teal)' }}>{d.lever}</span>
              </div>
            </Card>
          )
        })}
      </div>
    </section>
  )
}

// ─── SECTION: ESG SCORES ─────────────────────────────────────────────────────
function ESGSection() {
  const [filter, setFilter] = useState('All')
  const sectors = ['All', ...new Set(ESG_SCORES.map(d => d.sector))]
  const filtered = filter === 'All' ? ESG_SCORES : ESG_SCORES.filter(d => d.sector === filter)
  const sorted = [...filtered].sort((a, b) => b.composite - a.composite)

  const radarData = ['IT', 'Financials', 'Materials', 'Energy', 'Industrials'].map(s => {
    const items = ESG_SCORES.filter(d => d.sector === s)
    return {
      sector: s,
      E: Math.round(items.reduce((a, b) => a + b.E, 0) / items.length),
      S: Math.round(items.reduce((a, b) => a + b.S, 0) / items.length),
      G: Math.round(items.reduce((a, b) => a + b.G, 0) / items.length),
    }
  })

  return (
    <section style={{ marginBottom: 48 }}>
      <SectionTitle sub="Nifty-50 ESG scores · BRSR disclosed · synthetic research data">
        ESG Scoring · Indian Capital Markets
      </SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: 16 }}>
        <Card>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
            <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, color: 'var(--text)' }}>
              Composite ESG Score — Nifty-50 Sample
            </div>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {sectors.map(s => (
                <button key={s} onClick={() => setFilter(s)} style={{
                  fontFamily: 'var(--font-mono)', fontSize: 10, padding: '3px 8px', borderRadius: 4, cursor: 'pointer',
                  background: filter === s ? 'var(--green)' : 'var(--bg3)',
                  color: filter === s ? 'var(--bg)' : 'var(--text3)',
                  border: 'none', transition: 'all .2s'
                }}>{s}</button>
              ))}
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sorted} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="ticker" width={90} tick={{ fontSize: 11, fontFamily: 'DM Mono, monospace', fill: '#8faaa5' }} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine x={60} stroke="rgba(52,211,153,0.3)" strokeDasharray="4 4" />
              <Bar dataKey="composite" name="ESG Composite" radius={[0, 4, 4, 0]}>
                {sorted.map((d, i) => (
                  <Cell key={i} fill={d.composite >= 70 ? '#34d399' : d.composite >= 55 ? '#fbbf24' : '#f87171'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <Card>
            <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 14, color: 'var(--text)' }}>
              E / S / G by Sector (avg.)
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="var(--border)" />
                <PolarAngleAxis dataKey="sector" tick={{ fontFamily: 'DM Mono, monospace', fontSize: 10, fill: '#8faaa5' }} />
                <Radar name="E" dataKey="E" stroke="#34d399" fill="#34d399" fillOpacity={0.15} />
                <Radar name="S" dataKey="S" stroke="#60a5fa" fill="#60a5fa" fillOpacity={0.1} />
                <Radar name="G" dataKey="G" stroke="#fbbf24" fill="#fbbf24" fillOpacity={0.1} />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </Card>
          <Card>
            <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 12, color: 'var(--text)' }}>
              High Coal Exposure Flags
            </div>
            {ESG_SCORES.filter(d => d.coal > 0).map(d => (
              <div key={d.ticker} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
                <div>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--text)' }}>{d.ticker}</span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text3)', marginLeft: 8 }}>{d.name}</span>
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: d.coal > 90 ? 'var(--red)' : 'var(--amber)' }}>
                  {d.coal}% coal exposure
                </span>
              </div>
            ))}
          </Card>
        </div>
      </div>
    </section>
  )
}

// ─── SECTION: PRODUCT TAXONOMY ────────────────────────────────────────────────
function TaxonomySection() {
  const products = [
    { name: 'Green Project Finance', family: 'Use of Proceeds', fit: 'Renewables, Storage, Grid', tenor: '10–18yr', hard: 'Medium', color: '#34d399' },
    { name: 'Green Corporate Term Loan', family: 'Use of Proceeds', fit: 'Corporates, Retrofit', tenor: '3–7yr', hard: 'Medium', color: '#2dd4bf' },
    { name: 'Green Bond', family: 'Use of Proceeds', fit: 'Investment-grade, Refinancing', tenor: '5–12yr', hard: 'Low', color: '#60a5fa' },
    { name: 'Sustainability-Linked Loan', family: 'SLL', fit: 'General corporate + KPI', tenor: '3–7yr', hard: 'High', color: '#fbbf24' },
    { name: 'Transition Finance Loan', family: 'Transition', fit: 'Steel, Cement, Chemicals', tenor: '5–12yr', hard: 'High', color: '#fb923c' },
    { name: 'Blended Finance (DFI+)', family: 'Blended', fit: 'Early tech, New markets', tenor: '7–15yr', hard: 'High', color: '#a78bfa' },
    { name: 'Carbon / Results-Based', family: 'Carbon', fit: 'Efficiency, Nature, Early', tenor: '1–10yr', hard: 'High', color: '#e879f9' },
    { name: 'Green Securitisation', family: 'Structured', fit: 'Rooftop solar, EV pools', tenor: '3–8yr', hard: 'Low', color: '#38bdf8' },
  ]

  return (
    <section style={{ marginBottom: 48 }}>
      <SectionTitle sub="sustainable finance instrument taxonomy · tenor · hard-to-abate fit">
        Product Taxonomy · Financing Instruments
      </SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {products.map(p => (
          <Card key={p.name} style={{ padding: '14px 16px', borderLeft: `3px solid ${p.color}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
              <span style={{ fontFamily: 'var(--font-head)', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text)' }}>{p.name}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: p.color, background: p.color + '18', padding: '2px 6px', borderRadius: 4 }}>
                {p.family}
              </span>
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)', marginBottom: 8 }}>{p.fit}</div>
            <div style={{ display: 'flex', gap: 10 }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text3)' }}>
                Tenor: <span style={{ color: 'var(--text2)' }}>{p.tenor}</span>
              </span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text3)' }}>
                H2A: <span style={{ color: p.hard === 'High' ? 'var(--amber)' : 'var(--text3)' }}>{p.hard}</span>
              </span>
            </div>
          </Card>
        ))}
      </div>
    </section>
  )
}

// ─── SECTION: REPO / WORKFLOW ─────────────────────────────────────────────────
function RepoSection() {
  const labelColor = (l) => LABEL_COLORS[l] || '#8faaa5'

  return (
    <section style={{ marginBottom: 48 }}>
      <SectionTitle sub="GitHub · DogInfantry/sustainable-finance-india-transition">
        Research Workflow · Repository Status
      </SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <Card>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, color: 'var(--text)' }}>Open Issues</div>
            <a href="https://github.com/DogInfantry/sustainable-finance-india-transition/issues" target="_blank" rel="noreferrer"
              style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'var(--green)', fontSize: 11, fontFamily: 'var(--font-mono)', textDecoration: 'none' }}>
              View on GitHub <ExternalLink size={11} />
            </a>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {ISSUES.map(issue => (
              <div key={issue.id} style={{ padding: '10px 12px', background: 'var(--bg2)', borderRadius: 6, borderLeft: '2px solid var(--border-hi)' }}>
                <div style={{ display: 'flex', gap: 8, marginBottom: 6 }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)' }}>#{issue.id}</span>
                  <span style={{ fontFamily: 'var(--font-body)', fontSize: 12, color: 'var(--text)' }}>{issue.title}</span>
                </div>
                <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                  {issue.labels.map(l => (
                    <span key={l} style={{
                      fontFamily: 'var(--font-mono)', fontSize: 10, padding: '2px 6px', borderRadius: 3,
                      color: labelColor(l), background: labelColor(l) + '18'
                    }}>{l}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <Card>
            <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 14, color: 'var(--text)' }}>
              Recent Commits
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {COMMITS.map(c => (
                <div key={c.sha} style={{ display: 'flex', gap: 10, padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--green)', minWidth: 56 }}>{c.sha}</span>
                  <div>
                    <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text)', marginBottom: 2 }}>{c.msg}</div>
                    <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text3)' }}>{c.date}</div>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 14, color: 'var(--text)' }}>
              Repository Structure
            </div>
            {[
              { path: 'src/', desc: 'Core Python models (ESG spread, VaR, DCF, taxonomy)', icon: '⚙️', color: 'var(--teal)' },
              { path: 'data/', desc: 'Synthetic datasets: green bonds, ESG, climate scenarios', icon: '📊', color: 'var(--green)' },
              { path: 'reports/', desc: 'Roadmap, product mapping, bank views', icon: '📄', color: 'var(--blue)' },
              { path: 'notebooks/', desc: 'Jupyter notebooks (planned v1.1+)', icon: '📓', color: 'var(--purple)' },
              { path: 'tests/', desc: 'pytest coverage for core models', icon: '🧪', color: 'var(--amber)' },
            ].map(item => (
              <div key={item.path} style={{ display: 'flex', gap: 10, padding: '8px 0', borderBottom: '1px solid var(--border)', alignItems: 'flex-start' }}>
                <span style={{ fontSize: 14 }}>{item.icon}</span>
                <div>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: item.color }}>{item.path}</span>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text3)', marginTop: 2 }}>{item.desc}</div>
                </div>
              </div>
            ))}
          </Card>

          <Card>
            <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 600, marginBottom: 12, color: 'var(--text)' }}>Repo Topics</div>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {['carbon-markets', 'climate-finance', 'climate-policy', 'esg', 'green-bonds-analysis', 'india-energy-transition', 'sustainable-finance', 'taxonomy'].map(t => (
                <span key={t} style={{
                  fontFamily: 'var(--font-mono)', fontSize: 10, padding: '4px 8px',
                  background: 'var(--bg3)', color: 'var(--green)', border: '1px solid var(--border-hi)',
                  borderRadius: 20, letterSpacing: '0.03em'
                }}>{t}</span>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </section>
  )
}

// ─── SECTION: POLICY FRAMEWORK ────────────────────────────────────────────────
function PolicySection() {
  const policies = [
    { body: 'SEBI', instrument: 'BRSR Core Mandate', year: 2023, status: 'Active', impact: 'High', desc: 'Top 150 listed cos. mandatory Business Responsibility & Sustainability Reporting' },
    { body: 'SEBI', instrument: 'Green/SLB Framework', year: 2021, status: 'Active', impact: 'High', desc: 'Listing requirements for labelled bonds; use-of-proceeds + SPT disclosures' },
    { body: 'RBI', instrument: 'Climate Risk Framework', year: 2023, status: 'Consultation', impact: 'Medium', desc: 'Draft guidance on climate-related financial risks; capital impact TBD' },
    { body: 'GoI', instrument: 'Sovereign Green Bonds', year: 2023, status: 'Active', impact: 'High', desc: '₹44,000Cr issued; establishes sovereign yield curve for green pricing' },
    { body: 'NITI Aayog', instrument: 'Low Carbon Dev. Strategy', year: 2022, status: 'Published', impact: 'Medium', desc: 'Net Zero 2070 roadmap; sectoral transition pathways and investment needs' },
    { body: 'MoEFCC', instrument: 'Carbon Credit Trading', year: 2023, status: 'Developing', impact: 'High', desc: 'CCTS framework; domestic carbon market; BEE-linked credit issuance' },
  ]

  const impactColor = { High: 'var(--green)', Medium: 'var(--amber)', Low: 'var(--text3)' }
  const statusColor = { Active: 'var(--green)', Consultation: 'var(--amber)', Developing: 'var(--blue)', Published: 'var(--teal)' }

  return (
    <section style={{ marginBottom: 48 }}>
      <SectionTitle sub="SEBI · RBI · NITI Aayog · MoEFCC regulatory landscape">
        Policy & Regulatory Framework
      </SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 12 }}>
        {policies.map(p => (
          <Card key={p.instrument} style={{ padding: '14px 16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
              <div>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text3)', marginRight: 6 }}>{p.body} ·</span>
                <span style={{ fontFamily: 'var(--font-head)', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text)' }}>{p.instrument}</span>
              </div>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: statusColor[p.status], background: statusColor[p.status] + '18', padding: '2px 7px', borderRadius: 4 }}>
                {p.status}
              </span>
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)', marginBottom: 8, lineHeight: 1.5 }}>{p.desc}</div>
            <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text3)' }}>Since {p.year}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: impactColor[p.impact] }}>● {p.impact} Impact</span>
            </div>
          </Card>
        ))}
      </div>
    </section>
  )
}

// ─── NAVIGATION ──────────────────────────────────────────────────────────────
const TABS = [
  { id: 'overview', label: 'Overview', icon: Activity },
  { id: 'capital', label: 'Capital', icon: BarChart2 },
  { id: 'emissions', label: 'Emissions', icon: Globe },
  { id: 'esg', label: 'ESG', icon: Leaf },
  { id: 'taxonomy', label: 'Products', icon: Shield },
  { id: 'policy', label: 'Policy', icon: CheckCircle2 },
  { id: 'repo', label: 'Repo', icon: GitBranch },
]

// ─── APP ──────────────────────────────────────────────────────────────────────
export default function App() {
  const [activeTab, setActiveTab] = useState('overview')
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)' }}>
      {/* Header */}
      <header style={{
        position: 'sticky', top: 0, zIndex: 100,
        background: scrolled ? 'rgba(6,10,14,0.95)' : 'transparent',
        backdropFilter: 'blur(12px)',
        borderBottom: scrolled ? '1px solid var(--border)' : '1px solid transparent',
        transition: 'all 0.3s',
        padding: '0 24px',
      }}>
        <div style={{ maxWidth: 1400, margin: '0 auto', display: 'flex', alignItems: 'center', gap: 24, height: 60 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{ width: 28, height: 28, borderRadius: 6, background: 'linear-gradient(135deg, var(--green), var(--teal))', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Leaf size={14} color="#060a0e" />
            </div>
            <div>
              <div style={{ fontFamily: 'var(--font-head)', fontSize: '0.9rem', fontWeight: 700, color: 'var(--text)', lineHeight: 1.1 }}>India Transition Finance</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--text3)', lineHeight: 1 }}>DogInfantry / sustainable-finance-india-transition</div>
            </div>
          </div>

          <nav style={{ display: 'flex', gap: 2, marginLeft: 16, flex: 1 }}>
            {TABS.map(tab => {
              const Icon = tab.icon
              const active = activeTab === tab.id
              return (
                <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{
                  display: 'flex', alignItems: 'center', gap: 5, padding: '6px 12px',
                  borderRadius: 6, border: 'none', cursor: 'pointer', transition: 'all .2s',
                  background: active ? 'var(--bg3)' : 'transparent',
                  color: active ? 'var(--green)' : 'var(--text3)',
                  fontFamily: 'var(--font-mono)', fontSize: 11
                }}>
                  <Icon size={12} /> {tab.label}
                </button>
              )
            })}
          </nav>

          <a href="https://github.com/DogInfantry/sustainable-finance-india-transition" target="_blank" rel="noreferrer"
            style={{ display: 'flex', alignItems: 'center', gap: 5, color: 'var(--text3)', fontSize: 11, fontFamily: 'var(--font-mono)', textDecoration: 'none', transition: 'color .2s' }}
            onMouseEnter={e => e.currentTarget.style.color = 'var(--green)'}
            onMouseLeave={e => e.currentTarget.style.color = 'var(--text3)'}>
            <ExternalLink size={12} /> GitHub
          </a>
        </div>
      </header>

      {/* Hero strip */}
      <div style={{
        background: 'linear-gradient(180deg, rgba(52,211,153,0.04) 0%, transparent 100%)',
        borderBottom: '1px solid var(--border)',
        padding: '28px 24px 24px',
      }}>
        <div style={{ maxWidth: 1400, margin: '0 auto' }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--green)', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 8 }}>
            Research Dashboard · v1.0 · Synthetic Data
          </div>
          <h1 style={{ fontFamily: 'var(--font-head)', fontSize: 'clamp(1.6rem, 4vw, 2.6rem)', fontWeight: 800, color: 'var(--text)', lineHeight: 1.15, letterSpacing: '-0.02em', maxWidth: 700, marginBottom: 10 }}>
            India's Sustainable Finance<br />
            <span style={{ color: 'var(--green)' }}>Transition</span> — Data & Frameworks
          </h1>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: 13, color: 'var(--text2)', maxWidth: 600, lineHeight: 1.6 }}>
            Green bonds · ESG integration · SEBI/RBI policy frameworks · Climate risk in Indian capital markets · Transition finance for hard-to-abate sectors
          </p>
        </div>
      </div>

      {/* Main content */}
      <main style={{ maxWidth: 1400, margin: '0 auto', padding: '32px 24px' }}>
        {activeTab === 'overview' && <OverviewSection />}
        {activeTab === 'capital' && <CapitalSection />}
        {activeTab === 'emissions' && <EmissionsSection />}
        {activeTab === 'esg' && <ESGSection />}
        {activeTab === 'taxonomy' && <TaxonomySection />}
        {activeTab === 'policy' && <PolicySection />}
        {activeTab === 'repo' && <RepoSection />}
      </main>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid var(--border)', padding: '20px 24px', marginTop: 24 }}>
        <div style={{ maxWidth: 1400, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)' }}>
            © 2026 · Anklesh Rawat · IIM Bodh Gaya · MIT License · All data is synthetic / illustrative
          </div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text3)' }}>
            Powered by React + Recharts · Deployed on Vercel
          </div>
        </div>
      </footer>
    </div>
  )
}
