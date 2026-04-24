from pydantic import BaseModel
from typing import List, Dict, Literal, Optional

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
    examples: Optional[List[Example]] = []
    sampleTests: Optional[List[Example]] = []
    hiddenTests: Optional[List[Dict]] = []
    note: Optional[str] = ""
    rating: Optional[int] = None
    source: Optional[str] = None
    tags: Optional[List[str]] = []
    platform: Literal["leetcode", "codeforces"] = "codeforces"

class RequestBody(BaseModel):
    problem: Problem

class ResponseBody(BaseModel):
    hiddenTestCases: List[str]

class AIBattleProblem(BaseModel):
    title: str
    statement: str
    inputFormat: Optional[str] = ""
    outputFormat: Optional[str] = ""
    constraints: Optional[str] = ""
    samples: Optional[List[Example]] = []

class PersonaConfig(BaseModel):
    targetSkill: Optional[str] = "balanced"
    maxRefinementPasses: Optional[int] = 1
    displayName: Optional[str] = "KodeBot"
    persona: Optional[str] = "generalist"

class AIBattleSolveRequest(BaseModel):
    battleId: str
    mode: Literal["cp", "dsa"]
    topic: str
    attemptNumber: Optional[int] = 1
    retryFeedback: Optional[str] = ""
    ratingBand: int
    language: str
    problem: AIBattleProblem
    personaConfig: PersonaConfig

class AIBattleSolveResponse(BaseModel):
    strategy: Literal["real_solver", "assisted_solver"]
    language: str
    generatedCode: str
    confidence: float
    attempts: int
