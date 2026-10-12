from app.models.incident import Incident
from app.agents.diagnosis_agent import DiagnosisAgent


def test_diagnosis():
    print("\n========== SENTINELAI AI DIAGNOSIS TEST ==========")

    incident = Incident(
        severity="CRITICAL",
        problems=["High CPU usage detected: 92%"]
    )

    diagnosis_agent = DiagnosisAgent()

    print("\nTesting AI diagnosis for high CPU usage...")
    print("Severity:", incident.severity)
    print("Problems:", incident.problems)

    result = diagnosis_agent.execute(incident)

    print("\n========== DIAGNOSIS RESULT ==========")
    print(result)


if __name__ == "__main__":
    test_diagnosis()