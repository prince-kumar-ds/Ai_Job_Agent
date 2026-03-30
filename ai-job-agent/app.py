import streamlit as st
import os

from api.fetch_jobs import fetch_jobs
from processing.clean_jobs import process_jobs
from processing.resume_parser import extract_resume
from processing.matcher import match_job
from processing.skill_extractor import load_keywords, create_keyword_embeddings
from llm_module.llm_engine import improve_resume, generate_cover_letter

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="AI Job Hunter", layout="wide")
st.title("🚀 AI Job Hunter")

# ========================
# SESSION STATE INIT
# ========================
if "results" not in st.session_state:
    st.session_state["results"] = None

if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = None

# ========================
# SIDEBAR INPUT
# ========================
st.sidebar.header("📄 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF Resume",
    type=["pdf"],
    help="Max size: 5MB"
)

st.sidebar.header("🔎 Job Filters")

role = st.sidebar.text_input("💼 Job Role", "Data Scientist")
location = st.sidebar.text_input("📍 Location", "Delhi NCR")

date_posted = st.sidebar.selectbox(
    "📅 Date Posted",
    ["all", "today", "3days", "week", "month"]
)

num_pages = st.sidebar.slider(
    "📄 Number of Pages (API cost ⚠️)",
    min_value=1,
    max_value=5,
    value=1
)

remote_only = st.sidebar.checkbox("🏠 Remote Only")

employment_type = st.sidebar.multiselect(
    "💼 Employment Type",
    ["FULLTIME", "PARTTIME", "CONTRACTOR", "INTERN"]
)

search_clicked = st.sidebar.button("🔍 Search Jobs")

# ========================
# SEARCH LOGIC
# ========================
if uploaded_file and search_clicked:

    # File size check
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error("File too large. Max 5MB allowed.")
        st.stop()

    # Save resume
    os.makedirs("data", exist_ok=True)
    with open("data/resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Extract text
    resume_text = extract_resume("data/resume.pdf")

    # Load keyword model
    keywords = load_keywords()
    keyword_embeddings = create_keyword_embeddings(keywords)

    # Fetch jobs
    raw_data = fetch_jobs(
        role,
        location,
        date_posted,
        num_pages,
        remote_only,
        employment_type
    )

    jobs = process_jobs(raw_data)

    results = []

    for job in jobs:
        job_text = (job.get("title") or "") + " " + (job.get("description") or "")

        if not job_text.strip():
            continue

        result = match_job(
            resume_text,
            job_text,
            keywords,
            keyword_embeddings
        )

        results.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "score": result.get("score", 0),
            "missing": result.get("missing", []),
            "link": job.get("job_apply_link") or job.get("link") or "#",
            "description": job.get("description", "")
        })

    # Filter + sort
    results = [job for job in results if job["score"] > 40]
    results = sorted(results, key=lambda x: x["score"], reverse=True)[:10]

    # Save to session
    st.session_state["results"] = results
    st.session_state["resume_text"] = resume_text

# ========================
# DISPLAY RESULTS
# ========================
if st.session_state["results"]:

    results = st.session_state["results"]
    resume_text = st.session_state["resume_text"]

    st.subheader("🎯 Job Matches")

    for i, job in enumerate(results):

        with st.container():
            col1, col2 = st.columns([3, 1])

            # LEFT SIDE
            with col1:
                st.markdown(f"### {job['title']}")
                st.write(f"🏢 {job['company']}")

                st.progress(job["score"] / 100)
                st.markdown(f"**📊 Match Score:** `{job['score']}%`")

                # Match level
                if job["score"] >= 85:
                    st.success("🔥 Strong Match")
                elif job["score"] >= 70:
                    st.info("✅ Good Match")
                else:
                    st.warning("⚠️ Moderate Match")

                # Missing skills
                if job["missing"]:
                    st.markdown(
                        f"**⚠️ Missing Skills:** `{', '.join(job['missing'])}`"
                    )

                # Apply link
                if job["link"] and job["link"] != "#":
                    st.markdown(
                        f'<a href="{job["link"]}" target="_blank">🔗 Apply Now</a>',
                        unsafe_allow_html=True
                    )
                else:
                    st.write("🚫 No apply link available")

            # RIGHT SIDE (AI)
            with col2:

                # Init AI state
                if f"ai_{i}" not in st.session_state:
                    st.session_state[f"ai_{i}"] = None

                if st.button("✨ AI Help", key=f"btn_{i}"):

                    if st.session_state[f"ai_{i}"] is None:
                        with st.spinner("Generating..."):
                            try:
                                ai_resume = improve_resume(
                                    resume_text,
                                    job["description"]
                                )

                                cover_letter = generate_cover_letter(
                                    resume_text,
                                    job["description"]
                                )

                                st.session_state[f"ai_{i}"] = (ai_resume, cover_letter)

                            except Exception as e:
                                st.session_state[f"ai_{i}"] = (f"Error: {e}", "")

                # Show AI output if exists
                if st.session_state[f"ai_{i}"]:
                    ai_resume, cover_letter = st.session_state[f"ai_{i}"]

                    st.markdown("#### 🧠 Resume Tips")
                    st.write(ai_resume)

                    st.markdown("#### ✉️ Cover Letter")
                    st.write(cover_letter)

        st.divider()

# ========================
# EMPTY STATE
# ========================
else:
    st.info("👈 Upload resume and click 'Search Jobs' to begin")



# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 16px 0 8px 0; color:#94a3b8; font-size:13px;">
    Built by <b style="color:#f97316">Prince Kumar</b> · Ai/Ml Enthusiast · 📞 9971287050<br>
    <a href="https://www.linkedin.com/in/prince-datascientist" target="_blank" style="color:#f97316; text-decoration:none;">LinkedIn</a> &nbsp;·&nbsp;
    <a href="https://github.com/prince-kumar-ds" target="_blank" style="color:#f97316; text-decoration:none;">GitHub</a> &nbsp;·&nbsp;
""", unsafe_allow_html=True)
