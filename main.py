import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
verbose = False

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, use the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="returns and prints the contents of the given file. constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path pointing to the file that is being read for its contents",
            ),
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the given python file with provided optional arguments. constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path pointing to the .py file that is being run.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="optional arguments for the python file. If no arguments are provided, run the file without any arguments"
            )
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes and/or over writes a file with the provided text. constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path pointing to the file that is going to be created and/or overwritten.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String that is written into give file_path"
            )
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling Function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    callable_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
        }

    function_name = function_call_part.name
    function_dict = function_call_part.args.copy()
    function_dict["working_directory"] = "./calculator"

    if function_name not in callable_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    
    function_result = callable_functions[function_name](**function_dict)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
            )   
        ],
    )

    


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

system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
max_iterations = 20
current_iteration = 0
while current_iteration < max_iterations:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

    try:
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:

                function_call_result = call_function(function_call_part, verbose)

                if not hasattr(function_call_result.parts[0], "function_response"):
                    raise Exception("fatal error when running function")
                if not hasattr(function_call_result.parts[0].function_response, "response"):
                    raise Exception("fatal error when running function")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                messages.append(function_call_result)

        else:
            print(response.text)
            break

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    current_iteration += 1

if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    


