class RecoveryAgent:
    def execute(self, incident):
        recommendations = []

        for problem in incident.problems:
            problem = problem.lower()

            if "cpu" in problem:
                recommendations.append(
                    "Investigate processes consuming excessive CPU."
                )

            elif "memory" in problem or "ram" in problem:
                recommendations.append(
                    "Check memory usage and investigate possible memory leaks."
                )

            elif "disk" in problem or "storage" in problem:
                recommendations.append(
                    "Identify large files and review disk space usage."
                )

        if not recommendations:
            recommendations.append(
                "Investigate the incident and review relevant system logs."
            )

        return recommendations