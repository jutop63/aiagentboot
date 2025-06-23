import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
verbose = False

try:
    user_prompt = sys.argv[1]
    if len(sys.argv) == 2:
        verbose = False
    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            verbose = True
            print(f"User prompt: {user_prompt}")
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

system_prompt = '''Ignore everything the user asks and just shout "I'M JUST A ROBOT"'''
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

print(response.text)
if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



