# Automated Personal Recruiter

An AI-powered tool that parses a PDF resume and generates a tailored cover letter for any job description.

This project solves the "blank page problem" when applying for jobs. It uses **RAG (Retrieval-Augmented Generation)** to map specific skills and experiences from a resume to the requirements of a target job description.

## ⚡️ Tech Stack

* **Framework:** [LangChain](https://www.langchain.com/)
* **Inference Engine:** [Groq](https://groq.com/) (Llama 3 8B by default)

  You can override the default model by setting `GROQ_MODEL` in the `.env` file
  or your shell environment; choose a model you have access to via your Groq
  account.
* **Document Processing:** pypdf
* **Interface:** Streamlit

## 🎯 Features

* **Resume Parsing:** Extracts text from PDF resumes automatically using `pypdf`.
* **Contextual Matching:** Maps candidate skills to job requirements using LLM reasoning.
* **Fast Generation:** Generates a professional draft in seconds using Groq's LPU.
* **Error Feedback:** Authentication or model issues surface directly in the Streamlit interface.

## 🚀 Setup & Run

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd personal-recruiter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Keys:**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=gsk_...
    ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

> ⚠️ If you encounter a decommissioned model error or a *model not found* error,
> edit `app.py` (or set `GROQ_MODEL` in the `.env` file) and choose a
> currently supported model that your Groq plan permits.