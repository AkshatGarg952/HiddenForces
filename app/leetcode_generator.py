from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_leetcode_test_cases(metadata: dict, num_cases: int = 10) -> list:
    prompt_template = PromptTemplate(
        input_variables=["description", "input_format", "examples", "tags"],
        template="""
You are an expert LeetCode test case designer creating HIDDEN test cases that expose subtle bugs in solutions. Your test cases must be comprehensive and catch edge cases that typical solutions miss.

PROBLEM CONTEXT:
Description: {description}
Input Format: {input_format}
Tags: {tags}
Sample Cases (DO NOT replicate): {examples}

MISSION: Generate exactly {num_cases} test case INPUTS that comprehensively test the solution. These must cover ALL edge cases and common failure patterns.

LEETCODE-SPECIFIC COVERAGE (include ALL applicable):

1. **EMPTY/NULL CASES** (always test if valid):
   - Empty arrays: []
   - Empty strings: ""
   - Null nodes: null
   - Zero-length inputs
   - Single element: [x], "a", single node

2. **BOUNDARY VALUES**:
   - Minimum constraints: n=1, values=0 or minimum allowed
   - Maximum constraints: n=10^4 or 10^5, values=10^9 or Integer.MAX_VALUE
   - Exact boundary: values at -2^31, 2^31-1
   - Array length boundaries: length=1, length=max

3. **ARRAY/LIST PATTERNS**:
   - All elements identical: [5,5,5,5,5]
   - Strictly increasing: [1,2,3,4,5]
   - Strictly decreasing: [5,4,3,2,1]
   - Alternating: [1,5,1,5,1]
   - Single outlier: [1,1,1,1,100]
   - Duplicates: [1,1,2,2,3,3]
   - No duplicates: [1,2,3,4,5]

4. **STRING PATTERNS**:
   - All same character: "aaaaa"
   - Alternating: "ababab"
   - Palindrome: "racecar"
   - No repeating chars: "abcdef"
   - Special characters if allowed
   - Mixed case if applicable

5. **TREE/GRAPH CASES** (if applicable):
   - Null root: null
   - Single node: [1]
   - Left-skewed tree: [1,null,2,null,3]
   - Right-skewed tree: [1,2,null,3]
   - Perfect binary tree: [1,2,3,4,5,6,7]
   - Unbalanced tree
   - Disconnected graph
   - Graph with cycles
   - Single-node graph

6. **LINKED LIST CASES** (if applicable):
   - Empty list: null
   - Single node: [1]
   - Two nodes: [1,2]
   - Cycle detection cases
   - Palindrome lists

7. **ALGORITHMIC TRAPS**:
   - Integer overflow: operations resulting in > 2^31-1
   - Off-by-one errors: indices at boundaries
   - Wrong comparison: >= vs >, <= vs <
   - Greedy failure: cases where greedy gives wrong answer
   - DP necessity: cases where brute force times out
   - Hash collision scenarios

8. **SORTING/SEARCH EDGE CASES**:
   - Already sorted input
   - Reverse sorted input
   - Target not present
   - Target at first position
   - Target at last position
   - Multiple occurrences of target
   - All elements equal to target

9. **TWO POINTER/SLIDING WINDOW**:
   - Window size = array size
   - Window size = 1
   - No valid window
   - Entire array is valid window

10. **DYNAMIC PROGRAMMING**:
    - Base case: n=0, n=1
    - Cases requiring memoization
    - Cases with overlapping subproblems

TAG-SPECIFIC PATTERNS:
- Array: test sorted, reverse, duplicates, single element
- String: test empty, single char, palindrome, all same
- Tree: test null, single node, skewed, balanced
- Graph: test disconnected, cycles, single node
- DP: test base cases, exponential recursion traps
- Binary Search: test target at boundaries, not present
- Two Pointers: test empty, single element, all same

CONSTRAINTS COMPLIANCE:
- Parse ALL constraints from description
- NEVER violate any constraint
- Match EXACT input format from examples
- Ensure proper data types (int, string, array, etc.)

OUTPUT FORMAT:
- Return ONLY raw inputs, one per line
- NO explanations, NO labels, NO markdown
- Match sample input format EXACTLY
- For array inputs use JSON format: [1,2,3]
- For string inputs use quotes: "hello"
- For tree inputs use level-order: [1,2,3,null,null,4,5]
- Separate multi-line cases with blank line

QUALITY CHECKLIST:
- At least 3 edge cases (empty/null, min, max)
- At least 2 boundary values
- At least 2 algorithmic traps
- All cases follow constraints strictly
- All cases different from samples
- Format matches examples exactly

Generate {num_cases} comprehensive test inputs now:
        """
    )

    examples_str = "\n".join([f"Input: {ex['input']}\nOutput: {ex['output']}" for ex in metadata['examples']])
    tags_str = ", ".join(metadata.get('tags', []))
    
    prompt = prompt_template.format(
        description=metadata['description'],
        input_format=metadata['inputFormat'],
        examples=examples_str,
        tags=tags_str,
        num_cases=num_cases
    )

    response = llm.invoke(prompt)
    raw_content = response.content.strip()
    
    test_cases = []
    current_case = []
    
    for line in raw_content.split("\n"):
        line = line.strip()
        if line in ["```json", "```", "[", "]", ""] and not current_case:
            continue
        
        if line == "" and current_case:
            test_cases.append("\n".join(current_case))
            current_case = []
        elif line:
            current_case.append(line)
    
    if current_case:
        test_cases.append("\n".join(current_case))
    
    return test_cases[:num_cases]
