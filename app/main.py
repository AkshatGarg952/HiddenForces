from fastapi import FastAPI
from .models import RequestBody, ResponseBody
from .workflow import build_workflow

app = FastAPI()

@app.post("/generate-test-cases", response_model=ResponseBody)
async def generate_test_cases(request: RequestBody):
    """
    Generate and validate hidden test cases, then get outputs from an external API.
    """
    workflow = build_workflow()
    # Extract the problem dictionary and add language and code
    metadata = request.problem.dict()
    metadata['language'] = request.language
    metadata['code'] = request.code

    result = workflow.invoke({
        "metadata": metadata,
        "test_cases": [],
        "valid_test_cases": [],
        "final_test_cases": []
    })
    return ResponseBody(hiddenTestCases=result['final_test_cases'])