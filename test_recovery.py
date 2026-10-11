from app.models.incident import Incident
from app.agents.recovery_agent import RecoveryAgent

incident = Incident(
    severity="CRITICAL",
    problems=[
        "CPU usage is above 90%",
        "Memory usage is too high",
        "Disk storage is nearly full"
    ]
)

agent = RecoveryAgent()
recommendations = agent.execute(incident)

print("Recovery Recommendations:")

for recommendation in recommendations:
    print("-", recommendation)