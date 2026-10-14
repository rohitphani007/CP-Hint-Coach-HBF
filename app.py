import streamlit as st
from coach import generate_hints
from codeforces import get_recent_struggles

# ── Page config ──────────────────────────────────────────────────────────────────
st.set_page_config(page_title="CP Hint Coach", layout="centered")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; max-width: 780px; }
        .hint-label {
            font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em;
            text-transform: uppercase; color: #888; margin-bottom: 0.35rem;
        }
        a { color: #4a9eff !important; }
    </style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────────
if "hints"          not in st.session_state: st.session_state.hints          = None
if "unlocked_level" not in st.session_state: st.session_state.unlocked_level = 0
if "cf_problems"    not in st.session_state: st.session_state.cf_problems    = []

# ── Header ───────────────────────────────────────────────────────────────────────
st.title("CP Hint Coach")
st.caption("Get just enough help to get unstuck — without reading the editorial.")
st.divider()

# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")

    language = st.selectbox(
        "Language for code skeleton",
        options=["Python", "C++", "Java", "JavaScript", "Go", "Rust", "Kotlin"],
    )

    st.divider()
    st.header("Codeforces")
    st.caption("Fetch problems you recently struggled with.")

    cf_handle = st.text_input("Handle", placeholder="e.g. tourist")

    if st.button("Fetch Recent Struggles", use_container_width=True):
        if not cf_handle.strip():
            st.warning("Enter a Codeforces handle first.")
        else:
            with st.spinner("Fetching from Codeforces..."):
                result = get_recent_struggles(cf_handle.strip())

            if isinstance(result, str):
                st.error(result)
            else:
                st.session_state.cf_problems = result

    if st.session_state.cf_problems:
        st.markdown("**Open a problem, then paste its statement into the main area.**")
        for p in st.session_state.cf_problems:
            st.markdown(
                f"[{p['index']}. {p['name']}]({p['url']})  \n"
                f"<span style='font-size:0.75rem; color:#888;'>{p['verdict']}</span>",
                unsafe_allow_html=True,
            )

# ── Input ────────────────────────────────────────────────────────────────────────
st.subheader("Problem Statement")
problem = st.text_area(
    label="problem_input",
    label_visibility="collapsed",
    placeholder="Paste the full problem statement here...",
    height=220,
)

st.subheader("Your Current Thinking")
st.caption("Optional — describe your approach or paste your code. Better context leads to better hints.")
user_approach = st.text_area(
    label="approach_input",
    label_visibility="collapsed",
    placeholder="What have you tried so far?",
    height=120,
)

# ── Generate ─────────────────────────────────────────────────────────────────────
if st.button("Generate Hint Ladder", use_container_width=True, type="primary"):
    if not problem.strip():
        st.warning("Paste a problem statement first.")
    else:
        st.session_state.unlocked_level = 0
        with st.spinner("Analyzing the problem — this takes 15–25 seconds..."):
            st.session_state.hints = generate_hints(problem, user_approach, language)

st.divider()

# ── Hint Ladder ──────────────────────────────────────────────────────────────────
if st.session_state.hints:
    hints = st.session_state.hints

    st.subheader("Hint Ladder")
    st.caption("Unlock one level at a time. Try to solve it before going deeper.")

    levels = [
        (1, "Hint 1 — Nudge",           "hint_1"),
        (2, "Hint 2 — Key Observation",  "hint_2"),
        (3, "Hint 3 — Approach",         "hint_3"),
        (4, "Hint 4 — Code Skeleton",    "hint_4"),
    ]

    if st.session_state.unlocked_level == 0:
        if st.button("Reveal Hint 1", use_container_width=True):
            st.session_state.unlocked_level = 1
            st.rerun()

    for level_num, label, key in levels:
        if st.session_state.unlocked_level >= level_num:

            with st.container(border=True):
                st.markdown(
                    f"<div class='hint-label'>{label}</div>",
                    unsafe_allow_html=True,
                )
                if key == "hint_4":
                    lang_map = {"c++": "cpp", "javascript": "js"}
                    lang_key = language.lower()
                    st.code(hints[key], language=lang_map.get(lang_key, lang_key))
                else:
                    st.markdown(hints[key])

            if st.session_state.unlocked_level == level_num and level_num < 4:
                st.caption("Take a few minutes with this hint before going deeper.")
                if st.button(f"Still stuck — unlock Hint {level_num + 1}", key=f"unlock_{level_num}"):
                    st.session_state.unlocked_level += 1
                    st.rerun()

# ── Footer ───────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Powered by open-source AI running locally. No data leaves your machine.")
