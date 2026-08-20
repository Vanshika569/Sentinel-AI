
class AlertAgent:
    def execute(self,metrices):
        problems = []
        severity = "HEALTHY"
        if metrices.cpu >90 : 
             problems.append(f"cpu usage is {metrices.cpu}%") 
             severity = "CRITICAL"
        elif metrices.cpu > 70:
             problems.append(f"cpu usage is {metrices.cpu}%") 
             severity = "WARNING"

        if metrices.disk >90 : 
            problems.append(f"disk usage is {metrices.disk}%")
            severity = "CRITICAL"
        elif metrices.disk > 70:
            problems.append(f"disk usage is {metrices.disk}%") 
            severity = "WARNING"

        if metrices.memory >90 : 
            problems.append(f"memory usage is {metrices.memory}%")
            severity = "CRITICAL"
        elif metrices.memory > 70:
            problems.append(f"memory usage is {metrices.memory}%") 
            severity = "WARNING"
        return severity,problems