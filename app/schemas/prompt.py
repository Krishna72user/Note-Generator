from pydantic import BaseModel

class Prompt_model(BaseModel):
    title: str
    prompt: str
