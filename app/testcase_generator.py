from .leetcode_generator import generate_leetcode_test_cases
from .codeforces_generator import generate_codeforces_test_cases

def generate_test_cases(metadata: dict, num_cases: int = 10) -> list:
    platform = metadata.get('platform', 'codeforces')
    
    if platform == 'leetcode':
        return generate_leetcode_test_cases(metadata, num_cases)
    elif platform == 'codeforces':
        return generate_codeforces_test_cases(metadata, num_cases)
    else:
        return generate_codeforces_test_cases(metadata, num_cases)
