# HiddenForces

AI-powered hidden test case generator for LeetCode and Codeforces problems using **LangChain**, **LangGraph**, and **Google Gemini**.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Service](#running-the-service)
- [API Endpoints](#api-endpoints)
- [How It Works](#how-it-works)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)

---

## Overview

**HiddenForces** is an intelligent microservice that generates comprehensive hidden test cases for competitive programming problems. It uses advanced AI techniques with **LangChain** and **LangGraph** to create edge cases, boundary conditions, and stress tests that thoroughly validate code submissions.

The service supports both **LeetCode** and **Codeforces** problem formats and integrates seamlessly with the KodeKshetra platform to provide robust test coverage for coding battles.

---

## Features

- **AI-Powered Generation**: Uses Google Gemini via LangChain for intelligent test case creation
- **Workflow-Based Validation**: LangGraph workflow ensures test cases are valid and comprehensive
- **Platform Support**: Works with both LeetCode and Codeforces problem formats
- **Automatic Validation**: Generated test cases are validated before being returned
- **FastAPI Backend**: High-performance async API built with FastAPI
- **Structured Output**: Returns clean, validated test cases ready for code execution
- **Edge Case Coverage**: Generates boundary conditions, corner cases, and stress tests
- **CORS Enabled**: Ready for cross-origin requests from frontend applications

---

## Architecture

HiddenForces uses a **workflow-based architecture** powered by LangGraph:

```
┌─────────────────────────────────────────────────────────────┐
│                     HiddenForces Service                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────────────────────┐    │
│  │   FastAPI    │─────▶│      LangGraph Workflow       │    │
│  │   Endpoint   │      │                               │    │
│  └──────────────┘      │  ┌────────────────────────┐  │    │
│                         │  │  1. Test Generator     │  │    │
│         ▲               │  │     (LangChain + AI)   │  │    │
│         │               │  └──────────┬─────────────┘  │    │
│         │               │             │                 │    │
│    JSON Response        │             ▼                 │    │
│         │               │  ┌────────────────────────┐  │    │
│         │               │  │  2. Test Validator     │  │    │
│         └───────────────│  │     (Format Check)     │  │    │
│                         │  └──────────┬─────────────┘  │    │
│                         │             │                 │    │
│                         │             ▼                 │    │
│                         │  ┌────────────────────────┐  │    │
│                         │  │  3. Valid Test Cases   │  │    │
│                         │  │     (Output)           │  │    │
│                         │  └────────────────────────┘  │    │
│                         └──────────────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Workflow Components

1. **Generator** (`codeforces_generator.py` / `leetcode_generator.py`)
   - Uses LangChain with Google Gemini to generate test cases
   - Analyzes problem constraints, examples, and difficulty
   - Creates diverse test cases including edge cases and stress tests

2. **Validator** (`codeforces_validator.py` / `leetcode_validator.py`)
   - Validates generated test cases against problem constraints
   - Ensures proper format and data types
   - Filters out invalid or malformed test cases

3. **Workflow** (`workflow.py`)
   - Orchestrates the generation and validation process
   - Uses LangGraph for state management
   - Ensures only valid test cases are returned

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/AkshatGarg952/HiddenForces.git
   cd HiddenForces
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
PORT=8000
```

### Environment Variables

- **GOOGLE_API_KEY**: Your Google Gemini API key (required)
- **PORT**: Port number for the server (default: 8000)

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

---

## Running the Service

### Option 1: Using run.py (Recommended)

The easiest way to start the server with the PORT from your `.env` file:

```bash
python run.py
```

This will:
- Load the PORT from your `.env` file
- Start the server on the configured port (default: 8000)
- Enable auto-reload during development

### Option 2: Using uvicorn directly

Start the FastAPI server manually:

```bash
uvicorn app.main:app --reload
```

**Important Notes:**
- Use `app.main:app` (NOT `app.main.py:app`)
- The `--reload` flag enables auto-reload during development
- Default server runs on: `http://127.0.0.1:8000`
- To use a custom port: `uvicorn app.main:app --reload --port 8001`

### Production Deployment

For production, run without reload and specify host/port:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use the run.py script with production settings by modifying it to set `reload=False`.

---

## API Endpoints

### 1. Root Endpoint

**GET** `/`

Returns service information.

**Response:**
```json
{
  "message": "HiddenForces Test Generator API"
}
```

---

### 2. Health Check

**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "ok",
  "service": "HiddenForces",
  "message": "Service is running"
}
```

---

### 3. Generate LeetCode Test Cases

**POST** `/generate-leetcode-tests`

Generate hidden test cases for a LeetCode problem.

**Request Body:**
```json
{
  "problem": {
    "problemId": "two-sum",
    "title": "Two Sum",
    "difficulty": "Easy",
    "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
    "constraints": [
      "2 <= nums.length <= 10^4",
      "-10^9 <= nums[i] <= 10^9",
      "-10^9 <= target <= 10^9",
      "Only one valid answer exists"
    ],
    "examples": [
      {
        "input": "nums = [2,7,11,15], target = 9",
        "output": "[0,1]",
        "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
      }
    ],
    "tags": ["Array", "Hash Table"]
  }
}
```

**Response:**
```json
{
  "hiddenTestCases": [
    "[3, 3]\n6",
    "[1, 2, 3, 4, 5]\n9",
    "[-1, -2, -3, -4, -5]\n-8",
    "[1000000000, 1000000000]\n2000000000"
  ]
}
```

---

### 4. Generate Codeforces Test Cases

**POST** `/generate-codeforces-tests`

Generate hidden test cases for a Codeforces problem.

**Request Body:**
```json
{
  "problem": {
    "problemId": "1A",
    "name": "Theatre Square",
    "difficulty": "800",
    "description": "Theatre Square in the capital city has a rectangular shape with dimensions n × m meters. Calculate minimum number of flagstones needed to pave the square if each flagstone is a × a meters.",
    "inputFormat": "The input contains three positive integer numbers in the first line: n, m and a (1 ≤ n, m, a ≤ 10^9).",
    "outputFormat": "Write the needed number of flagstones.",
    "constraints": [
      "1 ≤ n, m, a ≤ 10^9"
    ],
    "examples": [
      {
        "input": "6 6 4",
        "output": "4"
      }
    ],
    "tags": ["math", "implementation"]
  }
}
```

**Response:**
```json
{
  "hiddenTestCases": [
    "1 1 1",
    "1000000000 1000000000 1",
    "10 10 3",
    "7 8 5"
  ]
}
```

---

## How It Works

### Test Generation Process

1. **Problem Analysis**
   - AI analyzes problem description, constraints, and examples
   - Identifies key parameters and edge cases
   - Determines appropriate test case diversity

2. **Test Case Generation**
   - Creates multiple test cases covering:
     - **Minimum values**: Smallest valid inputs
     - **Maximum values**: Largest valid inputs per constraints
     - **Edge cases**: Boundary conditions (e.g., n=1, empty arrays)
     - **Corner cases**: Special scenarios (e.g., all same elements)
     - **Stress tests**: Large inputs near constraint limits
     - **Random cases**: Diverse middle-range values

3. **Validation**
   - Each test case is validated against problem constraints
   - Format is checked for correctness
   - Invalid cases are filtered out

4. **Output**
   - Returns array of valid test case strings
   - Format matches platform requirements (LeetCode/Codeforces)

---

## Usage Examples

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Generate Codeforces tests
curl -X POST http://localhost:8000/generate-codeforces-tests \
  -H "Content-Type: application/json" \
  -d '{
    "problem": {
      "problemId": "1A",
      "name": "Theatre Square",
      "difficulty": "800",
      "description": "Calculate minimum flagstones needed",
      "constraints": ["1 ≤ n, m, a ≤ 10^9"],
      "examples": [{"input": "6 6 4", "output": "4"}]
    }
  }'
```

### Using Python

```python
import requests

url = 'http://localhost:8000/generate-leetcode-tests'
payload = {
    'problem': {
        'problemId': 'two-sum',
        'title': 'Two Sum',
        'difficulty': 'Easy',
        'description': 'Find two numbers that add up to target',
        'constraints': ['2 <= nums.length <= 10^4'],
        'examples': [
            {
                'input': 'nums = [2,7,11,15], target = 9',
                'output': '[0,1]'
            }
        ]
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

### Using JavaScript

```javascript
const generateTests = async () => {
  const response = await fetch('http://localhost:8000/generate-leetcode-tests', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      problem: {
        problemId: 'two-sum',
        title: 'Two Sum',
        difficulty: 'Easy',
        description: 'Find two numbers that add up to target',
        constraints: ['2 <= nums.length <= 10^4'],
        examples: [{
          input: 'nums = [2,7,11,15], target = 9',
          output: '[0,1]'
        }]
      }
    })
  });
  
  const data = await response.json();
  console.log(data.hiddenTestCases);
};
```

---

## Project Structure

```
HiddenForces/
├── app/
│   ├── main.py                      # FastAPI application and endpoints
│   ├── models.py                    # Pydantic models for request/response
│   ├── workflow.py                  # LangGraph workflow orchestration
│   ├── testcase_generator.py       # Base generator interface
│   ├── testcase_validator.py       # Base validator interface
│   ├── codeforces_generator.py     # Codeforces test generator
│   ├── codeforces_validator.py     # Codeforces test validator
│   ├── leetcode_generator.py       # LeetCode test generator
│   └── leetcode_validator.py       # LeetCode test validator
├── .env                             # Environment variables (create this)
├── .gitignore
├── run.py                           # Server startup script (uses PORT from .env)
├── requirements.txt                 # Python dependencies
└── README.md
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Web Framework** | FastAPI 0.115.2 |
| **Server** | Uvicorn 0.32.0 |
| **AI Framework** | LangChain 0.3.27 |
| **Workflow Engine** | LangGraph 0.2.35 |
| **LLM Provider** | Google Gemini (via langchain-google-genai 2.1.12) |
| **HTTP Client** | Requests 2.32.3 |
| **Environment** | python-dotenv 1.0.1 |

