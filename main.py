import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()

if len(sys.argv) <= 1:
    print('No prompt was provided!!!')
    sys.exit(1)

user_prompt = sys.argv[1]
verbose_flag = len(sys.argv) == 3

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]


api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages
)

if verbose_flag:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print(response.text)
