import streamlit as st
import os
import PyPDF2
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Loading my keys
load_dotenv()

# --- CONFIGURATION --- #
# I'm using Llama 3 8B here because it's fast and sufficient for drafting
GROQ_MODEL = "llama3-8b-8192"

def get_pdf_text(pdf_file):
    """
    My helper function to extract raw text from the uploaded PDF.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_cover_letter(cv_text, job_desc):
    """
    This is where the magic happens. 
    I'm instructing the LLM to map my skills to the job requirements.
    """
    llm = ChatGroq(
        temperature=0.7, 
        model_name=GROQ_MODEL, 
        api_key=os.getenv("GROQ_API_KEY")
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
    
    return chain.invoke({"cv": cv_text, "job": job_desc})

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
            cover_letter = generate_cover_letter(cv_text, job_desc)
            
            st.success("Draft Generated!")
            st.subheader("My Personalized Cover Letter")
            st.text_area("Copy this:", value=cover_letter, height=400)
    else:
        st.error("I need both a CV and a Job Description to proceed.")