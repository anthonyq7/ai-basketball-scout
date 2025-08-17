import google.genai as genai
from dotenv import load_dotenv
import json
load_dotenv()

client = genai.Client() #Finds GEMINI_API_KEY from .env

def generate_report(player_data: dict):
    prompt = (
        "You are an analytical, direct, and witty AI basketball assistant knowledgable about all things basketball.\n"
        "Use all of the given statistics to direct your analysis and draft a concise and accurate formal scouting report (~250 to ~400 words) for the given player.\n"
        "Focus on strengths, weaknesses, tendencies, playstyle, and scheme fit.\n"
        "Be technical and professional with your tone\n." 
        "Consistently format your report with an brief overview, strengths, weaknesses, playstyle and tendencies, and scheme fit. \n"
        "Do not hallucinate or draw any inferences without being about to back it up with player statistics from the JSON"
        "JSON:\n"
        f"{player_data}"
    )

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )

    return response.text