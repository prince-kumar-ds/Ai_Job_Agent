import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# ✅ Use stable model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
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

