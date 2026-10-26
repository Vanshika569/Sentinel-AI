from app.services.system_monitor import System_monitor

from app.agents.diagnosis_agent import DiagnosisAgent
from app.agents.alertagent import AlertAgent
from app.agents.recovery_agent import RecoveryAgent

monitor = System_monitor()
metrices = monitor.get_metrices()


monitor2 = AlertAgent()
incident = monitor2.execute(metrices)

diagnosis_agent = DiagnosisAgent()
recovery_agent  = RecoveryAgent()

diagnosis = diagnosis_agent.execute(incident)
recommendations = recovery_agent.execute(incident)

print("\n========== SENTINELAI INCIDENT REPORT ==========")

print("\nIncident Severity:")
print(incident.severity)

print("\nDetected Problems:")
for problem in incident.problems:
    print("-", problem)

print("\n========== AI DIAGNOSIS ==========")
print(diagnosis)

print("\n========== RECOVERY RECOMMENDATIONS ==========")
for recommendation in recommendations:
    print("-", recommendation)