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
