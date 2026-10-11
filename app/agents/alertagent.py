from app.models.inciddent import Incident
class AlertAgent:
    def execute(self,metrices):
        problems = []
        severity = "HEALTHY"
        if metrices.cpu >90 : 
             problems.append(f"cpu usage is {metrices.cpu}%") 
             severity = "CRITICAL"
        elif metrices.cpu > 70:
             problems.append(f"cpu usage is {metrices.cpu}%")
             if(severity!="CRITICAL"): 
                severity = "WARNING"

        if metrices.disk >90 : 
            problems.append(f"disk usage is {metrices.disk}%")
            severity = "CRITICAL"
        elif metrices.disk > 70:
            problems.append(f"disk usage is {metrices.disk}%") 
            if(severity!="CRITICAL"): 
                severity = "WARNING"

        if metrices.memory >90 : 
            problems.append(f"memory usage is {metrices.memory}%")
            severity = "CRITICAL"
        elif metrices.memory > 70:
            problems.append(f"memory usage is {metrices.memory}%") 
            if(severity!="CRITICAL"): 
                severity = "WARNING"
        return Incident(
                severity=severity,
                problems=problems
            )