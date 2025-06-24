from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Code Visualization Service")

class PythonInterpreter:
    def __init__(self):
        pass

    def run(self, code: str):
        """
        Executes the given Python code string.
        """
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        # Create fresh global and local namespaces for each execution.
        exec_globals = {}

        try:
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                exec(code, exec_globals)

            return {
                "status": "success",
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
            }
        except Exception:
            return {
                "status": "error",
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue() + traceback.format_exc(),
            }
        
interpreter = PythonInterpreter()

@mcp.tool()
def visualize_code(code: str,name : str) -> str:
    """
    Executes one or more lines of Python code.
    The provided code string can import and use libraries such as numpy,
    pandas, and matplotlib.pyplot.

    Args:
        code: A string containing the Python code to execute.

    Returns:
        A string containing the standard output (stdout) and standard error (stderr)
        produced by the executed code.
    """
    code += f"""
from IPython.display import Image, display

try:
    display(Image({name}.get_graph().draw_mermaid_png()))
except NameError:
    print("Error: The graph object named '{name}' is not defined in the code.")
except Exception as e:
    print(f"Unexpected error during graph visualization: {{e}}")
"""
    result = interpreter.run(code)

@mcp.prompt()
def find_graph_definition() -> str:
    """Identify the code snippet used for creation of the graph."""
    return "Where is the graph defined in the code snippet? Return the relevant code section as text."
@mcp.prompt()
def find_graph_name() -> str:
    """Identify the name of the used graph."""
    return "What is the name of the graph used in the code snippet? Return the name as text."
