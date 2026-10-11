import os
import time
from datetime import datetime
from types import SimpleNamespace

import psutil
import streamlit as st

# ------------------------------------------------------------
# SentinelAI — AI-Powered SRE Incident Commander
# Dashboard UI + live host metrics + safe, rule-based guidance.
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
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #080d18;
        --panel: #101827;
        --panel2: #0c1422;
        --line: rgba(148, 163, 184, .15);
        --muted: #bdcbe0;
        --text: #edf4ff;
        --cyan: #4de2d0;
        --blue: #6d9bff;
        --amber: #ffbf69;
        --red: #ff6b81;
    }
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
        font-size: 16px;
    }
    /* Readability pass: increase small labels, supporting text, and controls. */
    .stApp, .stMarkdown, .stText, .stCaption, label {
        color: #edf4ff;
        font-size: 1rem;
    }
    p, li { font-size: .96rem; line-height: 1.65; }
    [data-testid="stCaptionContainer"] p { font-size: .86rem !important; color: #b8c7dc !important; }
    [data-testid="stMetricLabel"] { font-size: .95rem !important; }
    [data-testid="stMetricValue"] { font-size: 2rem !important; }
    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, rgba(38, 95, 150, .19), transparent 38%),
            radial-gradient(ellipse at 95% 12%, rgba(36, 174, 158, .10), transparent 28%),
            var(--bg);
        color: var(--text);
    }
    [data-testid="stHeader"] { background: rgba(8, 13, 24, .88); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e1727 0%, #0a111e 100%);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div { padding-top: 1.3rem; }
    .block-container { padding-top: 1.7rem; padding-bottom: 3rem; max-width: 1500px; }
    h1, h2, h3, p, label { color: var(--text); }
    .eyebrow {
        color: var(--cyan); font-size: .84rem; font-weight: 800;
        letter-spacing: .19em; text-transform: uppercase; margin-bottom: .45rem;
    }
    .hero-title {
        color: #f3f7ff; font-size: clamp(2rem, 3.1vw, 3.1rem);
        font-weight: 800; letter-spacing: -.055em; line-height: 1.05;
        margin: 0;
    }
    .hero-subtitle { color: #b8c7dc; font-size: 1.08rem; line-height: 1.65; margin-top: .75rem; }
    .pill {
        display: inline-flex; align-items: center; gap: .45rem;
        border: 1px solid rgba(77, 226, 208, .25);
        background: rgba(77, 226, 208, .08); color: var(--cyan);
        border-radius: 999px; padding: .42rem .75rem;
        font-size: .72rem; font-weight: 800; letter-spacing: .06em;
    }
    .dot {
        width: 7px; height: 7px; display: inline-block; border-radius: 50%;
        background: var(--cyan); box-shadow: 0 0 12px rgba(77,226,208,.8);
    }
    .section-head {
        display: flex; justify-content: space-between; align-items: center;
        gap: 1rem; margin: 1.35rem 0 .8rem;
    }
    .section-title { font-size: 1.05rem; font-weight: 800; letter-spacing: -.02em; }
    .section-note { color: #b8c7dc; font-size: .88rem; }
    .metric-card {
        background: linear-gradient(145deg, rgba(20,32,51,.98), rgba(13,22,36,.98));
        border: 1px solid var(--line); border-radius: 18px;
        padding: 1.15rem 1.2rem 1.05rem; min-height: 175px;
        box-shadow: 0 12px 32px rgba(0,0,0,.12);
    }
    .metric-top { display: flex; justify-content: space-between; align-items: center; }
    .metric-label { color: #aab8cd; font-size: .9rem; font-weight: 700; letter-spacing: .04em; }
    .metric-icon {
        display: inline-flex; align-items: center; justify-content: center;
        width: 34px; height: 34px; border-radius: 11px;
        background: rgba(109,155,255,.12); color: #91b4ff; font-size: 1rem;
    }
    .metric-value { font-size: 2.15rem; line-height: 1.15; font-weight: 800; letter-spacing: -.06em; margin-top: .75rem; }
    .metric-foot { color: var(--muted); font-size: .88rem; line-height: 1.5; margin-top: .45rem; }
    .panel {
        background: linear-gradient(145deg, rgba(17,27,44,.98), rgba(12,20,34,.98));
        border: 1px solid var(--line); border-radius: 18px;
        padding: 1.15rem 1.25rem; height: 100%;
    }
    .panel-title { font-size: 1rem; font-weight: 800; margin-bottom: .2rem; }
    .panel-desc { color: #b8c7dc; font-size: .9rem; line-height: 1.55; margin-bottom: 1rem; }
    .status-box {
        display: flex; align-items: center; justify-content: space-between; gap: 1rem;
        border-radius: 14px; padding: 1rem 1.1rem; margin: .65rem 0;
        background: rgba(77,226,208,.07); border: 1px solid rgba(77,226,208,.20);
    }
    .status-box.warning { background: rgba(255,191,105,.07); border-color: rgba(255,191,105,.25); }
    .status-box.critical { background: rgba(255,107,129,.07); border-color: rgba(255,107,129,.25); }
    .status-main { font-size: 1.1rem; font-weight: 800; }
    .status-caption { color: #c0ccde; font-size: .88rem; line-height: 1.5; margin-top: .2rem; }
    .status-tag {
        border-radius: 8px; padding: .35rem .55rem; font-size: .69rem;
        font-weight: 800; letter-spacing: .08em; white-space: nowrap;
        color: var(--cyan); background: rgba(77,226,208,.1);
    }
    .warning .status-tag { color: var(--amber); background: rgba(255,191,105,.12); }
    .critical .status-tag { color: var(--red); background: rgba(255,107,129,.12); }
    .signal {
        padding: .7rem 0; border-bottom: 1px solid var(--line);
        display: flex; gap: .65rem; align-items: flex-start;
    }
    .signal:last-child { border-bottom: 0; }
    .signal-bullet { color: var(--cyan); font-size: 1rem; line-height: 1.3; }
    .signal-text { color: #d8e2f2; font-size: .96rem; line-height: 1.6; }
    .signal-sub { color: #b8c7dc; font-size: .84rem; line-height: 1.5; margin-top: .2rem; }
    .recommendation {
        border: 1px solid var(--line); background: rgba(255,255,255,.025);
        border-radius: 12px; padding: .8rem .9rem; margin: .55rem 0;
        color: #edf4ff; font-size: .96rem; line-height: 1.6;
    }
    .rec-number { color: var(--cyan); font-family: 'DM Mono', monospace; margin-right: .45rem; }
    .mini-label { color: #b8c7dc; font-size: .82rem; letter-spacing: .1em; text-transform: uppercase; font-weight: 800; }
    .mono { font-family: 'DM Mono', monospace; }
    .footer {
        border-top: 1px solid var(--line); margin-top: 2rem; padding-top: 1rem;
        color: #aebdd2; font-size: .82rem; display: flex; justify-content: space-between; gap: 1rem;
    }
    div.stButton > button,
    div.stButton > button:focus,
    div.stButton > button:hover,
    [data-testid="stSidebar"] div.stButton > button {
        border-radius: 12px !important;
        border: 1px solid #79f1e4 !important;
        background: linear-gradient(110deg, #4de2d0, #76e8db) !important;
        color: #061521 !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        line-height: 1.35 !important;
        min-height: 48px !important;
        padding: .78rem 1rem !important;
        box-shadow: 0 5px 18px rgba(77,226,208,.12);
        transition: transform .15s ease, filter .15s ease;
    }
    div.stButton > button p,
    div.stButton > button span,
    div.stButton > button div,
    [data-testid="stSidebar"] div.stButton > button p,
    [data-testid="stSidebar"] div.stButton > button span {
        color: #061521 !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
    }
    div.stButton > button:hover { filter: brightness(1.05); transform: translateY(-1px); }
    div[data-testid="stProgress"] > div > div { background: linear-gradient(90deg, #4de2d0, #6d9bff); }
    div[data-testid="stProgress"] > div { background: #243248; border-radius: 999px; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background: #101a2a !important; color: var(--text) !important;
        border-color: var(--line) !important; border-radius: 10px !important;
    }

    /* Final accessibility/readability pass */
    .stApp { font-size: 17px; }
    .stMarkdown p, .stMarkdown li { font-size: 1rem; line-height: 1.7; }
    .metric-label { font-size: .96rem !important; color: #d0def1 !important; }
    .metric-foot { font-size: .94rem !important; color: #c0cfe3 !important; }
    .section-title, .panel-title { font-size: 1.12rem !important; }
    .section-note, .panel-desc { font-size: .94rem !important; color: #c3d1e5 !important; }
    .status-caption { font-size: .94rem !important; color: #d0dced !important; }
    .status-tag { font-size: .8rem !important; }
    .pill { font-size: .82rem !important; }
    .eyebrow { font-size: .9rem !important; }
    .signal-text, .recommendation { font-size: 1rem !important; line-height: 1.7 !important; }
    .signal-sub { font-size: .9rem !important; color: #c0cfe3 !important; }
    .mini-label { font-size: .86rem !important; color: #c0cfe3 !important; }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label {
        color: #d3deed !important;
        font-size: .95rem !important;
        line-height: 1.65 !important;
    }
    [data-testid="stSidebar"] div.stButton > button {
        min-height: 52px !important;
    }

    .stAlert { border-radius: 12px; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [role="radiogroup"] label {
        font-size: .94rem !important;
        line-height: 1.6 !important;
        color: #e1eaf7 !important;
    }
    [data-testid="stDataFrame"] { font-size: .9rem; }
    div[data-testid="stProgress"] { margin-top: .1rem; }
    div[data-testid="stProgress"] > div > div { min-height: 9px; }
    #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Helpers ----------
def get_system_metrics():
    """Read live CPU, memory, and root-disk utilization from this machine."""
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk_root = os.path.abspath(os.sep)
    disk = psutil.disk_usage(disk_root)
    return {
        "cpu": float(cpu),
        "memory": float(memory.percent),
        "memory_used_gb": memory.used / (1024 ** 3),
        "memory_total_gb": memory.total / (1024 ** 3),
        "disk": float(disk.percent),
        "disk_used_gb": disk.used / (1024 ** 3),
        "disk_total_gb": disk.total / (1024 ** 3),
        "disk_root": disk_root,
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
        # Dashboard remains usable if project imports are not available yet.
        return None
    return None


def status_color(severity):
    return {"HEALTHY": "healthy", "WARNING": "warning", "CRITICAL": "critical"}.get(severity, "healthy")


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:1.5rem;">
            <div style="width:45px;height:45px;border-radius:14px;background:linear-gradient(135deg,#4de2d0,#6d9bff);display:flex;align-items:center;justify-content:center;font-size:1.45rem;">🛡️</div>
            <div>
                <div style="font-size:1.2rem;font-weight:800;letter-spacing:-.04em;color:#f3f7ff;">SentinelAI</div>
                <div style="font-size:.66rem;color:#91a0b7;letter-spacing:.12em;text-transform:uppercase;">Incident Commander</div>
            </div>
        </div>
        <div class="mini-label">Workspace</div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Workspace navigation",
        ["Overview", "Incident analysis", "Runbook guidance"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown('<div class="mini-label">Monitoring configuration</div>', unsafe_allow_html=True)
    st.caption("Live host metrics are read from the computer running this dashboard.")
    refresh_now = st.button("↻  Refresh system metrics", use_container_width=True)
    st.markdown("---")
    st.markdown('<div class="mini-label">Safety mode</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="border:1px solid rgba(77,226,208,.22);background:rgba(77,226,208,.06);border-radius:12px;padding:.75rem;font-size:.78rem;color:#cbd8e9;">'
        '<span style="color:#4de2d0;font-weight:800;">● HUMAN APPROVAL REQUIRED</span><br>'
        '<span style="color:#91a0b7;">SentinelAI suggests investigation steps only. It does not terminate processes or change your system.</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="position:fixed;bottom:1rem;color:#62728b;font-size:.68rem;">SENTINELAI • MVP BUILD</div>',
        unsafe_allow_html=True,
    )

# ---------- Read live metrics ----------
try:
    metrics = get_system_metrics()
except Exception as exc:
    st.error(f"Could not read system metrics: {exc}")
    st.stop()

severity = get_severity(metrics)
problems = get_problems(metrics)
recommendations = get_recommendations(problems)
runbook = try_get_runbook(problems)
now = datetime.now().astimezone()

# Keep a small session history of dashboard checks.
if "metric_history" not in st.session_state:
    st.session_state.metric_history = []
st.session_state.metric_history.append(
    {"time": now.strftime("%H:%M:%S"), "cpu": metrics["cpu"], "memory": metrics["memory"], "disk": metrics["disk"], "status": severity}
)
st.session_state.metric_history = st.session_state.metric_history[-8:]

if refresh_now:
    st.toast("System metrics refreshed.", icon="✅")

# ---------- Hero ----------
hero_left, hero_right = st.columns([3.1, 1])
with hero_left:
    st.markdown('<div class="eyebrow">Site reliability engineering • Control room</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Incident command<br>starts with clarity.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">A live system-health overview with actionable signals, runbook context, and human-approved recovery guidance.</div>',
        unsafe_allow_html=True,
    )
with hero_right:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:right;"><span class="pill"><span class="dot"></span> MONITORING ACTIVE</span><div style="color:#91a0b7;font-size:.72rem;margin-top:.7rem;">Last checked <span class="mono">{now.strftime("%H:%M:%S")}</span></div></div>',
        unsafe_allow_html=True,
    )

# ---------- Status banner ----------
status_class = status_color(severity)
status_message = {
    "HEALTHY": "All monitored resource levels are within the configured thresholds.",
    "WARNING": "At least one resource is elevated. Investigate before it becomes an incident.",
    "CRITICAL": "At least one resource has reached the critical threshold. Investigate promptly.",
}[severity]
status_tag = {"HEALTHY": "ALL CLEAR", "WARNING": "NEEDS ATTENTION", "CRITICAL": "ACTION REQUIRED"}[severity]
status_icon = {"HEALTHY": "✓", "WARNING": "!", "CRITICAL": "×"}[severity]
st.markdown(
    f'<div class="status-box {status_class}"><div style="display:flex;align-items:center;gap:.85rem;"><div style="width:38px;height:38px;border-radius:12px;background:rgba(255,255,255,.05);display:flex;align-items:center;justify-content:center;font-size:1.25rem;font-weight:800;">{status_icon}</div><div><div class="status-main">System status: {severity}</div><div class="status-caption">{status_message}</div></div></div><div class="status-tag">{status_tag}</div></div>',
    unsafe_allow_html=True,
)

# ---------- Metric cards ----------
st.markdown(
    '<div class="section-head"><div class="section-title">Resource telemetry</div><div class="section-note">Live readings from this host</div></div>',
    unsafe_allow_html=True,
)
c1, c2, c3 = st.columns(3)
metric_items = [
    (c1, "CPU UTILIZATION", "◈", metrics["cpu"], "Processor load", f"{metrics['cpu']:.1f}%"),
    (c2, "MEMORY PRESSURE", "▦", metrics["memory"], f"{metrics['memory_used_gb']:.1f} / {metrics['memory_total_gb']:.1f} GB used", f"{metrics['memory']:.1f}%"),
    (c3, "DISK CAPACITY", "▤", metrics["disk"], f"{metrics['disk_used_gb']:.1f} / {metrics['disk_total_gb']:.1f} GB used", f"{metrics['disk']:.1f}%"),
]
for col, label, icon, value, foot, display in metric_items:
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-top"><div class="metric-label">{label}</div><div class="metric-icon">{icon}</div></div><div class="metric-value">{display}</div><div class="metric-foot">{foot}</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size:.86rem;color:#c4d2e5;margin:.45rem 0 .2rem;">{value:.1f}% utilized</div>',
            unsafe_allow_html=True,
        )
        st.progress(min(max(value / 100, 0.0), 1.0))

# ---------- Main workspace ----------
st.markdown("<br>", unsafe_allow_html=True)
if page == "Overview":
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown(
            '<div class="panel"><div class="panel-title">🔎 Signal summary</div><div class="panel-desc">What the current metrics indicate</div>',
            unsafe_allow_html=True,
        )
        if problems:
            for item in problems:
                st.markdown(
                    f'<div class="signal"><div class="signal-bullet">◆</div><div><div class="signal-text">{item}</div><div class="signal-sub">Threshold-based signal • review recommended</div></div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="signal"><div class="signal-bullet">✓</div><div><div class="signal-text">No resource threshold breaches detected.</div><div class="signal-sub">CPU and memory warning at 75%; disk warning at 85%.</div></div></div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            '<div style="color:#91a0b7;font-size:.73rem;margin-top:.8rem;">This MVP checks host-level resource usage. It does not yet monitor application logs, distributed traces, or remote servers.</div></div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            '<div class="panel"><div class="panel-title">🧭 Recommended next steps</div><div class="panel-desc">Safe investigation guidance • no automatic remediation</div>',
            unsafe_allow_html=True,
        )
        for idx, recommendation in enumerate(recommendations, start=1):
            st.markdown(
                f'<div class="recommendation"><span class="rec-number">0{idx}</span>{recommendation}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-head"><div class="section-title">Recent health checks</div><div class="section-note">This session • latest 8 readings</div></div>',
        unsafe_allow_html=True,
    )
    history = st.session_state.metric_history
    if history:
        rows = []
        for row in reversed(history):
            rows.append(
                {
                    "Time": row["time"],
                    "CPU": f'{row["cpu"]:.1f}%',
                    "Memory": f'{row["memory"]:.1f}%',
                    "Disk": f'{row["disk"]:.1f}%',
                    "Status": row["status"],
                }
            )
        st.dataframe(rows, use_container_width=True, hide_index=True)

elif page == "Incident analysis":
    st.markdown(
        '<div class="panel"><div class="panel-title">🚨 Incident analysis</div><div class="panel-desc">Review current host signals and prepare a triage summary.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**Current severity:** `{severity}`")
    if problems:
        for problem in problems:
            st.markdown(f"- {problem}")
    else:
        st.success("No CPU, memory, or disk threshold breach is currently detected.")
    st.markdown("#### Triage recommendations")
    for idx, recommendation in enumerate(recommendations, start=1):
        st.markdown(f"{idx}. {recommendation}")
    st.caption("Diagnosis in this dashboard currently uses transparent threshold rules. Gemini diagnosis is not invoked from this page yet.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Runbook guidance":
    st.markdown(
        '<div class="panel"><div class="panel-title">📘 Runbook guidance</div><div class="panel-desc">Relevant local runbook content, when a matching resource signal exists.</div>',
        unsafe_allow_html=True,
    )
    if runbook:
        st.markdown(runbook)
    elif problems:
        st.info("A relevant runbook was not found. Check that knowledge_base contains high_cpu.txt, high_memory.txt, and high_disk.txt and that app.runbook_retriever is importable.")
        st.markdown("#### General investigation suggestions")
        for item in recommendations:
            st.markdown(f"- {item}")
    else:
        st.success("No resource issue currently needs a runbook. Runbook guidance will appear here when a monitored threshold is breached.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown(
    f'<div class="footer"><span>🛡️ SENTINELAI · AI-POWERED SRE INCIDENT COMMANDER</span><span>Local host: <span class="mono">{metrics["disk_root"]}</span> · Updated {now.strftime("%d %b %Y, %H:%M:%S")}</span></div>',
    unsafe_allow_html=True,
)
