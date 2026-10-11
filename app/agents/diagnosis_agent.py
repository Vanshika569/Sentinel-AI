import os
from google import genai
from dotenv import load_dotenv
from app.models.inciddent import Incident

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

class DiagnosisAgent:

    def execute(self, incident: Incident):

        if incident.severity == "HEALTHY":
            return "No incident detected."

        prompt = f"""
        Analyze this system incident.

        Severity: {incident.severity}
        Problems: {incident.problems}

        Explain possible causes and suggest safe
        investigation steps. Do not claim certainty
        without sufficient evidence.
        """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text