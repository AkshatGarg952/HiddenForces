from fastapi import FastAPI
from .models import RequestBody, ResponseBody
from .workflow import build_workflow

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to HiddenForces!"}


@app.post("/generate-leetcode-tests", response_model=ResponseBody)
async def generate_leetcode_tests(request: RequestBody):
    workflow = build_workflow()
    metadata = request.problem.dict()
    metadata['platform'] = 'leetcode'

    result = workflow.invoke({
        "metadata": metadata,
        "test_cases": [],
        "valid_test_cases": []
    })
    return ResponseBody(hiddenTestCases=result['valid_test_cases'])

@app.post("/generate-codeforces-tests", response_model=ResponseBody)
async def generate_codeforces_tests(request: RequestBody):
    workflow = build_workflow()
    metadata = request.problem.dict()
    metadata['platform'] = 'codeforces'

    result = workflow.invoke({
        "metadata": metadata,
        "test_cases": [],
        "valid_test_cases": []
    })
    return ResponseBody(hiddenTestCases=result['valid_test_cases'])

