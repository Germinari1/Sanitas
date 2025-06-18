"""
Models for input and output of the RAG system agent
"""
from pydantic import BaseModel


class HospitalQueryInput(BaseModel):
    text: str


class HospitalQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]
