class DiagnosisAgent:

    def execute(self, status, problems):

        if status == "HEALTHY":
            return "No incident detected."

        return f"Incident detected: {problems}"