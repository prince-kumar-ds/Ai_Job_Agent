import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Priority: Streamlit secrets → fallback to .env
api_key = None

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

# ❌ Fail early if missing
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Set it in Streamlit secrets or .env")

# ✅ Initialize model safely
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=api_key
)


def improve_resume(resume_text, job_description):

    prompt = f"""
You are an expert AI resume coach.

Improve this resume based on the job description.

Focus on:
- Better bullet points
- Add missing skills
- ATS-friendly

Resume:
{resume_text}

Job Description:
{job_description}

Return improved bullet points only.
"""

    try:
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"


def generate_cover_letter(resume_text, job_description):

    prompt = f"""
Write a professional cover letter.

Make it:
- concise
- personalized
- impactful

Resume:
{resume_text}

Job Description:
{job_description}
"""

    try:
        response = model.invoke(prompt)
    
        return response.content
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

