import psutil
from app.models.metrices import SystemMetrices

class System_monitor: #"To encapsulate all monitoring logic in a single service. T
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)
    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent
    def get_disk_usage(self):
        disk = psutil.disk_usage("/")
        return disk.percent
    def get_metrices(self): 
        return SystemMetrices(
            cpu = self.get_cpu_usage(),
            memory= self.get_memory_usage(),
            disk = self.get_disk_usage()
        )