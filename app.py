from app.services.system_monitor import System_monitor
# from app.agents.monitoring_agent import MonitorAgent
from app.agents.diagnosis_agent import DiagnosisAgent
from app.agents.alertagent import AlertAgent
monitor = System_monitor()

# # cpu = monitor.get_cpu_usage()
# # print("Cpu usage : ",cpu,"%")

# # memory = monitor.get_memory_usage()
# # print("Memory usage : ",memory,"%")

# # disk = monitor.get_disk_usage()
# # print("Disk usage : ",disk,"%")

metrices = monitor.get_metrices()
# print(metrices)

monitor2 = AlertAgent()

# # result = monitor2.execute(metrices)

# monitor3 = DiagnosisAgent()

# # print(monitor3.execute(result.severity,result.problems))
incident = monitor2.execute(metrices)

# print("Severity:", incident.severity)
# print("Problems:", incident.problems)

# diagnosis = monitor3.execute(incident)

# print("Diagnosis:", diagnosis)

diagnosis_agent = DiagnosisAgent()
diagnosis = diagnosis_agent.execute(incident)

print("Diagnosis:", diagnosis)