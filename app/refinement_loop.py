from .candidate_generator import generate_candidate
from .prompt_builder import build_battle_prompt
from .response_normalizer import extract_code_from_response, is_viable_code


def solve_problem_with_refinement(request):
    max_refinements = max(0, min(int(request.personaConfig.maxRefinementPasses or 0), 1))
    total_attempts = 1 + max_refinements
    repair_feedback = ""
    best_candidate = {
        "code": "",
        "confidence": 0.0,
        "attempts": 0
    }

    for attempt_number in range(1, total_attempts + 1):
        prompt = build_battle_prompt(request, repair_feedback=repair_feedback, attempt_number=attempt_number)
        raw_response = generate_candidate(prompt)
        code = extract_code_from_response(raw_response)
        viable = is_viable_code(code, request.language)

        if viable:
            confidence = 0.78 if attempt_number == 1 else 0.64
            return {
                "strategy": "real_solver" if attempt_number == 1 else "assisted_solver",
                "language": request.language,
                "generatedCode": code,
                "confidence": confidence,
                "attempts": attempt_number
            }

        if len(code) > len(best_candidate["code"]):
            best_candidate = {
                "code": code,
                "confidence": 0.28,
                "attempts": attempt_number
            }

        repair_feedback = (
            "The previous answer did not return a full valid program. "
            "Return one complete runnable solution in a single fenced code block."
        )

    if best_candidate["code"]:
        return {
            "strategy": "assisted_solver",
            "language": request.language,
            "generatedCode": best_candidate["code"],
            "confidence": best_candidate["confidence"],
            "attempts": best_candidate["attempts"]
        }

    raise RuntimeError("AI solver could not produce a viable code candidate")
