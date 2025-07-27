import os
from dotenv import load_dotenv
load_dotenv()
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
    print('ABS working directory: ', abs_working_directory)
    print('ABS FILE PATH: ', abs_file_path)


    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, "r") as f:
            truncation_msg =f' [...File "{file_path}" truncated at 10000 characters]'
            print('TYPE: ', type(os.environ.get("MAX_CHARS")))
            file_contents = f.read(int(os.environ.get("MAX_CHARS")))
            additional_content = f.read(1)
            if additional_content:
                file_contents = file_contents + truncation_msg

            return file_contents
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {os.environ.get("MAX_CHARS")} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)