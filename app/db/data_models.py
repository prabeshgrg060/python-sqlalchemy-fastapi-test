from pydantic import BaseModel

class Usermodel(BaseModel):
    name: str
    age: int

class userget(BaseModel):
    name: str