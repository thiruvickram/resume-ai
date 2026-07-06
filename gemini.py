import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("RESUME_AI_RANKER_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")


def generate_summary(resume_text, job_text, result):
    prompt = f"""
You are an expert job recruiter. Evaluate this candidate based ONLY on the provided data.

Job description:
{job_text}

Resume:
{resume_text}

Model scores:
- Final Score: {result['final_score']}
- Semantic Score: {result['semantic_score']}
- Skill Score: {result['skill_score']}

Matched skills:
{", ".join(result['matched_skills'])}

Missing skills:
{", ".join(result['missing_skills'])}

Write a structured hiring report with:

1. Overall Fit
2. Strengths
3. Potential Gaps
4. Recommendation

Rules:
- Do NOT invent skills not present
- Be concise
- Be professional
"""
    response = model.generate_content(prompt)
    return response.text