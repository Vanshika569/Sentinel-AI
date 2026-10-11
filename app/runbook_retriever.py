from pathlib import Path  #Path helps Python work with folders and file paths.


class RunbookRetriever:
    def __init__(self):
        self.knowledge_base = Path("knowledge_base")   #This stores the path to the folder containing our troubleshooting documents.
                                                        #For example, the retriever will look inside knowledge_base for high_cpu.txt.
    def load_runbooks(self):
        runbooks = {}

        for file_path in self.knowledge_base.glob("*.txt"):
            runbooks[file_path.stem] = file_path.read_text(
                encoding="utf-8"
            )

        return runbooks
# runbooks = {} creates an empty dictionary.
# glob("*.txt") finds text files in the knowledge-base folder.
# file_path.stem retrieves the filename without .txt.
# read_text() reads the document's contents.
# return runbooks returns all the documents as a dictionary.
    def retrieve_runbook(self, incident):
        text = " ".join(incident.problems).lower()

        if "cpu" in text or "processor" in text:
            category = "high_cpu"

        elif "memory" in text or "ram" in text:
            category = "high_memory"

        elif "disk" in text or "storage" in text:
            category = "high_disk"

        else:
            return "No relevant runbook found."

        runbooks = self.load_runbooks()
        return runbooks.get(category, "No relevant runbook found.")