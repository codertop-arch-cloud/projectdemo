from .sandbox import execute_code
from .patcher import analyze_and_patch

def run_repair_loop(initial_code: str, max_iterations: int = 5):
    """
    Runs the autonomous repair loop.
    Returns a list of steps (history).
    """
    history = []
    current_code = initial_code
    
    for i in range(max_iterations):
        step_info = {
            "iteration": i + 1,
            "code_before": current_code,
            "execution": None,
            "patch": None,
            "status": "running"
        }
        
        # 1. Run
        exec_result = execute_code(current_code)
        step_info["execution"] = exec_result
        
        # Check if we should stop (e.g., success? but for logic bugs, success might still be wrong output)
        # For this demo, we'll let the patcher decide if it sees a bug.
        # If the patcher finds nothing to fix, we stop.
        
        # 2. Patch
        patch_result = analyze_and_patch(current_code, exec_result["error"], exec_result["output"])
        step_info["patch"] = patch_result
        
        history.append(step_info)
        
        if patch_result["patch_applied"]:
            current_code = patch_result["new_code"]
            step_info["status"] = "patched"
        else:
            step_info["status"] = "no_patch_found"
            break
            
        # If execution was successful AND patcher didn't find logic bugs (this condition is tricky)
        # Actually, if patcher applied a patch, we loop again to verify.
        # If patcher didn't apply a patch, we stop.
        
    return history
