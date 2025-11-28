import re

def analyze_and_patch(code: str, error_log: str, output_log: str) -> dict:
    """
    Analyzes the code and logs to generate a patch.
    """
    print(f"DEBUG: Analyzing code (len={len(code)})")
    print(f"DEBUG: Error log: {error_log}")
    
    # --- Heuristic 1: Recursive Traversal Logic Bug ---
    if "def preorder" in code and "res.append(root.val)" in code:
        print("DEBUG: Detected preorder function")
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
        
        print(f"DEBUG: Indices - Left: {idx_left}, Append: {idx_append}, Right: {idx_right}")

        if idx_left != -1 and idx_append != -1 and idx_right != -1:
            if idx_left < idx_append < idx_right:
                print("DEBUG: Found Inorder pattern. Applying patch.")
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
            else:
                print("DEBUG: Pattern found but order is not Inorder.")

    # --- Heuristic 2: Memoization Failure ---
    # Bug: return memo[0] instead of memo[n]
    # Use regex to be safe against spacing: return\s+memo\[0\]
    if re.search(r"return\s+memo\[0\]", code):
        print("DEBUG: Detected memo[0] bug")
        # Replace using regex to preserve surrounding text if needed, or just simple replace if unique
        new_code = re.sub(r"return\s+memo\[0\]", "return memo[n]", code)
        return {
            "patch_applied": True,
            "new_code": new_code,
            "explanation": "Detected incorrect dictionary key usage. `memo[0]` returns a static value, changed to `memo[n]` to return the cached result for the current input.",
            "diff": "- return memo[0]\n+ return memo[n]"
        }

    # --- Heuristic 3: General Recursion Depth ---
    if "RecursionError" in error_log:
         return {
            "patch_applied": False,
            "new_code": code,
            "explanation": "RecursionError detected. Suggest adding a base case or increasing recursion limit.",
            "diff": ""
         }

    print("DEBUG: No patch found.")
    return {
        "patch_applied": False,
        "new_code": code,
        "explanation": "No specific patch pattern matched.",
        "diff": ""
    }
