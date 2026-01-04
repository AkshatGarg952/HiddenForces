from pydantic import BaseModel
from typing import List, Dict, Literal, Optional

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
    hiddenTests: Optional[List[Dict]] = []
    note: Optional[str] = ""
    rating: int
    source: str
    tags: List[str]
    platform: Literal["leetcode", "codeforces"] = "codeforces"

class RequestBody(BaseModel):
    problem: Problem

class ResponseBody(BaseModel):
    hiddenTestCases: List[str]