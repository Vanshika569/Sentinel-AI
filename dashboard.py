import base64
import html
import json
import math
import os
import time
from datetime import datetime
from types import SimpleNamespace

import psutil
import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------
# SentinelAI — AI-Powered SRE Incident Commander
# Enterprise dashboard: 3D system model, live host metrics,
# safe rule-based guidance. Monitoring logic is unchanged.
# ------------------------------------------------------------

st.set_page_config(
    page_title="SentinelAI | Incident Commander",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg: #070b14;
        --line: rgba(255,255,255,.08);
        --line-2: rgba(255,255,255,.14);
        --text: #e8edf7;
        --muted: #9aa8bf;
        --faint: #6b7a93;
        --ind: #6366f1;
        --ind-l: #a5b4fc;
        --vio: #8b5cf6;
        --sky: #38bdf8;
        --ok: #34d399;
        --warn: #fbbf24;
        --crit: #fb7185;
    }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(900px 520px at 6% -6%, rgba(99,102,241,.24), transparent 60%),
            radial-gradient(820px 540px at 100% 4%, rgba(139,92,246,.17), transparent 55%),
            radial-gradient(720px 520px at 50% 112%, rgba(56,189,248,.09), transparent 60%),
            var(--bg);
        color: var(--text);
    }
    .stApp:before {
        content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
        background-image:
            linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
        background-size: 56px 56px;
        -webkit-mask-image: radial-gradient(ellipse at 50% 0%, #000 0%, transparent 68%);
        mask-image: radial-gradient(ellipse at 50% 0%, #000 0%, transparent 68%);
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1400px; padding-top: 1.2rem; padding-bottom: 3rem; }
    #MainMenu, footer { visibility: hidden; }

    .stMarkdown p, .stMarkdown li, label, .stText { color: var(--text); font-size: 1rem; line-height: 1.7; }
    h1, h2, h3, h4 { font-family: 'Sora', sans-serif; color: var(--text); letter-spacing: -.02em; }
    [data-testid="stCaptionContainer"] p { color: var(--muted) !important; font-size: .9rem !important; }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1120 0%, #080d19 100%);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div { padding-top: 1.2rem; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown p { color: #d5deec !important; font-size: .95rem !important; }
    [data-testid="stSidebar"] hr { border-color: var(--line); }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: .55rem .75rem; border-radius: 10px; border: 1px solid transparent; transition: background .15s;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover { background: rgba(255,255,255,.05); }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(90deg, rgba(99,102,241,.25), rgba(99,102,241,.06));
        border-color: rgba(129,140,248,.4);
    }
    .brand { display: flex; align-items: center; gap: .75rem; margin-bottom: 1.5rem; }
    .brand-logo {
        width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        box-shadow: 0 8px 22px rgba(99,102,241,.45), inset 0 1px 0 rgba(255,255,255,.3);
    }
    .brand-name { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.2rem; letter-spacing: -.02em; color: #fff; }
    .brand-sub { font-size: .68rem; letter-spacing: .16em; text-transform: uppercase; color: var(--faint); margin-top: .1rem; }
    .side-label { font-size: .72rem; letter-spacing: .16em; text-transform: uppercase; color: var(--faint); font-weight: 600; margin: .3rem 0 .5rem; }
    .safety {
        border: 1px solid rgba(52,211,153,.28); background: rgba(52,211,153,.06);
        border-radius: 12px; padding: .85rem .95rem; font-size: .88rem; line-height: 1.55; color: #bcd0c8;
    }
    .safety b { color: var(--ok); font-size: .72rem; letter-spacing: .12em; }

    /* ---------- Top bar ---------- */
    .topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.1rem; }
    .crumbs { color: var(--muted); font-size: .92rem; }
    .crumbs b { color: var(--text); font-weight: 600; }
    .crumbs span { margin: 0 .45rem; color: var(--faint); }
    .top-right { display: flex; align-items: center; gap: .8rem; }
    .live {
        display: inline-flex; align-items: center; gap: .5rem; padding: .35rem .75rem; border-radius: 999px;
        background: rgba(52,211,153,.1); border: 1px solid rgba(52,211,153,.3);
        color: var(--ok); font-size: .76rem; font-weight: 700; letter-spacing: .08em;
    }
    .live i { width: 7px; height: 7px; border-radius: 50%; background: var(--ok); animation: pulse 2s infinite; }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(52,211,153,.6); }
        70% { box-shadow: 0 0 0 8px rgba(52,211,153,0); }
        100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
    }
    .clock { font-family: 'JetBrains Mono', monospace; font-size: .85rem; color: var(--muted); }

    /* ---------- Hero ---------- */
    .kicker { display: flex; align-items: center; gap: .6rem; font-size: .8rem; letter-spacing: .18em; text-transform: uppercase; font-weight: 700; color: var(--ind-l); margin-bottom: .9rem; }
    .kicker i { width: 28px; height: 2px; background: linear-gradient(90deg, var(--ind), transparent); display: inline-block; }
    .hero-h {
        font-family: 'Sora', sans-serif; font-weight: 800; letter-spacing: -.045em; line-height: 1.04;
        font-size: clamp(2.3rem, 4vw, 3.7rem); margin: 0; color: #fff;
    }
    .grad { background: linear-gradient(100deg, #818cf8 0%, #c084fc 55%, #38bdf8 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
    .hero-p { color: var(--muted); font-size: 1.08rem; line-height: 1.65; max-width: 540px; margin: 1rem 0 1.3rem; }

    .banner {
        --rgb: 52,211,153; --tone: #34d399;
        display: flex; align-items: center; justify-content: space-between; gap: 1rem;
        padding: 1rem 1.15rem; border-radius: 16px;
        background: linear-gradient(135deg, rgba(var(--rgb), .14), rgba(var(--rgb), .04));
        border: 1px solid rgba(var(--rgb), .35);
        box-shadow: 0 10px 40px rgba(var(--rgb), .10), inset 0 1px 0 rgba(255,255,255,.06);
    }
    .banner.warn { --rgb: 251,191,36; --tone: #fbbf24; }
    .banner.crit { --rgb: 251,113,133; --tone: #fb7185; }
    .banner-l { display: flex; align-items: center; gap: .9rem; }
    .banner-ic {
        width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
        background: rgba(var(--rgb), .18); color: var(--tone); font-weight: 800; font-size: 1.2rem;
    }
    .banner-t { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.08rem; }
    .banner-s { color: #c3cee0; font-size: .92rem; line-height: 1.5; margin-top: .15rem; }
    .banner-tag { font-size: .72rem; font-weight: 800; letter-spacing: .1em; color: var(--tone); background: rgba(var(--rgb), .15); padding: .4rem .65rem; border-radius: 8px; white-space: nowrap; }

    .stats { display: flex; gap: .8rem; margin-top: 1rem; }
    .stat { flex: 1; padding: .8rem 1rem; border-radius: 14px; background: rgba(255,255,255,.035); border: 1px solid var(--line); }
    .stat-v { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.35rem; color: #fff; }
    .stat-l { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--faint); margin-top: .15rem; font-weight: 600; }

    /* ---------- Section heading ---------- */
    .sec { display: flex; align-items: baseline; gap: .9rem; margin: 2rem 0 1rem; }
    .sec h3 { font-size: 1.3rem; font-weight: 700; margin: 0; }
    .sec span { color: var(--muted); font-size: .9rem; }
    .sec:after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, var(--line-2), transparent); transform: translateY(-4px); }

    /* ---------- Metric cards (3D tilt on hover) ---------- */
    .rcard-wrap { perspective: 1100px; }
    .rcard {
        position: relative; padding: 1.15rem 1.25rem 1rem; border-radius: 20px;
        background: linear-gradient(160deg, rgba(30,41,66,.82), rgba(14,21,38,.88));
        border: 1px solid var(--line);
        box-shadow: 0 24px 50px -18px rgba(0,0,0,.65), inset 0 1px 0 rgba(255,255,255,.07);
        transition: transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s, border-color .35s;
        transform-style: preserve-3d;
    }
    .rcard:before {
        content: ""; position: absolute; left: 18px; right: 18px; top: 0; height: 1px;
        background: linear-gradient(90deg, transparent, var(--c1, #818cf8), transparent); opacity: .9;
    }
    .rcard:hover {
        transform: rotateX(4deg) rotateY(-5deg) translateY(-6px);
        border-color: var(--line-2);
        box-shadow: 0 34px 60px -16px rgba(0,0,0,.75), 0 0 40px -10px var(--c1, #6366f1), inset 0 1px 0 rgba(255,255,255,.1);
    }
    .rc-top { display: flex; justify-content: space-between; align-items: center; }
    .rc-name { font-family: 'Sora', sans-serif; font-weight: 600; font-size: 1.05rem; }
    .rc-tag { font-family: 'JetBrains Mono', monospace; font-size: .72rem; color: var(--muted); border: 1px solid var(--line-2); border-radius: 6px; padding: .12rem .45rem; letter-spacing: .08em; }
    .rc-body { display: flex; align-items: center; gap: 1.1rem; margin: .7rem 0 .5rem; }
    .ring-wrap { position: relative; width: 138px; height: 138px; flex-shrink: 0; filter: drop-shadow(0 10px 18px rgba(0,0,0,.45)); }
    .ring-wrap img { width: 100%; height: 100%; display: block; }
    .ring-num { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.85rem; color: #fff; }
    .ring-num small { font-size: .85rem; color: var(--muted); margin-left: 2px; margin-top: .55rem; font-weight: 600; }
    .rc-info { min-width: 0; }
    .chip { display: inline-block; padding: .22rem .65rem; border-radius: 999px; font-size: .72rem; font-weight: 700; letter-spacing: .06em; }
    .chip.ok { background: rgba(52,211,153,.14); color: var(--ok); }
    .chip.warn { background: rgba(251,191,36,.14); color: var(--warn); }
    .chip.crit { background: rgba(251,113,133,.15); color: var(--crit); }
    .rc-foot { color: #c3cee0; font-size: .95rem; margin-top: .6rem; line-height: 1.45; }
    .rc-delta { color: var(--faint); font-size: .82rem; margin-top: .3rem; font-family: 'JetBrains Mono', monospace; }
    .rc-spark { border-top: 1px solid var(--line); padding-top: .65rem; margin-top: .3rem; }
    .rc-spark img { width: 100%; height: 48px; display: block; }
    .rc-cap { display: flex; justify-content: space-between; font-size: .72rem; color: var(--faint); letter-spacing: .08em; text-transform: uppercase; margin-top: .35rem; font-weight: 600; }

    /* ---------- Panels ---------- */
    .panel {
        padding: 1.2rem 1.35rem; border-radius: 20px; height: 100%;
        background: linear-gradient(160deg, rgba(26,36,58,.78), rgba(13,20,36,.85));
        border: 1px solid var(--line);
        box-shadow: 0 18px 40px -20px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.05);
    }
    .panel-t { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.12rem; }
    .panel-d { color: var(--muted); font-size: .92rem; margin: .15rem 0 .9rem; }
    .sig { display: flex; gap: .85rem; padding: .8rem 0; border-top: 1px solid var(--line); }
    .sig:first-of-type { border-top: 0; }
    .sig-ic { width: 28px; height: 28px; border-radius: 8px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: .85rem; }
    .sig.ok .sig-ic { background: rgba(52,211,153,.15); color: var(--ok); }
    .sig.warn .sig-ic { background: rgba(251,191,36,.15); color: var(--warn); }
    .sig.crit .sig-ic { background: rgba(251,113,133,.15); color: var(--crit); }
    .sig-t { font-size: 1rem; line-height: 1.55; }
    .sig-s { color: var(--muted); font-size: .86rem; margin-top: .1rem; }
    .step { display: flex; gap: .9rem; padding: .8rem 0; border-top: 1px solid var(--line); font-size: 1rem; line-height: 1.6; }
    .step:first-of-type { border-top: 0; }
    .step-n { font-family: 'JetBrains Mono', monospace; font-weight: 600; color: var(--ind-l); padding-top: .1rem; }
    .fine { color: var(--faint); font-size: .84rem; margin-top: .9rem; line-height: 1.5; }

    /* ---------- Tables ---------- */
    table.tbl { width: 100%; border-collapse: collapse; border: 0 !important; }
    table.tbl th, table.tbl td {
        border-left: 0 !important; border-right: 0 !important; border-top: 0 !important;
        background: transparent !important; white-space: nowrap;
    }
    table.tbl th { text-align: left; color: var(--faint); font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; font-weight: 600; padding: .35rem .5rem .6rem; border-bottom: 1px solid var(--line-2) !important; }
    table.tbl td { padding: .65rem .5rem; border-bottom: 1px solid var(--line) !important; font-size: .95rem; }
    table.tbl tr:last-child td { border-bottom: 0 !important; }
    table.tbl td.mono, .mono { font-family: 'JetBrains Mono', monospace; font-size: .88rem; color: #c3cee0; }
    .pname { font-weight: 600; max-width: 130px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .bar { display: inline-block; width: 34px; height: 6px; border-radius: 6px; background: rgba(255,255,255,.08); vertical-align: middle; margin-right: .45rem; overflow: hidden; }
    .panel { overflow-x: auto; }
    .st-key-incident_panel, .st-key-runbook_panel {
        padding: 1.3rem 1.5rem; border-radius: 20px; border: 1px solid var(--line);
        background: linear-gradient(160deg, rgba(26,36,58,.78), rgba(13,20,36,.85));
        box-shadow: 0 18px 40px -20px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.05);
    }
    .bar i { display: block; height: 100%; border-radius: 6px; background: linear-gradient(90deg, #6366f1, #a78bfa); }

    /* ---------- Streamlit widgets ---------- */
    div.stButton > button {
        border-radius: 12px !important; border: 1px solid rgba(165,180,252,.45) !important;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important; color: #fff !important;
        font-weight: 600 !important; font-size: 1rem !important; min-height: 48px;
        box-shadow: 0 10px 26px -8px rgba(99,102,241,.7), inset 0 1px 0 rgba(255,255,255,.25);
        transition: transform .15s, box-shadow .15s, filter .15s;
    }
    div.stButton > button p { color: #fff !important; font-weight: 600 !important; }
    div.stButton > button:hover { transform: translateY(-2px); filter: brightness(1.08); box-shadow: 0 14px 30px -8px rgba(99,102,241,.85), inset 0 1px 0 rgba(255,255,255,.3); }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(160deg, rgba(26,36,58,.78), rgba(13,20,36,.85));
        border: 1px solid var(--line) !important; border-radius: 20px; padding: .6rem .9rem;
        box-shadow: 0 18px 40px -20px rgba(0,0,0,.6);
    }
    [data-testid="stAlert"] { background: rgba(255,255,255,.045) !important; border: 1px solid var(--line-2); border-radius: 12px; }
    [data-testid="stAlert"] * { color: var(--text) !important; }
    [data-testid="stCode"] pre, code { background: #0c1424 !important; color: #dbe4f5 !important; border-radius: 8px; }
    [data-testid="stExpander"] { border: 1px solid var(--line) !important; border-radius: 12px; background: rgba(255,255,255,.02); }
    [data-testid="stExpander"] * { color: var(--text); }
    iframe { border: 0; border-radius: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Helpers (monitoring logic) ----------
def fmt_uptime(seconds):
    seconds = int(max(0, seconds))
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def get_system_metrics():
    """Read live CPU, memory, disk, uptime and top processes from this machine."""
    procs = []
    try:
        for p in psutil.process_iter(["pid", "name"]):
            try:
                p.cpu_percent(None)  # prime per-process CPU counters
                procs.append(p)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        procs = []

    cpu = psutil.cpu_percent(interval=0.3)
    memory = psutil.virtual_memory()
    disk_root = os.path.abspath(os.sep)
    disk = psutil.disk_usage(disk_root)
    cores = psutil.cpu_count(logical=True) or 1

    top = []
    for p in procs:
        try:
            name = (p.info.get("name") or "unknown")
            if p.pid == 0 or "idle" in name.lower():
                continue
            top.append({"pid": p.pid, "name": name, "cpu": p.cpu_percent(None) / cores, "mem": p.memory_percent()})
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
            continue
    top.sort(key=lambda r: (r["cpu"], r["mem"]), reverse=True)

    try:
        uptime = time.time() - psutil.boot_time()
    except Exception:
        uptime = 0

    return {
        "cpu": float(cpu),
        "memory": float(memory.percent),
        "memory_used_gb": memory.used / (1024 ** 3),
        "memory_total_gb": memory.total / (1024 ** 3),
        "disk": float(disk.percent),
        "disk_used_gb": disk.used / (1024 ** 3),
        "disk_total_gb": disk.total / (1024 ** 3),
        "disk_root": disk_root,
        "cores": cores,
        "uptime": uptime,
        "process_count": len(procs),
        "top_procs": top[:6],
    }


def get_severity(metrics):
    """Simple MVP thresholds; these are indicators, not production alert rules."""
    values = [metrics["cpu"], metrics["memory"], metrics["disk"]]
    if any(value >= 90 for value in values):
        return "CRITICAL"
    if any(value >= 75 for value in values):
        return "WARNING"
    return "HEALTHY"


def get_problems(metrics):
    problems = []
    if metrics["cpu"] >= 75:
        problems.append(f"High CPU usage detected: {metrics['cpu']:.1f}%")
    if metrics["memory"] >= 75:
        problems.append(f"High memory usage detected: {metrics['memory']:.1f}%")
    if metrics["disk"] >= 85:
        problems.append(f"High disk usage detected: {metrics['disk']:.1f}%")
    return problems


def get_recommendations(problems):
    recommendations = []
    for problem in problems:
        lower = problem.lower()
        if "cpu" in lower:
            recommendations.append(
                "Inspect the highest-CPU processes and check for unexpected workload spikes."
            )
        elif "memory" in lower:
            recommendations.append(
                "Review memory-heavy processes and check application logs for possible memory leaks."
            )
        elif "disk" in lower:
            recommendations.append(
                "Identify large files and old logs; confirm retention rules before removing anything."
            )
    if not recommendations:
        recommendations.append(
            "No threshold breach detected. Keep monitoring and review application-level logs if users report issues."
        )
    return recommendations


def try_get_runbook(problems):
    """Use the project's keyword runbook retriever when available."""
    if not problems:
        return None
    try:
        from app.runbook_retriever import RunbookRetriever
        retriever = RunbookRetriever()
        incident = SimpleNamespace(problems=problems)
        result = retriever.retrieve_runbook(incident)
        if result and result != "No relevant runbook found.":
            return result
    except Exception:
        return None
    return None


def run_sentinelai_agents():
    """Run the existing project pipeline on demand from the dashboard."""
    from app.services.system_monitor import System_monitor
    from app.agents.alertagent import AlertAgent
    from app.agents.diagnosis_agent import DiagnosisAgent
    from app.agents.recovery_agent import RecoveryAgent

    monitor = System_monitor()
    monitored_metrics = monitor.get_metrices()
    incident = AlertAgent().execute(monitored_metrics)

    diagnosis = None
    diagnosis_error = None
    try:
        diagnosis = DiagnosisAgent().execute(incident)
    except Exception as exc:
        diagnosis_error = str(exc)

    recommendations = RecoveryAgent().execute(incident)
    return incident, diagnosis, diagnosis_error, recommendations


# ---------- Helpers (visuals) ----------
def esc(text):
    return html.escape(str(text))


def tone_of(value):
    if value >= 90:
        return "crit"
    if value >= 75:
        return "warn"
    return "ok"


RES_GRAD = {"cpu": ("#6366f1", "#a5b4fc"), "memory": ("#8b5cf6", "#d8b4fe"), "disk": ("#0ea5e9", "#7dd3fc")}
TONE_GRAD = {"warn": ("#f59e0b", "#fde68a"), "crit": ("#f43f5e", "#fda4af")}
RES_HEX = {"cpu": "#818cf8", "memory": "#a78bfa", "disk": "#38bdf8"}
TONE_HEX = {"warn": "#fbbf24", "crit": "#fb7185"}


def grad_for(key, tone):
    return TONE_GRAD.get(tone, RES_GRAD[key])


def svg_img(svg, cls=""):
    """Embed an SVG as an <img> so it renders reliably inside st.markdown."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f'<img class="{cls}" alt="" src="data:image/svg+xml;base64,{b64}"/>'


def ring_svg(key, value, tone):
    c1, c2 = grad_for(key, tone)
    v = max(0.0, min(100.0, value))
    ticks = ""
    for pct, col in ((75, "#fbbf24"), (90, "#fb7185")):
        ang = math.radians(-90 + pct * 3.6)
        x1, y1 = 70 + 60 * math.cos(ang), 70 + 60 * math.sin(ang)
        x2, y2 = 70 + 67 * math.cos(ang), 70 + 67 * math.sin(ang)
        ticks += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="2.5" stroke-linecap="round" opacity=".9"/>'
    progress = ""
    if v > 0.4:
        progress = (
            f'<circle cx="70" cy="70" r="50" fill="none" stroke="url(#g)" stroke-width="11" stroke-linecap="round" '
            f'pathLength="100" stroke-dasharray="{v:.2f} 100" transform="rotate(-90 70 70)" filter="url(#glow)"/>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 140">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
        '<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<radialGradient id="face" cx="50%" cy="40%" r="65%"><stop offset="0" stop-color="#1b2744"/><stop offset="1" stop-color="#0c1322"/></radialGradient></defs>'
        '<circle cx="70" cy="70" r="40" fill="url(#face)" stroke="rgba(255,255,255,.07)" stroke-width="1"/>'
        '<circle cx="70" cy="70" r="50" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="11"/>'
        + progress + ticks + "</svg>"
    )


def spark_svg(values, tone_key, tone):
    c1, c2 = grad_for(tone_key, tone)
    w, h = 300, 48
    if len(values) < 2:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
            f'<line x1="0" y1="{h - 8}" x2="{w}" y2="{h - 8}" stroke="{c1}" stroke-opacity=".55" stroke-width="2" stroke-dasharray="4 6" vector-effect="non-scaling-stroke"/></svg>'
        )
    lo, hi = min(values), max(values)
    span = max(hi - lo, 10.0)
    mid = (hi + lo) / 2
    lo, hi = mid - span / 2, mid + span / 2
    step = w / (len(values) - 1)
    pts = [(i * step, (h - 6) - ((v - lo) / (hi - lo)) * (h - 12)) for i, v in enumerate(values)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"0,{h} {line} {w},{h}"
    lx, ly = pts[-1]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
        f'<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".38"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></linearGradient></defs>'
        f'<polygon points="{area}" fill="url(#a)"/>'
        f'<polyline points="{line}" fill="none" stroke="{c2}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>'
        f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3.2" fill="{c2}" vector-effect="non-scaling-stroke"/></svg>'
    )


def resource_card(key, label, tag, value, foot, series):
    tone = tone_of(value)
    c1, _ = grad_for(key, tone)
    status = {"ok": "NORMAL", "warn": "ELEVATED", "crit": "CRITICAL"}[tone]
    delta = ""
    if len(series) >= 2:
        d = series[-1] - series[-2]
        arrow = "▲" if d > 0.05 else ("▼" if d < -0.05 else "■")
        delta = f'<div class="rc-delta">{arrow} {abs(d):.1f} pts</div>'
    return (
        f'<div class="rcard-wrap"><div class="rcard" style="--c1:{c1}">'
        f'<div class="rc-top"><div class="rc-name">{label}</div><div class="rc-tag">{tag}</div></div>'
        f'<div class="rc-body"><div class="ring-wrap">{svg_img(ring_svg(key, value, tone))}'
        f'<div class="ring-num">{value:.0f}<small>%</small></div></div>'
        f'<div class="rc-info"><span class="chip {tone}">{status}</span>'
        f'<div class="rc-foot">{esc(foot)}</div>{delta}</div></div>'
        f'<div class="rc-spark">{svg_img(spark_svg(series, key, tone))}'
        f'<div class="rc-cap"><span>Last {len(series)} checks</span><span>Warn 75 · Crit 90</span></div></div>'
        f'</div></div>'
    )


def build_scene(metrics, severity):
    """HTML page with a canvas-based 3D model: one orbit ring per resource."""
    sev_color = {"HEALTHY": "#34d399", "WARNING": "#fbbf24", "CRITICAL": "#fb7185"}[severity]

    def ring_color(key, v):
        return TONE_HEX.get(tone_of(v), RES_HEX[key])

    data = {
        "sev": severity,
        "sevColor": sev_color,
        "rings": [
            {"name": "CPU", "v": round(metrics["cpu"], 1), "r": 1.22, "a": 0.35, "b": 0.15, "color": ring_color("cpu", metrics["cpu"])},
            {"name": "MEM", "v": round(metrics["memory"], 1), "r": 1.0, "a": 1.05, "b": -0.55, "color": ring_color("memory", metrics["memory"])},
            {"name": "DISK", "v": round(metrics["disk"], 1), "r": 0.8, "a": -0.9, "b": 0.7, "color": ring_color("disk", metrics["disk"])},
        ],
    }
    template = """<!doctype html><html><head><meta charset="utf-8">
<style>html,body{margin:0;height:100%;background:transparent;overflow:hidden}canvas{display:block;width:100%;height:100%}</style>
</head><body><canvas id="c"></canvas><script>
(function(){
var D=__DATA__;
var cv=document.getElementById('c'),ctx=cv.getContext('2d');
var W=0,H=0;
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function resize(){var dpr=Math.min(window.devicePixelRatio||1,2);W=cv.clientWidth;H=cv.clientHeight;cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);}
resize();window.addEventListener('resize',resize);
function rgba(hex,a){var n=parseInt(hex.slice(1),16);return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')';}
function rx(p,a){var c=Math.cos(a),s=Math.sin(a);return{x:p.x,y:p.y*c-p.z*s,z:p.y*s+p.z*c};}
function ry(p,a){var c=Math.cos(a),s=Math.sin(a);return{x:p.x*c+p.z*s,y:p.y,z:-p.x*s+p.z*c};}
function rz(p,a){var c=Math.cos(a),s=Math.sin(a);return{x:p.x*c-p.y*s,y:p.x*s+p.y*c,z:p.z};}
var yaw=0.6,tilt=-0.42,tx=0,ty=0,mx=0,my=0;
document.addEventListener('mousemove',function(e){mx=e.clientX/window.innerWidth-0.5;my=e.clientY/window.innerHeight-0.5;});
document.addEventListener('mouseleave',function(){mx=0;my=0;});
function view(p){p=ry(p,yaw+tx);return rx(p,tilt+ty);}
function proj(p){var S=Math.min(W,H)*0.325,d=4.6,k=d/(d+p.z);return{x:W/2+p.x*S*k,y:H/2+p.y*S*k,k:k,z:p.z};}
function depthAlpha(z){var a=(1.4-z)/2.8;a=Math.max(0,Math.min(1,a));return 0.28+0.72*a;}
function ringPt(rg,th){return rz(rx({x:rg.r*Math.cos(th),y:0,z:rg.r*Math.sin(th)},rg.a),rg.b);}
var stars=[];for(var i=0;i<90;i++){var u=Math.random()*Math.PI*2,v=Math.acos(2*Math.random()-1),r=1.7+Math.random()*1.4;stars.push({x:r*Math.sin(v)*Math.cos(u),y:r*Math.cos(v),z:r*Math.sin(v)*Math.sin(u)});}
function poly(pts,close){ctx.beginPath();for(var i=0;i<pts.length;i++){if(i===0)ctx.moveTo(pts[i].x,pts[i].y);else ctx.lineTo(pts[i].x,pts[i].y);}if(close)ctx.closePath();ctx.stroke();}
function frame(){
  if(!reduce){yaw+=0.0032;}
  tx+=(mx*0.9-tx)*0.06;ty+=(my*0.55-ty)*0.06;
  ctx.clearRect(0,0,W,H);
  var S=Math.min(W,H)*0.325;
  var g=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,S*1.7);
  g.addColorStop(0,rgba(D.sevColor,0.30));g.addColorStop(0.45,rgba(D.sevColor,0.07));g.addColorStop(1,rgba(D.sevColor,0));
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  // stars
  stars.forEach(function(s){var q=proj(view(s));var a=0.12+0.4*depthAlpha(q.z);ctx.fillStyle='rgba(199,210,254,'+a+')';ctx.beginPath();ctx.arc(q.x,q.y,1.1*q.k,0,6.283);ctx.fill();});
  // wire globe
  ctx.lineWidth=1;ctx.strokeStyle='rgba(165,180,252,0.16)';
  var R=0.52,i,j,pts;
  [-60,-30,0,30,60].forEach(function(lat){var la=lat*Math.PI/180;pts=[];for(j=0;j<=48;j++){var lg=j/48*Math.PI*2;pts.push(proj(view({x:R*Math.cos(la)*Math.cos(lg),y:R*Math.sin(la),z:R*Math.cos(la)*Math.sin(lg)})));}poly(pts,false);});
  for(i=0;i<6;i++){var ph=i*Math.PI/6;pts=[];for(j=0;j<=48;j++){var u2=j/48*Math.PI*2;pts.push(proj(view({x:R*Math.cos(u2)*Math.cos(ph),y:R*Math.sin(u2),z:R*Math.cos(u2)*Math.sin(ph)})));}poly(pts,false);}
  // core
  var cg=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,S*0.34);
  cg.addColorStop(0,rgba(D.sevColor,0.85));cg.addColorStop(1,rgba(D.sevColor,0));
  ctx.fillStyle=cg;ctx.beginPath();ctx.arc(W/2,H/2,S*0.34,0,6.283);ctx.fill();
  // rings
  var labels=[];
  D.rings.forEach(function(rg){
    var N=140,pts3=[];
    for(i=0;i<=N;i++){var th=i/N*Math.PI*2;pts3.push(proj(view(ringPt(rg,th))));}
    ctx.lineCap='round';
    for(i=0;i<N;i++){var p0=pts3[i],p1=pts3[i+1],a=depthAlpha((p0.z+p1.z)/2);ctx.strokeStyle='rgba(255,255,255,'+(0.10*a)+')';ctx.lineWidth=1.6*p0.k;ctx.beginPath();ctx.moveTo(p0.x,p0.y);ctx.lineTo(p1.x,p1.y);ctx.stroke();}
    var n=Math.round(N*Math.max(0,Math.min(100,rg.v))/100);
    for(i=0;i<n;i++){var q0=pts3[i],q1=pts3[i+1],aa=depthAlpha((q0.z+q1.z)/2);ctx.strokeStyle=rgba(rg.color,aa);ctx.shadowColor=rg.color;ctx.shadowBlur=12*aa;ctx.lineWidth=(3.4+1.6*q0.k)*q0.k;ctx.beginPath();ctx.moveTo(q0.x,q0.y);ctx.lineTo(q1.x,q1.y);ctx.stroke();}
    ctx.shadowBlur=0;
    var hth=Math.PI*2*Math.max(0,Math.min(100,rg.v))/100;
    var hp=proj(view(ringPt(rg,hth)));
    labels.push({rg:rg,hp:hp});
  });
  // heads + labels
  var pulse=1+0.25*Math.sin(Date.now()/380);
  ctx.font='600 11px Inter, system-ui, sans-serif';
  var placed=[];
  labels.sort(function(a,b){return a.hp.y-b.hp.y;});
  labels.forEach(function(L){
    var hp=L.hp,rg=L.rg,fa=depthAlpha(hp.z);
    var txt=rg.name+'  '+Math.round(rg.v)+'%';
    var tw=ctx.measureText(txt).width+18,th=22;
    // push the label outward from the centre so it never sits on the status badge
    var dx=hp.x-W/2,dy=hp.y-H/2,len=Math.sqrt(dx*dx+dy*dy);
    var ux=len>1?dx/len:1,uy=len>1?dy/len:0;
    var dist=Math.max(len+28,92);
    var ax=W/2+ux*dist,ay=H/2+uy*dist;
    var bx=ux>=0?ax:ax-tw,by=ay-th/2;
    bx=Math.max(4,Math.min(W-tw-4,bx));by=Math.max(4,Math.min(H-th-4,by));
    // nudge down while overlapping an earlier label
    for(var tries=0;tries<8;tries++){
      var hit=false;
      for(var k2=0;k2<placed.length;k2++){var o=placed[k2];if(bx<o.x+o.w+4&&bx+tw+4>o.x&&by<o.y+o.h+4&&by+th+4>o.y){by=o.y+o.h+6;hit=true;}}
      if(!hit)break;
    }
    by=Math.min(H-th-4,by);
    placed.push({x:bx,y:by,w:tw,h:th});
    // head dot with pulse
    ctx.fillStyle=rgba(rg.color,0.25*fa);ctx.beginPath();ctx.arc(hp.x,hp.y,9*hp.k*pulse,0,6.283);ctx.fill();
    ctx.fillStyle='#fff';ctx.shadowColor=rg.color;ctx.shadowBlur=14;ctx.beginPath();ctx.arc(hp.x,hp.y,4.2*hp.k,0,6.283);ctx.fill();ctx.shadowBlur=0;
    // leader line
    ctx.strokeStyle=rgba(rg.color,0.55);ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(hp.x,hp.y);ctx.lineTo(ux>=0?bx:bx+tw,by+th/2);ctx.stroke();
    // label pill
    ctx.fillStyle='rgba(9,14,26,0.92)';ctx.strokeStyle=rgba(rg.color,0.85);ctx.lineWidth=1;
    ctx.beginPath();if(ctx.roundRect){ctx.roundRect(bx,by,tw,th,7);}else{ctx.rect(bx,by,tw,th);}ctx.fill();ctx.stroke();
    ctx.fillStyle='#e8edf7';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(txt,bx+9,by+th/2+0.5);
  });
  // center status
  ctx.textAlign='center';ctx.textBaseline='middle';
  var cw=96,ch=40,cx0=W/2-cw/2,cy0=H/2-ch/2;
  ctx.fillStyle='rgba(8,12,22,0.62)';ctx.strokeStyle='rgba(255,255,255,0.12)';ctx.lineWidth=1;
  ctx.beginPath();if(ctx.roundRect){ctx.roundRect(cx0,cy0,cw,ch,11);}else{ctx.rect(cx0,cy0,cw,ch);}ctx.fill();ctx.stroke();
  ctx.fillStyle='rgba(154,168,191,0.95)';ctx.font='600 8.5px Inter, system-ui, sans-serif';ctx.fillText('SYSTEM',W/2,H/2-9);
  ctx.fillStyle=D.sevColor;ctx.font='700 14px Inter, system-ui, sans-serif';ctx.fillText(D.sev,W/2,H/2+7);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
})();
</script></body></html>"""
    return template.replace("__DATA__", json.dumps(data))


def panel_container(key):
    """Styled container for the workspace pages (falls back on older Streamlit)."""
    try:
        return st.container(key=key)
    except TypeError:
        return st.container(border=True)


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-logo">'
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 2.5l8 3v6c0 5-3.4 9.2-8 10.8-4.6-1.6-8-5.8-8-10.8v-6l8-3z"/><path d="M8.6 12.2l2.4 2.4 4.4-4.6"/></svg></div>'
        '<div><div class="brand-name">SentinelAI</div><div class="brand-sub">Incident Commander</div></div></div>'
        '<div class="side-label">Workspace</div>',
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Workspace navigation",
        ["Overview", "Incident analysis", "Runbook guidance"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown('<div class="side-label">Monitoring</div>', unsafe_allow_html=True)
    st.caption("Live host metrics are read from the computer running this dashboard.")
    refresh_now = st.button("Refresh metrics", use_container_width=True)
    auto_refresh = st.toggle("Auto-refresh every 10 seconds", value=False)
    st.markdown("---")
    st.markdown('<div class="side-label">Safety mode</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="safety"><b>● HUMAN APPROVAL REQUIRED</b><br>'
        "SentinelAI suggests investigation steps only. It does not terminate processes or change your system.</div>",
        unsafe_allow_html=True,
    )

# ---------- Read live metrics (cached so clicks stay fast) ----------
if "metric_history" not in st.session_state:
    st.session_state.metric_history = []

cache = st.session_state.get("metrics_cache")
need_fresh = (
    refresh_now
    or auto_refresh
    or cache is None
    or time.time() - cache["ts"] > 120
)
if need_fresh:
    try:
        fresh = get_system_metrics()
    except Exception as exc:
        st.error(f"Could not read system metrics: {exc}")
        st.stop()
    cache = {"data": fresh, "ts": time.time(), "at": datetime.now().astimezone()}
    st.session_state.metrics_cache = cache
    st.session_state.metric_history.append(
        {
            "time": cache["at"].strftime("%H:%M:%S"),
            "cpu": fresh["cpu"],
            "memory": fresh["memory"],
            "disk": fresh["disk"],
            "status": get_severity(fresh),
        }
    )
    st.session_state.metric_history = st.session_state.metric_history[-8:]

metrics = cache["data"]
now = cache["at"]
severity = get_severity(metrics)
problems = get_problems(metrics)
recommendations = get_recommendations(problems)
history = st.session_state.metric_history

if refresh_now:
    st.toast("System metrics refreshed.", icon="✅")

sev_tone = {"HEALTHY": "ok", "WARNING": "warn", "CRITICAL": "crit"}[severity]

# ---------- Top bar ----------
st.markdown(
    f'<div class="topbar"><div class="crumbs">Control room<span>/</span><b>{esc(page)}</b></div>'
    f'<div class="top-right"><span class="live"><i></i>LIVE</span>'
    f'<span class="clock">{now.strftime("%a %d %b %Y · %H:%M:%S")}</span></div></div>',
    unsafe_allow_html=True,
)

# ---------- Hero ----------
status_message = {
    "HEALTHY": "All monitored resource levels are within the configured thresholds.",
    "WARNING": "At least one resource is elevated. Investigate before it becomes an incident.",
    "CRITICAL": "At least one resource has reached the critical threshold. Investigate promptly.",
}[severity]
status_tag = {"HEALTHY": "ALL CLEAR", "WARNING": "NEEDS ATTENTION", "CRITICAL": "ACTION REQUIRED"}[severity]
status_icon = {"HEALTHY": "✓", "WARNING": "!", "CRITICAL": "✕"}[severity]

hero_l, hero_r = st.columns([1.02, 1], gap="large")
with hero_l:
    st.markdown(
        '<div class="kicker"><i></i>Site reliability engineering</div>'
        '<h1 class="hero-h">Incident command<br><span class="grad">starts with clarity.</span></h1>'
        '<p class="hero-p">A live system-health overview with actionable signals, runbook context, and human-approved recovery guidance.</p>'
        f'<div class="banner {sev_tone}"><div class="banner-l"><div class="banner-ic">{status_icon}</div>'
        f'<div><div class="banner-t">System status: {severity}</div><div class="banner-s">{status_message}</div></div></div>'
        f'<div class="banner-tag">{status_tag}</div></div>'
        '<div class="stats">'
        f'<div class="stat"><div class="stat-v">{fmt_uptime(metrics["uptime"])}</div><div class="stat-l">Uptime</div></div>'
        f'<div class="stat"><div class="stat-v">{metrics["process_count"]}</div><div class="stat-l">Processes</div></div>'
        f'<div class="stat"><div class="stat-v">{metrics["cores"]}</div><div class="stat-l">CPU threads</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )
with hero_r:
    scene_html = build_scene(metrics, severity)
    if hasattr(st, "iframe"):
        st.iframe(scene_html, height=400)  # newer Streamlit
    else:
        components.html(scene_html, height=400)  # older Streamlit

# ---------- Resource cards ----------
st.markdown(
    '<div class="sec"><h3>Resource telemetry</h3><span>Live readings from this host · hover a card</span></div>',
    unsafe_allow_html=True,
)
c1, c2, c3 = st.columns(3, gap="large")
cards = [
    (c1, "cpu", "Processor", "CPU", metrics["cpu"], f"{metrics['cores']} threads · current load"),
    (c2, "memory", "Memory", "RAM", metrics["memory"], f"{metrics['memory_used_gb']:.1f} / {metrics['memory_total_gb']:.1f} GB used"),
    (c3, "disk", "Storage", "DISK", metrics["disk"], f"{metrics['disk_used_gb']:.1f} / {metrics['disk_total_gb']:.0f} GB used"),
]
for col, key, label, tag, value, foot in cards:
    with col:
        st.markdown(
            resource_card(key, label, tag, value, foot, [row[key] for row in history]),
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# Rerun only this panel when its button is clicked (fast), not the whole page.
_fragment = getattr(st, "fragment", None) or getattr(st, "experimental_fragment", None) or (lambda f: f)


@_fragment
def render_incident_panel(severity, problems):
    with panel_container("incident_panel"):
        st.markdown("### Incident analysis")
        st.caption("Run the existing SentinelAI monitoring, alert, AI diagnosis, and recovery agents on demand.")
        st.markdown(f"**Live dashboard severity:** `{severity}`")
        if problems:
            for problem in problems:
                st.markdown(f"- {problem}")
        else:
            st.success("No CPU, memory, or disk threshold breach is currently detected by the dashboard rules.")

        st.markdown("#### Run the SentinelAI agent workflow")
        st.caption(
            "This button calls the project's System_monitor → AlertAgent → DiagnosisAgent → RecoveryAgent pipeline. "
            "Gemini diagnosis requires a valid API key and network access."
        )
        if st.button("▶  Run AI Incident Analysis", key="run_ai_incident_analysis", use_container_width=True):
            with st.spinner("Collecting metrics and running SentinelAI agents…"):
                t0 = time.time()
                try:
                    incident, diagnosis, diagnosis_error, agent_recommendations = run_sentinelai_agents()
                    st.session_state["sentinelai_analysis"] = {
                        "severity": getattr(incident, "severity", "UNKNOWN"),
                        "problems": list(getattr(incident, "problems", []) or []),
                        "diagnosis": diagnosis,
                        "diagnosis_error": diagnosis_error,
                        "recommendations": list(agent_recommendations or []),
                        "run_at": datetime.now().astimezone().strftime("%d %b %Y, %H:%M:%S %Z"),
                        "took": time.time() - t0,
                    }
                except Exception as exc:
                    st.session_state["sentinelai_analysis_error"] = str(exc)
                    st.session_state.pop("sentinelai_analysis", None)
                else:
                    st.session_state.pop("sentinelai_analysis_error", None)

        if st.session_state.get("sentinelai_analysis_error"):
            st.error("SentinelAI could not complete the agent workflow. Check the terminal for details.")
            st.code(st.session_state["sentinelai_analysis_error"])

        analysis = st.session_state.get("sentinelai_analysis")
        if analysis:
            st.markdown("---")
            st.markdown(f"**Agent incident severity:** `{analysis['severity']}`")
            st.caption(f"Analysis run: {analysis['run_at']} · took {analysis.get('took', 0):.1f}s")

            st.markdown("#### Detected problems")
            if analysis["problems"]:
                for problem in analysis["problems"]:
                    st.markdown(f"- {problem}")
            else:
                st.success("The Alert Agent did not identify a threshold-based problem.")

            st.markdown("#### AI diagnosis")
            if analysis["diagnosis"]:
                st.markdown(analysis["diagnosis"])
            elif analysis["diagnosis_error"]:
                st.warning("The incident and recovery results are available, but Gemini diagnosis failed for this run.")
                st.caption("This can happen if the API is temporarily unavailable, the API key is missing/invalid, or the network request fails.")
                with st.expander("Technical error details"):
                    st.code(analysis["diagnosis_error"])
            else:
                st.info("No AI diagnosis was needed or returned for this incident.")

            st.markdown("#### Recovery recommendations")
            if analysis["recommendations"]:
                for idx, recommendation in enumerate(analysis["recommendations"], start=1):
                    st.markdown(f"{idx}. {recommendation}")
            else:
                st.info("The Recovery Agent did not return any recommendations for this incident.")
            st.caption("Recommendations are advisory only. SentinelAI does not automatically execute remediation actions.")
        else:
            st.info("Select **Run AI Incident Analysis** to execute the agents and display their results here.")


# ---------- Pages ----------
if page == "Overview":
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        if problems:
            rows = "".join(
                f'<div class="sig {sev_tone}"><div class="sig-ic">!</div><div><div class="sig-t">{esc(p)}</div>'
                f'<div class="sig-s">Threshold-based signal · review recommended</div></div></div>'
                for p in problems
            )
        else:
            rows = (
                '<div class="sig ok"><div class="sig-ic">✓</div><div><div class="sig-t">No resource threshold breaches detected.</div>'
                '<div class="sig-s">CPU and memory warning at 75%; disk warning at 85%.</div></div></div>'
            )
        st.markdown(
            f'<div class="panel"><div class="panel-t">Signal summary</div><div class="panel-d">What the current metrics indicate</div>{rows}'
            '<div class="fine">This MVP checks host-level resource usage. It does not yet monitor application logs, distributed traces, or remote servers.</div></div>',
            unsafe_allow_html=True,
        )
    with right:
        steps = "".join(
            f'<div class="step"><span class="step-n">{i:02d}</span><div>{esc(r)}</div></div>'
            for i, r in enumerate(recommendations, start=1)
        )
        st.markdown(
            f'<div class="panel"><div class="panel-t">Recommended next steps</div>'
            f'<div class="panel-d">Safe investigation guidance · no automatic remediation</div>{steps}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="sec"><h3>Activity</h3><span>Busiest processes and this session’s checks</span></div>',
        unsafe_allow_html=True,
    )
    a_left, a_right = st.columns([1.1, 1], gap="large")
    with a_left:
        if metrics["top_procs"]:
            prow = ""
            for p in metrics["top_procs"]:
                prow += (
                    f'<tr><td class="pname">{esc(p["name"])}</td><td class="mono">{p["pid"]}</td>'
                    f'<td class="mono"><span class="bar"><i style="width:{min(100, p["cpu"]):.0f}%"></i></span>{p["cpu"]:.1f}%</td>'
                    f'<td class="mono"><span class="bar"><i style="width:{min(100, p["mem"]):.0f}%"></i></span>{p["mem"]:.1f}%</td></tr>'
                )
            body = f'<table class="tbl"><thead><tr><th>Process</th><th>PID</th><th>CPU</th><th>Memory</th></tr></thead><tbody>{prow}</tbody></table>'
        else:
            body = '<div class="sig-s">Process details are not available on this system.</div>'
        st.markdown(
            f'<div class="panel"><div class="panel-t">Top processes</div><div class="panel-d">Read-only view · sorted by CPU, then memory</div>{body}</div>',
            unsafe_allow_html=True,
        )
    with a_right:
        hrows = ""
        for row in reversed(history):
            t = {"HEALTHY": "ok", "WARNING": "warn", "CRITICAL": "crit"}[row["status"]]
            hrows += (
                f'<tr><td class="mono">{row["time"]}</td><td class="mono">{row["cpu"]:.1f}%</td>'
                f'<td class="mono">{row["memory"]:.1f}%</td><td class="mono">{row["disk"]:.1f}%</td>'
                f'<td><span class="chip {t}">{row["status"]}</span></td></tr>'
            )
        st.markdown(
            f'<div class="panel"><div class="panel-t">Recent health checks</div><div class="panel-d">This session · latest 8 readings</div>'
            f'<table class="tbl"><thead><tr><th>Time</th><th>CPU</th><th>Mem</th><th>Disk</th><th>Status</th></tr></thead><tbody>{hrows}</tbody></table></div>',
            unsafe_allow_html=True,
        )

elif page == "Incident analysis":
    render_incident_panel(severity, problems)

elif page == "Runbook guidance":
    with panel_container("runbook_panel"):
        runbook = try_get_runbook(problems)
        st.markdown("### Runbook guidance")
        st.caption("Relevant local runbook content, when a matching resource signal exists.")
        if runbook:
            st.markdown(runbook)
        elif problems:
            st.info("A relevant runbook was not found. Check that knowledge_base contains high_cpu.txt, high_memory.txt, and high_disk.txt and that app.runbook_retriever is importable.")
            st.markdown("#### General investigation suggestions")
            for item in recommendations:
                st.markdown(f"- {item}")
        else:
            st.success("No resource issue currently needs a runbook. Runbook guidance will appear here when a monitored threshold is breached.")

# ---------- Footer ----------
st.markdown(
    f'<div style="margin-top:2.5rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.08);display:flex;'
    f'justify-content:space-between;gap:1rem;color:#6b7a93;font-size:.82rem;">'
    f'<span>SENTINELAI · AI-POWERED SRE INCIDENT COMMANDER</span>'
    f'<span>Local host: <span class="mono">{esc(metrics["disk_root"])}</span> · Updated {now.strftime("%d %b %Y, %H:%M:%S")}</span></div>',
    unsafe_allow_html=True,
)

if auto_refresh:
    time.sleep(10)
    st.rerun()