import fitz
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

SKILL_DB = [
    "python", "java", "c++", "sql",
    "machine learning", "deep learning",
    "pandas", "numpy", "tensorflow",
    "pytorch", "docker", "aws",
    "flask", "fastapi", "react",
    "git", "linux"
]


def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in doc:
        text += page.get_text()

    return text


def extract_skills(text):
    text = text.lower()
    return list(set([s for s in SKILL_DB if s in text]))


def get_embedding(text):
    return model.encode(text)


def calculate_similarity(vec1, vec2):
    return float(cosine_similarity([vec1], [vec2])[0][0]) * 100


def split_sentences(text):
    return [s.strip() for s in re.split(r'[.\n]', text) if s.strip()]


def sentence_similarity(resume_text, job_text):

    resume_sentences = split_sentences(resume_text)
    job_sentences = split_sentences(job_text)

    if not resume_sentences or not job_sentences:
        return []

    resume_embeddings = model.encode(resume_sentences)
    job_embeddings = model.encode(job_sentences)

    matches = []

    for i, r_vec in enumerate(resume_embeddings):
        for j, j_vec in enumerate(job_embeddings):

            score = cosine_similarity([r_vec], [j_vec])[0][0] * 100

            if score > 60:
                matches.append({
                    "resume_sentence": resume_sentences[i],
                    "job_sentence": job_sentences[j],
                    "score": round(score, 2)
                })

    return sorted(matches, key=lambda x: x["score"], reverse=True)[:5]


def rank_resumes(resumes, job_text):

    job_skills = extract_skills(job_text)
    job_vec = get_embedding(job_text)

    results = []

    for name, text in resumes:

        resume_vec = get_embedding(text)
        resume_skills = extract_skills(text)

        semantic_score = calculate_similarity(resume_vec, job_vec)

        matched = set(resume_skills) & set(job_skills)

        skill_score = (len(matched) / len(job_skills) * 100) if job_skills else 0

        final_score = (semantic_score * 0.7) + (skill_score * 0.3)

        results.append({
            "name": name,
            "semantic_score": round(semantic_score, 2),
            "skill_score": round(skill_score, 2),
            "final_score": round(final_score, 2),
            "matched_skills": list(matched),
            "missing_skills": list(set(job_skills) - set(resume_skills)),
            "explanation": sentence_similarity(text, job_text),
            "resume_text": text
        })

    return sorted(results, key=lambda x: x["final_score"], reverse=True)