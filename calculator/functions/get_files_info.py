import os, sys, subprocess
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, directory)
    print('FULL PATH: ', abs_working_dir)
    abs_path = os.path.abspath(full_path)
    print('ABS PATH: ', abs_path)

    try:
        if directory == ".":
            print('Result for the current directory: ')
        else:
            print(f"Result for the '{directory}' directory: ")
        # if directory.startswith("../") or directory.startswith("/"):
        if not abs_path.startswith(abs_working_dir):
            return f'\t Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'\tError: "{directory}" is not a directory'
        dir_contents = os.listdir(full_path)
        # print('DIR CONTENTS: ', dir_contents)

        files_info = []
        for dir_content in dir_contents:
            abs_dir_content = os.path.join(abs_path, dir_content)
            file_info = f'  - {dir_content}: file_size={os.path.getsize(abs_dir_content)} bytes, is_dir={os.path.isdir(abs_dir_content)}'
            files_info.append(file_info)
        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)