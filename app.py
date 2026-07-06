import streamlit as st
import time
from utils import extract_text_from_pdf, rank_resumes
from gemini import generate_summary

st.set_page_config(page_title="Resume Ranker", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>

/* Layout container */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

/* Hero */
.hero {
    padding: 24px;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(100,149,237,0.15), rgba(147,112,219,0.12));
    border: 1px solid rgba(150,150,150,0.2);
    margin-top: 20px;
    margin-bottom: 20px;
}

/* Card */
div.card {
    padding: 16px;
    border-radius: 12px;
    border: 1px solid rgba(150,150,150,0.15);
    margin-bottom: 12px;

    background: #f3f5f7 !important;
}

/* force ALL text inside card to be readable */
div.card * {
    color: #111827 !important;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .card {
        background-color: rgba(30,30,30,0.55);
    }
}

/* Skill chips */
.skill-chip {
    display: inline-block;
    padding: 4px 10px;
    margin: 3px;
    border-radius: 999px;
    font-size: 12px;
    background-color: rgba(100,149,237,0.15);
    border: 1px solid rgba(100,149,237,0.35);
}

.missing-chip {
    display: inline-block;
    padding: 4px 10px;
    margin: 3px;
    border-radius: 999px;
    font-size: 12px;
    background-color: rgba(255,99,71,0.12);
    border: 1px solid rgba(255,99,71,0.25);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #6495ED, #7C3AED);
    color: white;
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 15px;
    font-weight: 600;
    border: none;
    transition: 0.2s ease-in-out;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(135deg, #5a85e6, #6d28d9);
    cursor: pointer;
}

/* Section label */
.section {
    font-size: 13px;
    font-weight: 600;
    opacity: 0.75;
    margin-top: 10px;
    margin-bottom: 6px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h2 style="margin-bottom:6px;">AI Resume Ranking System</h2>
    <p style="margin:0; opacity:0.8;">
        Upload resumes and compare candidates using semantic AI + skill matching.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    show_explanations = st.toggle("Show explanations", value=True)

    sort_mode = st.selectbox(
        "Sort results by",
        ["Final Score", "Semantic Score", "Skill Score"]
    )

# ---------------- INPUT ----------------
job_text = st.text_area("Job Description")

uploaded_files = st.file_uploader(
    "Upload resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

# ---------------- STATE ----------------
if "results" not in st.session_state:
    st.session_state.results = None

if "summaries" not in st.session_state:
    st.session_state.summaries = {}

if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# ---------------- RUN ----------------
if st.button("Rank Candidates"):

    if not job_text.strip():
        st.error("Please enter a job description")
        st.stop()

    if not uploaded_files:
        st.error("Please upload resumes")
        st.stop()

    resumes = []

    with st.spinner("Analyzing resumes..."):
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resumes.append((file.name, text))

        st.session_state.results = rank_resumes(resumes, job_text)
        st.session_state.summaries = {}

# ---------------- RESULTS ----------------
if st.session_state.results:

    results = st.session_state.results

    if sort_mode == "Semantic Score":
        results = sorted(results, key=lambda x: x["semantic_score"], reverse=True)
    elif sort_mode == "Skill Score":
        results = sorted(results, key=lambda x: x["skill_score"], reverse=True)
    else:
        results = sorted(results, key=lambda x: x["final_score"], reverse=True)

    st.subheader("Ranked Candidates")

    for i, r in enumerate(results):

        st.markdown(f"""
        <div class="card">
            <h3 style="margin-bottom:6px;">#{i+1} {r['name']}</h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        col1.metric("Final Score", f"{r['final_score']}%")
        col2.metric("Semantic Score", f"{r['semantic_score']}%")
        col3.metric("Skill Score", f"{r['skill_score']}%")

        st.markdown('<div class="section">Matched Skills</div>', unsafe_allow_html=True)
        if r["matched_skills"]:
            st.markdown(
                " ".join([f"<span class='skill-chip'>{s}</span>" for s in r["matched_skills"]]),
                unsafe_allow_html=True
            )
        else:
            st.write("None")

        st.markdown('<div class="section">Missing Skills</div>', unsafe_allow_html=True)
        if r["missing_skills"]:
            st.markdown(
                " ".join([f"<span class='missing-chip'>{s}</span>" for s in r["missing_skills"]]),
                unsafe_allow_html=True
            )
        else:
            st.write("None")

        if show_explanations and r["explanation"]:
            with st.expander("Why this matches"):
                for item in r["explanation"]:
                    st.write(f"Resume: {item['resume_sentence']}")
                    st.write(f"Job: {item['job_sentence']}")
                    st.write(f"Score: {item['score']}%")
                    st.divider()

        # ---------------- AI BUTTON ----------------
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

        if st.button(
            "Generate AI Summary",
            key=f"btn_{i}",
            use_container_width=True
        ):

            now = time.time()

            if now - st.session_state.last_call < 25:
                st.warning("Please wait before generating another summary.")
                st.stop()

            st.session_state.last_call = now

            if i not in st.session_state.summaries:
                with st.spinner("Generating AI summary..."):
                    try:
                        st.session_state.summaries[i] = generate_summary(
                            r["resume_text"],
                            job_text,
                            r
                        )
                    except:
                        st.session_state.summaries[i] = "AI unavailable."

        if i in st.session_state.summaries:
            with st.expander("AI Summary", expanded=True):
                st.markdown(st.session_state.summaries[i])

        st.divider()