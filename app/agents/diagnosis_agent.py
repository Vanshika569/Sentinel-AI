import os
from google import genai
from dotenv import load_dotenv
from app.models.incident import Incident
from app.runbook_retriever import RunbookRetriever

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

class DiagnosisAgent:

    def execute(self, incident: Incident):
        if incident.severity == "HEALTHY":
            return "No incident detected."
        runbook = self.retriever.retrieve_runbook(incident)

        prompt = f"""
                Analyze the following system incident.

                Severity: {incident.severity}
                Problems: {incident.problems}

                Relevant troubleshooting documentation:
                {runbook}

                Use the documentation above as supporting context.

                Explain:
                1. Possible causes of the incident.
                2. Investigation steps.
                3. Safe recovery recommendations.

                Distinguish possible causes from confirmed causes.
                Do not claim that an action has been performed.
                Do not recommend destructive actions without approval.
                """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text
    def __init__(self):
        self.retriever = RunbookRetriever()