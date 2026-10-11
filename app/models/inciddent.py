from pydantic import BaseModel

class Incident(BaseModel):
    severity : str
    problems : list[str]