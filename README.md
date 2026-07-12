# AI Resume Ranking System

An AI-powered resume screening application that helps recruiters evaluate and rank candidates based on their suitability for a job description.

The system combines transformer-based Natural Language Processing (NLP), semantic relevance scoring, skill matching and generative AI to provide a more meaningful evaluation than traditional keyword-based resume filtering.

---

## Live Demo

**Try the deployed application here:**

**https://resume-ai-ranker.streamlit.app/**

The screenshots below showcase some of the application's core features. For the complete interactive experience, including resume uploads, candidate ranking, sentence-level explanations, and AI-generated hiring summaries, visit the live application.

---

# Application Preview

## Home Page

<img src="images/RAIR1.png" width="900">

---

## Upload Job Description & Resumes

<img src="images/RAIR2.png" width="900">

---

## Candidate Ranking

<img src="images/RAIR3.png" width="900">

---

## Additional Candidate Results

<img src="images/RAIR4.png" width="900">

---

## AI Hiring Summary

<img src="images/RAIR6.png" width="900">

<img src="images/RAIR7.png" width="900">

---

## Features

### Resume Upload and Processing

* Upload multiple PDF resumes simultaneously
* Extract text from resumes using **PyMuPDF**
* Automatically prepare resumes for semantic analysis

### Intelligent Candidate Ranking

Instead of relying solely on keyword matching, the application uses a **CrossEncoder transformer model (`ms-marco-MiniLM-L6-v2`)** to evaluate the semantic relationship between each resume and the job description.

Unlike traditional embedding-based similarity methods, the CrossEncoder jointly processes the resume and job description before producing a relevance score, allowing it to better understand context, wording, and the relationship between both documents.

Each candidate receives an overall ranking based on:

* Semantic relevance score
* Skill matching score

These scores are combined to produce a final candidate ranking.

### Explainable Results

For every candidate, the application provides:

* Final ranking score
* Semantic relevance score
* Skill matching score
* Matched skills
* Missing skills
* Sentence-level explanations showing which resume sections best match the job description

### AI Hiring Summary

Google Gemini is used to generate recruiter-style hiring reports based on the candidate's resume and ranking results.

Each AI summary includes:

* Overall candidate fit
* Key strengths
* Potential skill gaps
* Hiring recommendation

---

## Tech Stack

### Python

Used to implement the application's backend logic, resume processing pipeline, ranking algorithm, and AI integration.

### Streamlit

Provides the interactive web interface for:

* Uploading resumes
* Entering job descriptions
* Displaying ranked candidates
* Viewing explanations
* Generating AI hiring summaries

### Sentence Transformers (CrossEncoder)

The project uses the **CrossEncoder `ms-marco-MiniLM-L6-v2`** model from Sentence Transformers.

Unlike cosine similarity approaches that compare two independently generated embeddings, the CrossEncoder jointly processes the resume and job description and directly predicts a semantic relevance score. This generally produces more accurate rankings because the model evaluates both texts together instead of comparing them after separate encoding.

### Google Gemini API

Used to generate structured recruiter-style hiring summaries from the ranking results and extracted resume content.

### PyMuPDF

Extracts machine-readable text from uploaded PDF resumes.

### NumPy

Used for numerical computations and score normalization within the ranking pipeline.

---

## Project Structure

```text
resume-ai/
│
├── app.py                 # Streamlit application
├── utils.py               # Resume processing and ranking logic
├── gemini.py              # Google Gemini integration
├── requirements.txt       # Project dependencies
├── README.md
└── images/
    ├── RAIR1.png
    ├── RAIR2.png
    ├── RAIR3.png
    ├── RAIR4.png
    ├── RAIR5.png
    ├── RAIR6.png
    └── RAIR7.png
```

---

## Future Improvements

* Support additional resume formats (DOCX, TXT)
* Recruiter feedback-based ranking refinement
* Candidate comparison dashboard
* Batch AI summary generation
* Expanded skill extraction using larger domain-specific skill databases
