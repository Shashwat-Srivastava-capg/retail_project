import tempfile
import subprocess
import os
import shutil

def visualization_execution_tool(PYTHON_CODE: str):
    """
    This is a Python program that executes dynamically generated Python code 
    for data visualization purposes. It is designed to run code that typically 
    includes plotting libraries like matplotlib, seaborn, or plotly.

    Args:
    `PYTHON_CODE`: A string containing valid Python code that generates a visualization.
                   The code should be self-contained and handle its own data loading 
                   and plotting logic.

    Returns:
    A dictionary containing:
    - `stdout`: Standard output from the code execution.
    - `stderr`: Any error messages or warnings generated during execution.
    - `image_path` : Path to the generated visualization image
    """
    

    # Create a temporary directory to store the image
    temp_dir = tempfile.mkdtemp()
    image_path = os.path.join(temp_dir, "output.png")

    # Inject image saving code if not already present
    if "plt.savefig" not in PYTHON_CODE:
        PYTHON_CODE += f"\nimport matplotlib.pyplot as plt\nplt.savefig('{image_path}')"

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as f:
        f.write(PYTHON_CODE)
        f.flush()
        try:
            result = subprocess.run(
                ["python", f.name],
                capture_output=True,
                text=True,
                timeout=15
                )
            output = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "image_path": image_path if os.path.exists(image_path) else None
            }
        except subprocess.TimeoutExpired:
            output = {"error": "Execution timed out"}
        finally:
            os.unlink(f.name)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    return output
