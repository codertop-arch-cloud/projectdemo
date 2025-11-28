import subprocess
import sys
import tempfile
import os
import traceback

def execute_code(code: str, timeout: int = 5):
    """
    Executes the given python code in a separate process.
    Returns a dictionary with:
    - success: bool
    - output: str (stdout)
    - error: str (stderr)
    - return_code: int
    """
    # Create a temporary file to run the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
        tmp_file.write(code)
        tmp_file_path = tmp_file.name

    try:
        # Run the code in a subprocess
        result = subprocess.run(
            [sys.executable, tmp_file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Execution timed out.",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "return_code": -1
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
