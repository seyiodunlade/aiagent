import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main()












# import os, sys
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types
# from functions.get_files_info import schema_get_files_info
# from functions.get_file_content import schema_get_file_content
# from functions.write_file import schema_write_file
# from functions.run_python_file import schema_run_python_file
# from call_function import call_function, available_functions


# # print(call_function)
# load_dotenv()

# system_prompt="""You are a helpful AI coding agent.

# When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

# - List files and directories

# All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
# """

# def main():

#     if len(sys.argv) <= 1:
#         print('No prompt was provided!!!')
#         sys.exit(1)

#     user_prompt = sys.argv[1]
#     verbose_flag = len(sys.argv) == 3

#     # Functions available to the LLM

#     available_functions = types.Tool(
#     function_declarations=[
#         schema_get_files_info,
#         schema_get_file_content,
#         schema_run_python_file,
#         schema_write_file
#     ]
# )

#     messages = [
#         types.Content(role="user", parts=[types.Part(text=user_prompt)]),
#     ]

#     print(os.environ.get("hot_head"))
#     api_key = os.environ.get("GEMINI_API_KEY")
#     client = genai.Client(api_key=api_key)
#     response = client.models.generate_content(
#         model="gemini-2.0-flash-001",
#         contents=messages,
#         config=types.GenerateContentConfig(tools=[call_function],system_instruction=system_prompt)
#     )

#     if verbose_flag:
#         print(f"User prompt: {user_prompt}")
#         print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
#         print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
#     print('RESPONSE: ', response.candidates[0].content)
#     # Check if there are function calls in the response
#     if response.candidates[0].content.parts:
#         for part in response.candidates[0].content.parts:
#             if hasattr(part, 'function_call'):
#                 function_call_part = part.function_call
#                 print(f"Calling function: {function_call_part.name}({function_call_part.args})")
#             elif hasattr(part, 'text'):
#                 print(part.text)
#     else:
#         print("No response generated")

# if __name__ == "__main__":
#     main()