import os, sys, subprocess
from dotenv import load_dotenv
load_dotenv()
# Here are some standard library functions you'll find helpful:

# os.path.abspath(): Get an absolute path from a relative path
# os.path.join(): Join two paths together safely (handles slashes)
# .startswith(): Check if a string starts with a substring
# os.path.isdir(): Check if a path is a directory
# os.listdir(): List the contents of a directory
# os.path.getsize(): Get the size of a file
# os.path.isfile(): Check if a path is a file
# .join(): Join a list of strings together with a separator

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

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    dirname = os.path.dirname(abs_file_path)

    try:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(abs_file_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'


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