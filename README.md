# HiddenForces

AI-powered test case generator for LeetCode and Codeforces problems.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create `.env` file in project root:
```
GOOGLE_API_KEY=your_gemini_api_key
```

Get API key: https://makersuite.google.com/app/apikey

## Running

Start the server:
```bash
uvicorn app.main:app --reload
```

**Important:** Use `app.main:app` (NOT `app.main.py:app`)

Server runs on: http://127.0.0.1:8000

## API Endpoints

- `POST /generate-leetcode-tests` - Generate LeetCode test cases
- `POST /generate-codeforces-tests` - Generate Codeforces test cases

## Documentation

- API Docs: http://127.0.0.1:8000/docs
- Flow: [FLOW.md](FLOW.md)
- Testing: [TESTING.md](TESTING.md)

## Quick Test

```bash
curl -X POST http://localhost:8000/generate-codeforces-tests \
  -H "Content-Type: application/json" \
  -d '{"problem": {...}}'
```

See [TESTING.md](TESTING.md) for complete examples.