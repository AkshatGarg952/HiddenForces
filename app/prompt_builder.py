def build_battle_prompt(request, repair_feedback: str = "", attempt_number: int = 1) -> str:
    samples = request.problem.samples or []
    samples_text = "\n".join(
        [
            f"Sample Input:\n{sample.input}\nSample Output:\n{sample.output}"
            for sample in samples
        ]
    )

    refinement_note = ""
    if repair_feedback:
        refinement_note = f"""
PREVIOUS ATTEMPT FEEDBACK:
{repair_feedback}

You must fix that issue and return a complete working solution.
"""

    judged_feedback_note = ""
    if getattr(request, "retryFeedback", ""):
        judged_feedback_note = f"""
PREVIOUS JUDGED FEEDBACK:
{request.retryFeedback}

Use this only as high-level feedback. Do not ask for hidden tests. Return a corrected full solution.
"""

    return f"""
You are participating in a coding battle as an AI opponent on KodeKshetra.

BATTLE CONTEXT:
- Persona: {request.personaConfig.displayName}
- Persona Key: {request.personaConfig.persona}
- Mode: {request.mode}
- Topic: {request.topic}
- Target Rating Band: {request.ratingBand}
- Preferred Language: {request.language}
- Battle Attempt Number: {getattr(request, "attemptNumber", 1)}
- Attempt Number: {attempt_number}

PROBLEM:
Title: {request.problem.title}
Statement:
{request.problem.statement}

Input Format:
{request.problem.inputFormat}

Output Format:
{request.problem.outputFormat}

Constraints:
{request.problem.constraints}

Samples:
{samples_text}

{judged_feedback_note}

{refinement_note}

RULES:
- Return only one complete solution program.
- Do not include explanations.
- Do not include markdown outside a single fenced code block.
- The code must be valid {request.language}.
- Prefer correctness over cleverness.
- Handle edge cases.
- If the problem is DSA-style, write a full runnable program that reads stdin and prints stdout.
- If the problem is Codeforces-style, write a full competitive programming solution.

OUTPUT FORMAT:
Return exactly:
```{request.language}
<code>
```
"""
