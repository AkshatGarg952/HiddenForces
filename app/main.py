from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import RequestBody, ResponseBody
from .workflow import build_workflow

app = FastAPI(title="HiddenForces Test Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "HiddenForces Test Generator API"}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "HiddenForces",
        "message": "Service is running"
    }

@app.post("/generate-leetcode-tests", response_model=ResponseBody)
async def generate_leetcode_tests(request: RequestBody):
    try:
        workflow = build_workflow()
        metadata = request.problem.dict()
        metadata['platform'] = 'leetcode'

        result = workflow.invoke({
            "metadata": metadata,
            "test_cases": [],
            "valid_test_cases": []
        })
        return ResponseBody(hiddenTestCases=result['valid_test_cases'])
    except Exception as e:
        print(f"Error generating LeetCode tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-codeforces-tests", response_model=ResponseBody)
async def generate_codeforces_tests(request: RequestBody):
    try:
        workflow = build_workflow()
        metadata = request.problem.dict()
        metadata['platform'] = 'codeforces'

        result = workflow.invoke({
            "metadata": metadata,
            "test_cases": [],
            "valid_test_cases": []
        })
        return ResponseBody(hiddenTestCases=result['valid_test_cases'])
    except Exception as e:
        print(f"Error generating Codeforces tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))
