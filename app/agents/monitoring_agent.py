from app.services.system_monitor import System_monitor

class MonitorAgent:
    def execute(self):  # now we are creating execute as all agents will have the same interface like monitoring.execute,diagnosis.execute,alert.execute
        monitor = System_monitor
        return monitor.get_metrices()