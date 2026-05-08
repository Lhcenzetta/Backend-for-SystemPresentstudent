import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from PIL import Image

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Attendance Dashboard | FS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Customization ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #f5f7fb; color: #1e293b; }
.stApp { background: #f5f7fb; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem; }

/* Header & Logo */
.header-container {
    background: white; padding: 1rem 2rem; border-radius: 18px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 2rem; border: 1px solid #e2e8f0; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.fsa-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin: 0; }
.fsa-subtitle { color: #2563eb; font-weight: 600; font-size: 1rem; }
.live-badge { background: #dcfce7; color: #166534; padding: 0.5rem 1rem; border-radius: 999px; font-weight: 600; font-size: 0.8rem; }

/* Metric Cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 2rem; }
.metric-card { flex: 1; background: white; padding: 1.5rem; border-radius: 18px; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
.metric-label { color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
.metric-value { font-size: 1.8rem; font-weight: 700; color: #0f172a; }

/* Table & Charts */
.section-label { font-size: 1rem; font-weight: 700; color: #334155; margin-bottom: 1rem; }
.side-card { background: #f8fafc; padding: 1rem; border-radius: 14px; border: 1px solid #e2e8f0; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ─── Header & Logo Section ──────────────────────────────────────────────────
col_header_left, col_header_right = st.columns([4, 1])

with col_header_left:
    c1, c2 = st.columns([1, 6])
    with c1:
        try:
            img = Image.open("logo.png")
            # st.image(img, width=80)
        except:
            st.markdown("🏫")
    with c2:
        # st.markdown('<p class="fsa-title">Faculté des Sciences Appliquées - Ait Melloul</p>', unsafe_allow_html=True)
        st.markdown('<p class="fsa-subtitle">Système de Pointage Intelligent • UI Dashboard</p>', unsafe_allow_html=True)

with col_header_right:
    now_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f'<div class="live-badge">🟢 LIVE • {now_time}</div>', unsafe_allow_html=True)

# ─── Fetch Data Logic ────────────────────────────────────────────────────────
def fetch_data():
    try:
        r = requests.get("http://127.0.0.1:8000/all_attendance", timeout=2)
        if r.status_code == 200:
            return r.json()
    except:
        return []
    return []

data = fetch_data()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📥 Management")
    if data:
        df_side = pd.DataFrame(data)
        csv = df_side.to_csv(index=False).encode('utf-8')
        st.download_button("Export Attendance CSV", csv, "attendance.csv", "text/csv", width='stretch')
        
        st.markdown("---")
        st.markdown(f"""
        <div class="side-card">
            <div style="font-size:0.7rem; color:#64748b;">LATEST STUDENT</div>
            <div style="font-weight:700; color:#2563eb;">{df_side.iloc[-1]['full_name'] if not df_side.empty else '—'}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Main Content ────────────────────────────────────────────────────────────
if data:
    df = pd.DataFrame(data)
    
    # Calculation
    total = len(df)
    unique = df['apogee_code'].nunique()
    
    # ── Metric Cards ──
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card"><div class="metric-label">Total Records</div><div class="metric-value">{total}</div></div>
        <div class="metric-card"><div class="metric-label">Unique Students</div><div class="metric-value">{unique}</div></div>
        <div class="metric-card"><div class="metric-label">Avg Scans</div><div class="metric-value">{total/unique:.1f}</div></div>
        <div class="metric-card"><div class="metric-label">Status</div><div class="metric-value" style="color:#166534;">Online</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Table & Activity ──
    col_table, col_chart = st.columns([3, 2], gap="large")

    with col_table:
        st.markdown('<p class="section-label">📄 Attendance Log</p>', unsafe_allow_html=True)
        # FIX: width='stretch' blast use_container_width
        st.dataframe(
            df.sort_values(by='id', ascending=False),
            width='stretch', 
            hide_index=True,
            height=450
        )

    with col_chart:
        st.markdown('<p class="section-label">📊 Top Attendees</p>', unsafe_allow_html=True)
        chart_data = df['full_name'].value_counts().head(10)
        st.bar_chart(chart_data, color="#2563eb", width='stretch')

else:
    st.error("🔴 Backend Offline - Cannot connect to http://127.0.0.1:8000")

# ─── Auto Refresh ────────────────────────────────────────────────────────────
st.markdown(f'<div style="text-align:center; color:#64748b; font-size:0.8rem; margin-top:2rem;">Auto-refresh active (5s) • Last update: {now_time}</div>', unsafe_allow_html=True)
time.sleep(5)
st.rerun()