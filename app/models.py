from pydantic import BaseModel
from typing import List, Dict

class Example(BaseModel):
    input: str
    output: str

class Problem(BaseModel):
    _id: str
    problemId: str
    timeLimit: float
    memoryLimit: int
    title: str
    description: str
    inputFormat: str
    outputFormat: str
    examples: List[Example]
    hiddenTests: List[Dict]
    note: str
    rating: int
    source: str
    tags: List[str]

class RequestBody(BaseModel):
    language: str
    problem: Problem
    code: str

class TestCase(BaseModel):
    input: str
    output: str

class ResponseBody(BaseModel):
    hiddenTestCases: List[TestCase]