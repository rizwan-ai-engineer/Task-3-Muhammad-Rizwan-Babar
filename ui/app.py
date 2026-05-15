"""
ui/app.py — Streamlit Interface (fixed HTML rendering)
DecodeLabs Project 3 | AI Recommendation Logic
"""

import sys
import os
import streamlit as st

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from core.recommender import TechStackRecommender

st.set_page_config(
    page_title="Tech Stack Recommender · DecodeLabs",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; background-color: #0e0f11; color: #e8e6e1; }
.stApp { background: #0e0f11; }
section[data-testid="stSidebar"] { background: #141518; border-right: 1px solid #2a2b2f; }
section[data-testid="stSidebar"] * { color: #e8e6e1 !important; }

.header-banner {
    background: linear-gradient(135deg, #141518 0%, #1a1b20 50%, #141518 100%);
    border: 1px solid #2a2b2f; border-left: 4px solid #f5a623;
    border-radius: 4px; padding: 28px 36px; margin-bottom: 28px;
    position: relative; overflow: hidden;
}
.header-banner::before {
    content: ''; position: absolute; top: 0; right: 0; bottom: 0; width: 40%;
    background: repeating-linear-gradient(45deg, transparent, transparent 8px, rgba(245,166,35,0.03) 8px, rgba(245,166,35,0.03) 16px);
}
.header-title { font-family: 'Syne', sans-serif; font-size: 2.1rem; font-weight: 800; color: #f5f4f0; margin: 0 0 6px 0; }
.header-subtitle { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #f5a623; letter-spacing: 2px; text-transform: uppercase; margin: 0; }

.pipeline-row { display: flex; gap: 8px; margin-bottom: 24px; }
.pipeline-step { flex: 1; background: #141518; border: 1px solid #2a2b2f; border-top: 3px solid #f5a623; border-radius: 4px; padding: 14px 16px; text-align: center; font-family: 'JetBrains Mono', monospace; }
.step-num { font-size: 0.65rem; color: #f5a623; letter-spacing: 2px; text-transform: uppercase; display: block; margin-bottom: 4px; }
.step-name { font-size: 0.82rem; font-weight: 600; color: #e8e6e1; }

.result-card { background: #141518; border: 1px solid #2a2b2f; border-radius: 4px; padding: 24px 28px; margin-bottom: 16px; }
.result-card.rank-1 { border-left: 4px solid #f5a623; }
.result-card.rank-2 { border-left: 4px solid #b0b0b0; }
.result-card.rank-3 { border-left: 4px solid #cd7f32; }
.result-card.rank-other { border-left: 4px solid #333; }
.result-rank { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase; color: #666; margin-bottom: 6px; }
.result-role { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800; color: #f5f4f0; margin-bottom: 14px; }

.score-label { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; color: #555; margin-bottom: 4px; }
.score-high { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #50c878; }
.score-mid  { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #f5a623; }
.score-low  { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #ff6b6b; }
.score-pct  { font-size: 1rem; color: #555; font-weight: 400; }

.bar-wrap { background: #1e1f24; border-radius: 2px; height: 6px; margin: 8px 0 16px; overflow: hidden; }
.bar-high { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #50c878, #3daf64); }
.bar-mid  { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #f5a623, #e0921a); }
.bar-low  { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #ff6b6b, #e05555); }

.sec-label { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; color: #555; margin: 10px 0 6px; }
.tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 8px; }
.tag-m { background: rgba(80,200,120,0.12); border: 1px solid rgba(80,200,120,0.4); color: #50c878; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; padding: 4px 10px; border-radius: 2px; }
.tag-r { background: rgba(100,140,255,0.08); border: 1px solid rgba(100,140,255,0.25); color: #6e8eff; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; padding: 4px 10px; border-radius: 2px; }
.tag-u { background: rgba(245,166,35,0.12); border: 1px solid rgba(245,166,35,0.35); color: #f5a623; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; padding: 4px 10px; border-radius: 2px; }
.no-match { color: #555; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; font-style: italic; }

.stats-row { display: flex; gap: 10px; margin-bottom: 20px; }
.stat-box { flex: 1; background: #141518; border: 1px solid #2a2b2f; border-radius: 4px; padding: 14px; text-align: center; font-family: 'JetBrains Mono', monospace; }
.stat-num { font-size: 1.6rem; font-weight: 700; color: #f5a623; display: block; }
.stat-desc { font-size: 0.65rem; color: #666; letter-spacing: 1px; text-transform: uppercase; }

.empty-state { background: #141518; border: 1px dashed #2a2b2f; border-radius: 4px; padding: 48px; text-align: center; color: #555; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; line-height: 1.8; }

.stButton > button { background: #f5a623 !important; color: #0e0f11 !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important; font-size: 0.82rem !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; border: none !important; border-radius: 3px !important; padding: 10px 28px !important; width: 100% !important; }
.stButton > button:hover { background: #e09510 !important; box-shadow: 0 0 20px rgba(245,166,35,0.3) !important; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
hr { border-color: #2a2b2f !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_engine():
    return TechStackRecommender(os.path.join(ROOT, "data", "raw_skills.csv"))

engine = load_engine()


def card_html(r) -> str:
    """Build one result card as a safe HTML string."""
    if r.score >= 0.5:
        sc, bc = "score-high", "bar-high"
    elif r.score >= 0.25:
        sc, bc = "score-mid", "bar-mid"
    else:
        sc, bc = "score-low", "bar-low"

    bw = min(int(r.score * 160), 100)
    medals = {1: "&#127941; RANK 01", 2: "&#129352; RANK 02", 3: "&#129353; RANK 03"}
    rl = medals.get(r.rank, f"# RANK {r.rank:02d}")
    rc = f"rank-{r.rank}" if r.rank <= 3 else "rank-other"

    if r.matched_skills:
        mt = "".join(f'<span class="tag-m">&#10003; {s}</span>' for s in r.matched_skills)
    else:
        mt = '<span class="no-match">indirect pattern match</span>'

    rt = "".join(f'<span class="tag-r">{s}</span>' for s in r.role_skills[:8])

    return (
        f'<div class="result-card {rc}">'
        f'<div class="result-rank">{rl}</div>'
        f'<div class="result-role">{r.role}</div>'
        f'<div class="score-label">COSINE SIMILARITY SCORE</div>'
        f'<div class="{sc}">{r.score:.4f} <span class="score-pct">({r.match_percent}% match)</span></div>'
        f'<div class="bar-wrap"><div class="{bc}" style="width:{bw}%"></div></div>'
        f'<div class="sec-label">Your Matched Skills</div>'
        f'<div class="tags">{mt}</div>'
        f'<div class="sec-label">Role Requires</div>'
        f'<div class="tags">{rt}</div>'
        f'</div>'
    )


# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    top_n = st.slider("Top N Recommendations", 1, engine.role_count, 3)
    st.markdown("---")
    st.markdown("### 📊 Dataset Stats")
    st.markdown(
        f'<div class="stats-row">'
        f'<div class="stat-box"><span class="stat-num">{engine.role_count}</span><span class="stat-desc">Job Roles</span></div>'
        f'<div class="stat-box"><span class="stat-num">{engine.skill_count}</span><span class="stat-desc">Unique Skills</span></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### 🧮 Algorithm")
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;color:#888;line-height:2;">'
        '<span style="color:#f5a623">TF</span> = count(t,d) / |d|<br>'
        '<span style="color:#f5a623">IDF</span> = log((N+1)/(df+1))+1<br>'
        '<span style="color:#f5a623">cos(θ)</span> = A&#183;B / &#8214;A&#8214;&#8214;B&#8214;'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("DecodeLabs · Project 3 · Batch 2026")


# ── HEADER ──
st.markdown(
    '<div class="header-banner">'
    '<p class="header-subtitle">DecodeLabs &middot; AI Recommendation Logic &middot; Project 3</p>'
    '<h1 class="header-title">&#127919; Tech Stack Recommender</h1>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="pipeline-row">'
    '<div class="pipeline-step"><span class="step-num">Step 01</span><span class="step-name">Ingestion</span></div>'
    '<div class="pipeline-step"><span class="step-num">Step 02</span><span class="step-name">TF-IDF Scoring</span></div>'
    '<div class="pipeline-step"><span class="step-num">Step 03</span><span class="step-name">Sorting</span></div>'
    '<div class="pipeline-step"><span class="step-num">Step 04</span><span class="step-name">Filtering</span></div>'
    '</div>',
    unsafe_allow_html=True,
)


# ── INPUT ──
st.markdown("#### Select Your Skills")
st.markdown("Choose at least **3 skills**. More skills = more precise recommendations.")

c1, c2 = st.columns([4, 1])
with c1:
    selected_skills = st.multiselect(
        "Skills", options=sorted(engine.all_known_skills),
        placeholder="e.g. python, docker, machine learning...",
        label_visibility="collapsed",
    )
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("▶  Run Engine", use_container_width=True)

with st.expander("✏️  Or type skills manually (comma-separated)"):
    manual = st.text_input("Type skills", placeholder="python, aws, kubernetes", label_visibility="collapsed")
    if manual:
        extra = [s.strip().lower() for s in manual.split(",") if s.strip()]
        selected_skills = list(set(selected_skills + extra))
        st.markdown(
            '<div class="tags">' + "".join(f'<span class="tag-u">{s}</span>' for s in selected_skills) + '</div>',
            unsafe_allow_html=True,
        )


# ── RUN ──
if run_btn or (selected_skills and len(selected_skills) >= 3):
    if len(selected_skills) < 3:
        st.warning(f"⚠️  Need at least 3 skills — you entered {len(selected_skills)}. Add {3 - len(selected_skills)} more.")
        st.stop()

    with st.spinner("Running recommendation pipeline..."):
        results = engine.recommend(selected_skills, top_n=top_n)

    st.markdown("---")
    st.markdown("**Your Profile Vector:**")
    st.markdown(
        '<div class="tags">' + "".join(f'<span class="tag-u">{s}</span>' for s in selected_skills) + '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"#### Top {top_n} Career Recommendations")

    if not results or results[0].score == 0.0:
        st.markdown(
            '<div class="empty-state">&#9888; No matches found.<br><br>'
            'Try: <strong>python</strong>, <strong>docker</strong>, <strong>sql</strong>, <strong>react</strong>, <strong>aws</strong></div>',
            unsafe_allow_html=True,
        )
    else:
        for r in results:
            st.markdown(card_html(r), unsafe_allow_html=True)

    with st.expander("📋  View full score table (all roles)"):
        all_r = engine.recommend(selected_skills, top_n=engine.role_count)
        st.dataframe(
            {
                "Rank":           [r.rank for r in all_r],
                "Job Role":       [r.role for r in all_r],
                "Score":          [round(r.score, 4) for r in all_r],
                "Match %":        [f"{r.match_percent}%" for r in all_r],
                "Matched Skills": [", ".join(r.matched_skills) or "—" for r in all_r],
            },
            use_container_width=True, hide_index=True,
        )

else:
    st.markdown(
        f'<div class="empty-state">'
        f'<div style="font-size:2.5rem;margin-bottom:14px;">&#128269;</div>'
        f'Select at least <strong style="color:#f5a623">3 skills</strong> above to run the engine.<br><br>'
        f'<span style="color:#444;">TF-IDF + Cosine Similarity across {engine.role_count} roles &amp; {engine.skill_count} skills</span>'
        f'</div>',
        unsafe_allow_html=True,
    )