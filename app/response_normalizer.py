import re

FENCED_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_+-]*\n(.*?)```", re.DOTALL)


def extract_code_from_response(response_text: str) -> str:
    text = (response_text or "").strip()
    if not text:
        return ""

    match = FENCED_BLOCK_RE.search(text)
    if match:
        return match.group(1).strip()

    return text.strip()


def is_viable_code(code: str, language: str) -> bool:
    text = (code or "").strip()
    if len(text) < 40:
        return False

    if language == "python":
        return "def " in text or "print(" in text or "import " in text

    if language == "cpp":
        return "#include" in text or "int main" in text

    if language == "java":
        return "class " in text and "public static void main" in text

    if language == "javascript":
        return "function " in text or "const " in text or "let " in text

    return True
