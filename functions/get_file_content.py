import os

def get_file_content(working_directory, file_path):
    current_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)
    common_path = os.path.commonprefix([working_path, current_path])

    if len(working_path) > len(common_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(current_path):
        return f'Error: File type invalid or "{file_path}" not found'
    
    MAX_CHARS = 10000
    result_str = ""

    with open(current_path, "r") as f:
        result_str = f.read(MAX_CHARS)

    return result_str

