import streamlit as st
import os
from pypdf import PdfReader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# error types from groq for cleaner messages
from groq import AuthenticationError, BadRequestError, NotFoundError

# Loading my keys
load_dotenv()

# --- CONFIGURATION --- #
# The Groq model to use. You can override via environment variable if you
# don't want to edit this file directly. Pick one you have access to via
# your Groq console.
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def get_pdf_text(pdf_file):
    """
    My helper function to extract raw text from the uploaded PDF.
    """
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_cover_letter(cv_text, job_desc):
    """
    This is where the magic happens. 
    I'm instructing the LLM to map my skills to the job requirements.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Please set it in your .env file.")

    llm = ChatGroq(
        temperature=0.7, 
        model_name=GROQ_MODEL, 
        api_key=api_key
    )
    
    template = """
    You are an expert career coach acting on my behalf.
    I need a professional cover letter connecting my CV to a Job Description.
    
    MY CV CONTENT:
    {cv}
    
    TARGET JOB DESCRIPTION:
    {job}
    
    MY INSTRUCTIONS:
    1. Hook the reader immediately.
    2. Map my specific skills from the CV to the requirements in the Job Description.
    3. Keep it under 300 words.
    4. The tone should be confident but professional.
    5. Sign off as "Sampath Krishna".
    
    OUTPUT:
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    try:
        return chain.invoke({"cv": cv_text, "job": job_desc})
    except AuthenticationError:
        raise ValueError("Failed to authenticate with Groq. Check GROQ_API_KEY.")
    except NotFoundError:
        raise ValueError(
            "The specified model does not exist or you lack access. "
            "Verify GROQ_MODEL and your Groq plan."
        )
    except BadRequestError as err:
        msg = str(err)
        if "decommissioned" in msg or "no longer supported" in msg:
            raise ValueError(
                "Requested model is unavailable; update GROQ_MODEL to a current model (e.g. 'llama3-8b')."
            )
        raise

# --- MY STREAMLIT UI --- #
st.set_page_config(page_title="Sampath's AI Recruiter", page_icon="🚀")

st.title("🚀 Automated Personal Recruiter")
st.caption(f"Built by Sampath Krishna | Powered by {GROQ_MODEL}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. My Resume")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

with col2:
    st.subheader("2. The Job")
    job_desc = st.text_area("Paste the JD here", height=300)

if st.button("Generate Cover Letter"):
    if uploaded_file and job_desc:
        with st.spinner("Analyzing the match..."):
            # Step 1: Read my CV
            cv_text = get_pdf_text(uploaded_file)
            
            # Step 2: Generate the letter
            try:
                cover_letter = generate_cover_letter(cv_text, job_desc)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success("Draft Generated!")
                st.subheader("My Personalized Cover Letter")
                st.text_area("Copy this:", value=cover_letter, height=400)
    else:
        st.error("I need both a CV and a Job Description to proceed.")