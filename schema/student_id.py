from pydantic import BaseModel

class StudentID(BaseModel):
    apogee_code: str
    class config:
        orm_mode = True