# we are creating metrices class differently because by creating this another agents can also use this information 
# as we are returning the object like in app.py we  can use metrices.disk,metrices.cpu,etc.

from pydantic import BaseModel
#pydantic will help catch bugs early
class SystemMetrices(BaseModel): #basemodel is a special template for creating data objects or [schemas]
    cpu : float
    memory:float
    disk:float
