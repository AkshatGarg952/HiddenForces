# API Testing Examples

## Setup
1. Create a `.env` file in the project root with:
   ```
   GOOGLE_API_KEY=your_actual_gemini_api_key
   ```

2. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## LeetCode Example - Two Sum Problem

### Request
```bash
curl -X POST http://localhost:8000/generate-leetcode-tests \
  -H "Content-Type: application/json" \
  -d '{
    "problem": {
      "_id": "1",
      "problemId": "two-sum",
      "timeLimit": 2.0,
      "memoryLimit": 256,
      "title": "Two Sum",
      "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order. Constraints: 2 <= nums.length <= 10^4, -10^9 <= nums[i] <= 10^9, -10^9 <= target <= 10^9, Only one valid answer exists.",
      "inputFormat": "First line: array of integers nums. Second line: integer target",
      "outputFormat": "Array of two indices",
      "examples": [
        {
          "input": "[2,7,11,15]\n9",
          "output": "[0,1]"
        },
        {
          "input": "[3,2,4]\n6",
          "output": "[1,2]"
        }
      ],
      "hiddenTests": [],
      "note": "Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?",
      "rating": 1200,
      "source": "leetcode",
      "tags": ["array", "hash-table"],
      "platform": "leetcode"
    }
  }'
```

### Expected Response
```json
{
  "hiddenTestCases": [
    "[1,2]\n3",
    "[1000000000,-1000000000,5]\n5",
    "[1,1,1,1,1]\n2",
    "[5,5,5,5,10]\n10",
    "[-1,-2,-3,-4,-5]\n-8",
    "[0,4,3,0]\n0",
    "[2,5,5,11]\n10",
    "[1,2,3,4,5,6,7,8,9,10]\n19"
  ]
}
```

## Codeforces Example - Theatre Square Problem

### Request
```bash
curl -X POST http://localhost:8000/generate-codeforces-tests \
  -H "Content-Type: application/json" \
  -d '{
    "problem": {
      "_id": "cf1",
      "problemId": "1A",
      "timeLimit": 2.0,
      "memoryLimit": 256,
      "title": "Theatre Square",
      "description": "Theatre Square in the capital city of Berland has a rectangular shape with the size n × m meters. On the occasion of the city'\''s anniversary, a decision was taken to pave the Square with square granite flagstones. Each flagstone is of the size a × a. What is the least number of flagstones needed to pave the Square? It'\''s allowed to cover the surface larger than the Theatre Square, but the Square has to be covered. It'\''s not allowed to break the flagstones. The sides of flagstones should be parallel to the sides of the Square. Constraints: 1 ≤ n, m, a ≤ 10^9",
      "inputFormat": "The input contains three positive integer numbers in the first line: n, m and a",
      "outputFormat": "Write the needed number of flagstones",
      "examples": [
        {
          "input": "6 6 4",
          "output": "4"
        }
      ],
      "hiddenTests": [],
      "note": "In the example n = 6, m = 6, a = 4. We need 4 flagstones.",
      "rating": 1000,
      "source": "codeforces",
      "tags": ["math"],
      "platform": "codeforces"
    }
  }'
```

### Expected Response
```json
{
  "hiddenTestCases": [
    "1 1 1",
    "1000000000 1000000000 1",
    "1000000000 1000000000 1000000000",
    "1 1 1000000000",
    "999999999 999999999 1000000000",
    "5 5 3",
    "10 10 3",
    "1000000000 1 1",
    "7 13 4",
    "100 100 10"
  ]
}
```

## Using Python Requests

### LeetCode Test
```python
import requests
import json

url = "http://localhost:8000/generate-leetcode-tests"
payload = {
    "problem": {
        "_id": "1",
        "problemId": "two-sum",
        "timeLimit": 2.0,
        "memoryLimit": 256,
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. Constraints: 2 <= nums.length <= 10^4, -10^9 <= nums[i] <= 10^9",
        "inputFormat": "Array and target",
        "outputFormat": "Two indices",
        "examples": [{"input": "[2,7,11,15]\\n9", "output": "[0,1]"}],
        "hiddenTests": [],
        "note": "",
        "rating": 1200,
        "source": "leetcode",
        "tags": ["array", "hash-table"],
        "platform": "leetcode"
    }
}

response = requests.post(url, json=payload)
print(json.dumps(response.json(), indent=2))
```

### Codeforces Test
```python
import requests
import json

url = "http://localhost:8000/generate-codeforces-tests"
payload = {
    "problem": {
        "_id": "cf1",
        "problemId": "1A",
        "timeLimit": 2.0,
        "memoryLimit": 256,
        "title": "Theatre Square",
        "description": "Calculate minimum flagstones needed. Constraints: 1 ≤ n, m, a ≤ 10^9",
        "inputFormat": "Three integers n, m, a",
        "outputFormat": "Single integer",
        "examples": [{"input": "6 6 4", "output": "4"}],
        "hiddenTests": [],
        "note": "",
        "rating": 1000,
        "source": "codeforces",
        "tags": ["math"],
        "platform": "codeforces"
    }
}

response = requests.post(url, json=payload)
print(json.dumps(response.json(), indent=2))
```

## Notes

- **Variable Name**: `GOOGLE_API_KEY` (must be exactly this)
- **File Location**: `.env` in project root (`c:\Users\garga\OneDrive\Desktop\HiddenForces\.env`)
- **Get API Key**: https://makersuite.google.com/app/apikey
- The `.env` file is already loaded by `python-dotenv` in the generator/validator files
- Make sure to add `.env` to your `.gitignore` to keep your API key secret
