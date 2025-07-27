import os, sys, subprocess
from dotenv import load_dotenv
from google.genai import types
load_dotenv()

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = [sys.executable, abs_file_path]
        if args:
            commands = [sys.executable, abs_file_path, args[0]]
        result = subprocess.run(commands, capture_output=True,timeout=30, cwd=abs_working_directory, check=True, text=True)
        output = []
        if not result.stdout and not result.stderr:
            return "No output produced"
        
        output.append(f"STDOUT: {result.stdout}")
        output.append(f"STDERR: {result.stderr}")
        return "\n".join(output)
    except subprocess.CalledProcessError as e:
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return f'"Process exited with code {e.returncode}'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)