---

## Troubleshooting

### Common Issues

**1. Missing API Key Error**
```
Error: GOOGLE_API_KEY not found in environment
```
**Solution**: Create a `.env` file with your Gemini API key:
```env
GOOGLE_API_KEY=your_key_here
```

**2. Import Error: `app.main.py:app`**
```
Error: No module named 'app.main.py'
```
**Solution**: Use `app.main:app` (without `.py`):
```bash
uvicorn app.main:app --reload
```

**3. Rate Limit Exceeded (Gemini API)**
```
Error: 429 Resource Exhausted
```
**Solution**: 
- Wait a few minutes before retrying
- Check your Gemini API quota at [Google AI Studio](https://makersuite.google.com/)
- Consider upgrading to a paid tier for higher limits

**4. Invalid Test Cases Generated**
```
Response: {"hiddenTestCases": []}
```
**Solution**: 
- Check that problem description and constraints are detailed
- Ensure examples are properly formatted
- Verify Gemini API is responding correctly
- Check logs for validation errors

**5. CORS Errors**
```
Access-Control-Allow-Origin error
```
**Solution**: The service allows all origins by default. If you need to restrict:
- Modify `allow_origin_regex` in `app/main.py`
- Set specific origins instead of `".*"`

### Debug Mode

Enable debug logging:

```python
# In app/main.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Documentation

- **API Docs**: http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative Docs**: http://127.0.0.1:8000/redoc (ReDoc)
- **Flow Documentation**: [FLOW.md](FLOW.md) (if available)
- **Testing Guide**: [TESTING.md](TESTING.md) (if available)

---

## Performance Considerations

- **Generation Time**: Typically 2-5 seconds per problem (depends on Gemini API response time)
- **Concurrent Requests**: FastAPI handles async requests efficiently
- **Caching**: Consider implementing caching for frequently requested problems
- **Rate Limiting**: Gemini free tier has rate limits; implement request queuing for high traffic

---

## License

This project is licensed under the MIT License.

## Author

**Akshat Garg**
- GitHub: [@AkshatGarg952](https://github.com/AkshatGarg952)

## Acknowledgments

- [Google Gemini](https://ai.google.dev/) for the powerful AI model
- [LangChain](https://www.langchain.com/) for the AI framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for workflow orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework

---

Star this repository if you find it helpful!