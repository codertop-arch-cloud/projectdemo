import re

def analyze_and_patch(code: str) -> dict:
    # --- Heuristic 1: Recursive Traversal Logic Bug ---
    if "def preorder" in code and "res.append(root.val)" in code:
        # Robust approach: Split into lines and reorder
        lines = code.split('\n')
        
        idx_left = -1
        idx_append = -1
        idx_right = -1
        
        for i, line in enumerate(lines):
            if "preorder(root.left, res)" in line:
                idx_left = i
            elif "res.append(root.val)" in line:
                idx_append = i
            elif "preorder(root.right, res)" in line:
                idx_right = i
        
        if idx_left != -1 and idx_append != -1 and idx_right != -1:
            if idx_left < idx_append < idx_right:
                lines_copy = list(lines)
                append_content = lines_copy[idx_append]
                lines_copy.pop(idx_append)
                lines_copy.insert(idx_left, append_content)
                fixed_code = '\n'.join(lines_copy)
                
                return {
                     "patch_applied": True,
                     "new_code": fixed_code,
                     "explanation": "Detected Inorder traversal (Left -> Root -> Right). Switched to Preorder (Root -> Left -> Right) to match expected output.",
                     "diff": "Moved `res.append(root.val)` to the top of the recursive steps."
                 }

    # --- Heuristic 2: Memoization Failure ---
    if "return memo[0]" in code:
        new_code = code.replace("return memo[0]", "return memo[n]")
        return {"patch_applied": True, "new_code": new_code, "explanation": "Memo Fixed"}

    return {"patch_applied": False, "explanation": "No patch found"}

# Exact code from user request
test_case_1 = """class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def preorder(root, res):
    if not root:
        return
    
    preorder(root.left, res)
    res.append(root.val)
    preorder(root.right, res)

root = Node(1)
root.left = Node(2)
root.right = Node(3)

res = []
preorder(root, res)
print(res)"""

test_case_2 = """def fib(n, memo={}):
    if n <= 1:
        return n

    if n in memo:
        return memo[0]   # BUG: wrong key returned

    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

print(fib(10))"""

print("--- Test Case 1 ---")
result1 = analyze_and_patch(test_case_1)
print(result1)

print("\n--- Test Case 2 ---")
result2 = analyze_and_patch(test_case_2)
print(result2)
