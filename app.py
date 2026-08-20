from app.services.system_monitor import System_monitor
from app.agents.monitoring_agent import MonitorAgent
from app.agents.alertagent import AlertAgent
monitor = System_monitor()

# cpu = monitor.get_cpu_usage()
# print("Cpu usage : ",cpu,"%")

# memory = monitor.get_memory_usage()
# print("Memory usage : ",memory,"%")

# disk = monitor.get_disk_usage()
# print("Disk usage : ",disk,"%")

metrices = monitor.get_metrices()
print(metrices)

monitor2 = AlertAgent()

print(monitor2.execute(metrices))