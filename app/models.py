from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

class Example(BaseModel):
    input: str
    output: str

class Problem(BaseModel):
    _id: Optional[str] = None
    problemId: str
    timeLimit: Optional[float] = None
    memoryLimit: Optional[int] = None
    title: str
    description: str
    inputFormat: Optional[str] = ""
    outputFormat: Optional[str] = ""
    examples: List[Example] = Field(default_factory=list)
    sampleTests: List[Example] = Field(default_factory=list)
    hiddenTests: List[Dict] = Field(default_factory=list)
    note: Optional[str] = ""
    rating: Optional[int] = None
    source: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    platform: Literal["leetcode", "codeforces"] = "codeforces"

class RequestBody(BaseModel):
    problem: Problem

class ResponseBody(BaseModel):
    hiddenTestCases: List[str]
