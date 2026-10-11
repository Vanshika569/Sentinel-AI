from app.services.system_monitor import System_monitor
# from app.agents.monitoring_agent import MonitorAgent
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

print("\nRecovery Recommendations:")

for recommendation in recommendations:
    print("-", recommendation)