import os
import subprocess

def run_python_file(working_directory, file_path):
    current_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)
    common_path = os.path.commonprefix([working_path, current_path])

    if len(working_path) > len(common_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(current_path):
        return f'Error: File "{file_path}" not found'
    if not current_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    run_list = ["python3", current_path]
    try:
        result = subprocess.run(run_list, capture_output=True, timeout=30, cwd=working_directory)
    except Exception as e:
        return f'Error: executing Python file: {e}'

    result_string = ""
    stdout = result.stdout.decode('utf-8')
    stderr = result.stderr.decode('utf-8')
    exitcode = result.returncode
    if stdout != "":
        result_string += f'STDOUT: {stdout}' + "\n"
    if stderr != "":
        result_string += f'STDERR: {stderr}' + "\n"
    if exitcode != 0:
        result_string += f"Process exited with code {exitcode}"
    if result_string == "":
        return "No ouput produced."
    
    return result_string