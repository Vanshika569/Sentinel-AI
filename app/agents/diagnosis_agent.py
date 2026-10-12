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

            You are SentinelAI, an AI-powered Site Reliability Engineering
            (SRE) incident diagnosis assistant.

            Your task is to analyze the incident using the supplied
            incident information and troubleshooting documentation.

            INCIDENT INFORMATION
            --------------------
            Severity: {incident.severity}
            Problems: {incident.problems}

            RETRIEVED TROUBLESHOOTING DOCUMENTATION
            ---------------------------------------
            {runbook}

            INSTRUCTIONS
            ------------

            1. Prioritize the retrieved runbook when explaining investigation
            steps and recovery recommendations.

            2. Clearly distinguish between:
            - Information directly supported by the incident data.
            - Information supported by the retrieved runbook.
            - Possible causes that have not been confirmed.
            - Additional suggestions based on your general technical knowledge.

            3. If the runbook does not contain enough information, acknowledge
            that limitation. Do not pretend that missing information exists.

            4. Do not invent system metrics, process names, log entries,
            root causes, or diagnostic results.

            5. Do not claim that you inspected processes, analyzed logs,
            fixed an issue, or performed any system operation. You have
            only been provided with the incident information and runbook.

            6. Provide practical investigation steps that explain what evidence
            should be checked before concluding what caused the incident.

            7. Suggest safe recovery options. Do not recommend deleting files,
            terminating processes, or restarting services without considering
            the potential impact and requiring appropriate human approval.

            8. If the retrieved documentation says that no relevant runbook
            was found, state that clearly. Do not claim to have consulted
            a relevant runbook.

            REQUIRED RESPONSE FORMAT
            ------------------------

            1. INCIDENT SUMMARY
            Summarize the detected problem and its reported severity.

            2. RUNBOOK-SUPPORTED GUIDANCE
            Explain the relevant troubleshooting guidance contained in the
            retrieved documentation. If no relevant runbook was found, say so.

            3. POSSIBLE CAUSES
            List plausible causes and clearly state that they are not confirmed
            unless evidence in the incident information establishes them.

            4. INVESTIGATION STEPS
            Provide an ordered list of checks that could help identify the cause.

            5. SAFE RECOVERY RECOMMENDATIONS
            Suggest appropriate actions, noting when human approval or further
            investigation is necessary.

            6. ADDITIONAL AI SUGGESTIONS
            Include useful suggestions that are not explicitly stated in the
            runbook. Clearly label them as additional suggestions rather than
            runbook-supported instructions.

            Keep the response clear, technically accurate, and suitable for an
            SRE engineer investigating a real system incident.
            """

        try:
            response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
            )

            if response.text:
                return response.text

            return (
        "Gemini returned an empty response. "
        "Please try running the diagnosis again."
    )

        except Exception as exc:
            print(f"Gemini diagnosis error: {exc}")

            return (
        "AI diagnosis is temporarily unavailable because Gemini "
        "could not complete the request.\n\n"
        "Incident detection and recovery recommendations can still "
        "be used. Please retry the diagnosis in a few minutes. "
        "No recovery action has been executed."
    )
    def __init__(self):
        self.retriever = RunbookRetriever()