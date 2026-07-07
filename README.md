# AI Resume Ranking System

An AI-powered resume screening application that helps recruiters evaluate and rank candidates based on their suitability for a job description.

The system uses Natural Language Processing (NLP), transformer-based semantic analysis, skill matching, and Generative AI to provide a more meaningful evaluation than traditional keyword-based resume filtering.

## Live Demo

Try the application here:

https://resume-ai-ranker.streamlit.app/

## Features

### Resume Upload and Processing

* Upload multiple resumes in PDF format
* Automatically extract resume content
* Analyze multiple candidates simultaneously

### Intelligent Candidate Ranking

* Rank candidates based on their relevance to a given job description
* Generate an overall compatibility score
* Compare candidates using both technical skills and contextual similarity

### Explainable Results

For each candidate, the system provides:

* Overall ranking score
* Semantic relevance score
* Skill matching score
* Matched skills
* Missing skills
* Sentence-level explanations showing relevant resume sections

### AI-Generated Hiring Summary

Using Gemini, recruiters can generate a structured candidate evaluation containing:

* Overall candidate fit
* Key strengths
* Potential skill gaps
* Hiring recommendation

## Technical Approach

### 1. Resume Text Extraction

Uploaded PDF resumes are converted into machine-readable text using **PyMuPDF**, allowing the system to analyze the candidate's experience, skills, and qualifications.

### 2. Skill-Based Analysis

The application extracts technical skills from both the resume and job description using a predefined skill database.

This provides a direct comparison of required and available skills, helping identify:

* Skills the candidate already possesses
* Skills that may be missing

### 3. Transformer-Based Semantic Matching

Instead of relying only on keyword overlap, the system uses a **CrossEncoder transformer model** to evaluate the relationship between the resume and job description.

The model reads both texts together and produces a relevance score based on contextual meaning.

For example, it can recognize that experience with "building neural networks using PyTorch" is relevant to a requirement for "deep learning experience" even when the exact wording differs.

### 4. Candidate Ranking

The final ranking score combines:

* Semantic relevance between resume and job description
* Technical skill compatibility

Candidates are then sorted according to their overall suitability.

### 5. Generative AI Assistance

The Gemini API is used to provide additional recruiter-style analysis based on the ranking results.

The AI summary acts as an interpretation layer, helping users understand why a candidate may or may not be suitable.

## Tech Stack

### Python

The core programming language used for:

* Resume processing
* NLP model integration
* Scoring logic
* Application backend

### Streamlit

A Python-based web framework used to create the interactive user interface.

Streamlit allows the application to:

* Accept resume uploads
* Display rankings dynamically
* Provide interactive explanations and AI-generated summaries

### Sentence Transformers / CrossEncoder

Transformer-based NLP models used for semantic understanding.

The project uses a CrossEncoder model (`ms-marco-MiniLM-L6-v2`) which evaluates pairs of text inputs together:

```
(Resume, Job Description) → Relevance Score
```

Unlike traditional keyword matching, this approach captures relationships between concepts and evaluates meaning from context.

### Google Gemini API

Used for Generative AI capabilities.

Gemini converts ranking data into structured hiring insights, including:

* Candidate strengths
* Areas for improvement
* Hiring recommendations

### PyMuPDF

A PDF processing library used to extract text from uploaded resumes.

### NumPy and Scikit-learn

Used for:

* Numerical operations
* Similarity calculations
* Supporting machine learning workflows

## Project Structure

```text
resume-ai/
│
├── app.py              # Streamlit interface
├── utils.py            # Resume processing and ranking pipeline
├── gemini.py           # Gemini API integration
├── requirements.txt    # Dependencies
└── README.md
```

## Future Improvements

* Automatic skill extraction using LLMs
* Support for additional document formats
* More advanced resume section detection
* Recruiter feedback-based ranking improvements
* Candidate comparison dashboard

## Author

Built as an AI/NLP portfolio project exploring practical applications of transformer models, semantic search, and Generative AI.
