# 📄 AI Resume Ranking System

An AI-powered resume screening and ranking system that evaluates candidates against job descriptions using Natural Language Processing (NLP), transformer-based models, and Large Language Models (LLMs).

The system analyzes uploaded resumes, compares them with job requirements, ranks candidates based on contextual relevance and technical skills, provides explainable matching insights, and generates AI-assisted hiring summaries.

---

# 🚀 Features

## Resume Analysis

- Upload multiple resumes in PDF format
- Automatically extract resume text
- Analyze multiple candidates simultaneously

## AI-Powered Ranking

- Semantic understanding using Sentence Transformers
- Technical skill matching
- Weighted candidate scoring
- Candidate ranking from highest to lowest fit

## Explainable AI

- Sentence-level resume and job description matching
- Cross-Encoder based relevance scoring
- Shows why a candidate matches specific requirements

## LLM Hiring Assistant

- Generate recruiter-style candidate summaries using Google Gemini
- Provides:
  - Overall fit assessment
  - Candidate strengths
  - Potential gaps
  - Hiring recommendation

## User Interface

- Interactive Streamlit dashboard
- Candidate comparison
- Sort results by:
  - Final Score
  - Semantic Score
  - Skill Score

---

# 🧠 How It Works

The system uses a multi-stage NLP pipeline.

```
PDF Resume
     |
     v
Text Extraction
(PyMuPDF)
     |
     v
Semantic Analysis
(Sentence Transformer)
     |
     v
Skill Matching
     |
     v
Candidate Ranking
     |
     v
Cross Encoder Explanation
     |
     v
Gemini AI Summary
```

---

# 1. Resume Text Extraction

Uploaded PDF resumes are processed using **PyMuPDF**, which extracts the raw text content from each document.

The extracted text is then used for NLP analysis.

---

# 2. Semantic Similarity Matching

The system uses the Sentence Transformer model:

```
all-MiniLM-L6-v2
```

Sentence Transformers convert text into dense numerical representations called embeddings.

These embeddings capture contextual meaning rather than relying only on exact keyword matches.

For example:

```
"Built machine learning models using Python"

and

"Experience developing ML solutions with Python"
```

can be recognized as semantically similar even though the wording differs.

The similarity between resume and job description embeddings is calculated using cosine similarity.

This produces the semantic similarity score.

---

# 3. Skill Matching

The application extracts technical skills from both resumes and job descriptions.

Currently supported examples include:

- Python
- Java
- SQL
- Machine Learning
- Deep Learning
- TensorFlow
- PyTorch
- Docker
- AWS
- React
- Git
- Linux

The skill score is calculated based on overlapping skills.

---

# 4. Candidate Ranking

The final candidate score combines semantic understanding and technical skill matching.

```
Final Score =

70% Semantic Similarity

+

30% Skill Match
```

This balances:

- Understanding of the candidate's overall experience
- Presence of required technical skills

---

# 5. Cross-Encoder Reranking

For explainability, the system uses a Cross-Encoder model:

```
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Unlike embedding models that encode two texts separately, a Cross-Encoder receives both pieces of text together:

```
Resume sentence
        +
Job requirement sentence
```

and directly predicts their relevance.

This allows more accurate sentence-level comparisons.

For example:

```
Resume:
"Developed applications using TensorFlow"

Job:
"Experience with TensorFlow required"
```

The Cross-Encoder can identify this as a strong match.

It is used to generate the "Why this matches" explanations shown to users.

---

# 6. AI Hiring Summary

The application integrates Google Gemini to generate a recruiter-style evaluation.

Gemini receives:

- Resume content
- Job description
- Candidate scores
- Matched skills
- Missing skills

and produces a structured summary containing:

- Overall candidate fit
- Strengths
- Potential weaknesses
- Hiring recommendation

---

# 🛠️ Tech Stack

## Programming

- Python

## Frontend

- Streamlit

## NLP / AI

- Sentence Transformers
- Cross Encoder
- Google Gemini API

## Machine Learning

- scikit-learn
- NumPy

## Document Processing

- PyMuPDF

---

# 📁 Project Structure

```
resume-ai/
│
├── app.py              # Streamlit user interface
├── utils.py            # NLP pipeline and ranking logic
├── gemini.py           # Gemini AI integration
├── requirements.txt    # Python dependencies
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/resume-ai.git
```

Navigate into the project:

```bash
cd resume-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Setup

Create a Gemini API key through Google AI Studio.

Set the environment variable:

### Windows PowerShell

```powershell
setx RESUME_AI_RANKER_API_KEY "YOUR_API_KEY"
```

Restart your terminal after creating the variable.

---

# ▶️ Running the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📌 Usage

1. Enter a job description.
2. Upload one or more PDF resumes.
3. Click **Rank Candidates**.
4. Review:
   - Candidate ranking
   - Final score
   - Semantic score
   - Skill score
   - Matched skills
   - Missing skills
   - Explanation matches
5. Generate an AI hiring summary for individual candidates.

---

# 🔮 Future Improvements

Possible future enhancements:

- Larger skill database
- Automatic skill extraction using LLMs
- OCR support for scanned resumes
- Resume section detection
- ATS compatibility scoring
- Export results to PDF/Excel
- Recruiter analytics dashboard
- Candidate comparison view
- Multi-language resume support

---

# 📸 Screenshots

Add screenshots after deployment:

```
Home Interface

[Insert screenshot]


Candidate Ranking

[Insert screenshot]


AI Hiring Summary

[Insert screenshot]
```

---

# 🌐 Live Demo

Coming soon.

---

# 📄 License

This project is created for educational and portfolio purposes.