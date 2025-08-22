import google.genai as genai
from dotenv import load_dotenv
import json
load_dotenv()

client = genai.Client() #Finds GEMINI_API_KEY from .env

def generate_report(player_data: dict):
    prompt = (
        "You are an analytical, direct, and witty AI basketball assistant with deep knowledge of the game.\n "
        "Using the provided player statistics across all available seasons, write a concise, data-driven scouting report between 250-600 words.\n"
        "Maintain a professional and technical tone. Structure the report into the following sections, each separated by line breaks\n"
        "Overview\n"
        "Strengths\n"
        "Weaknesses\n"
        "Playstyle and Tendencies\n"
        "Scheme Fit\n"
        "Guidelines:\n"
        "Base every statement strictly on the supplied statistics; do not invent or infer information without statistical support.\n"
        "Keep formatting simple (no bullets, asterisks, or special characters), just text and line breaks.\n"
        "Be accurate, formal, and consistent in presentation.\n"
        f"{player_data}"
    )

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )

    return response.text