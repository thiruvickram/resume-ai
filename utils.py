import fitz
import re
import numpy as np

from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

cross_encoder = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


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

    doc = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    for page in doc:
        text += page.get_text()

    return text


def extract_skills(text):

    text = text.lower()

    return list(
        set(
            [
                skill
                for skill in SKILL_DB
                if skill in text
            ]
        )
    )


def split_sentences(text):

    sentences = re.split(
        r'[.\n]',
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def get_embedding(text):

    return embedding_model.encode(
        text
    )


def calculate_semantic_similarity(
    resume_text,
    job_text
):

    resume_vector = get_embedding(
        resume_text
    )

    job_vector = get_embedding(
        job_text
    )

    score = cosine_similarity(
        [resume_vector],
        [job_vector]
    )[0][0]

    return round(
        float(score) * 100,
        2
    )


def sentence_similarity(
    resume_text,
    job_text
):

    resume_sentences = split_sentences(
        resume_text
    )

    job_sentences = split_sentences(
        job_text
    )

    if not resume_sentences or not job_sentences:
        return []


    pairs = [
        (resume_sentence, job_sentence)
        for resume_sentence in resume_sentences
        for job_sentence in job_sentences
    ]


    scores = cross_encoder.predict(
        pairs
    )


    results = []

    index = 0

    for resume_sentence in resume_sentences:

        for job_sentence in job_sentences:

            score = scores[index]

            index += 1


            results.append(
                {
                    "resume_sentence": resume_sentence,
                    "job_sentence": job_sentence,
                    "score": round(
                        float(score),
                        2
                    )
                }
            )


    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )[:5]


def rank_resumes(
    resumes,
    job_text
):

    job_skills = extract_skills(
        job_text
    )

    results = []


    for name, text in resumes:

        resume_skills = extract_skills(
            text
        )


        semantic_score = calculate_semantic_similarity(
            text,
            job_text
        )


        matched = (
            set(resume_skills)
            &
            set(job_skills)
        )


        if job_skills:

            skill_score = (
                len(matched)
                /
                len(job_skills)
                *
                100
            )

        else:

            skill_score = 0



        final_score = (
            semantic_score * 0.7
            +
            skill_score * 0.3
        )


        results.append(
            {
                "name": name,

                "semantic_score": round(
                    semantic_score,
                    2
                ),

                "skill_score": round(
                    skill_score,
                    2
                ),

                "final_score": round(
                    final_score,
                    2
                ),

                "matched_skills": list(
                    matched
                ),

                "missing_skills": list(
                    set(job_skills)
                    -
                    set(resume_skills)
                ),

                "explanation": sentence_similarity(
                    text,
                    job_text
                ),

                "resume_text": text
            }
        )


    return sorted(
        results,
        key=lambda x: x["final_score"],
        reverse=True
    )