import google.genai as genai
from dotenv import load_dotenv
import json
load_dotenv()

client = genai.Client() #Finds GEMINI_API_KEY from .env

def generate_report(player_data: dict):
    prompt = (
        "You are an analytical, direct, and witty AI basketball assistant knowledgable about all things basketball.\n"
        "Use all of the given statistics and seasons to direct your analysis and draft a concise and accurate formal scouting report (from ~250 to ~600 words) for the given player.\n"
        "Be technical and professional with your tone\n." 
        "Consistently format your report with an brief overview, strengths, weaknesses, playstyle and tendencies, and scheme fit. \n"
        "Do not hallucinate or draw any inferences without being about to back it up with player statistics from the JSON\n"
        "Make the formatting of your response simple. For each subsection and the overall report, don't use * or any fancy formatting, separating by new lines should do\n"
        "JSON:\n"
        f"{player_data}"
    )

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )

    return response.text