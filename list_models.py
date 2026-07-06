import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("RESUME_AI_RANKER_API_KEY"))

for m in genai.list_models():
    print(m.name)