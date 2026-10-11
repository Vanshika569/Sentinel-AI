from app.models.incident import Incident
from app.agents.diagnosis_agent import DiagnosisAgent

incident = Incident(
    severity="CRITICAL",
    problems=["CPU usage is above 90%"]
)

diagnosis_agent = DiagnosisAgent()

result = diagnosis_agent.execute(incident)

print("\n========== SENTINELAI RAG DIAGNOSIS ==========\n")
print(result)