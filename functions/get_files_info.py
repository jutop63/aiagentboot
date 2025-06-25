import os

def get_files_info(working_directory, directory=None):
    if directory == None:
        directory = "."
    
    current_path = os.path.abspath(os.path.join(working_directory, directory))
    working_path = os.path.abspath(working_directory)
    common_path = os.path.commonprefix([working_path, current_path])

    if len(working_path) > len(common_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(current_path):
        return f'Error: "{directory}" is not a directory'
    
    contents_list = os.listdir(current_path)
    result_list = list(map(lambda x: define_file(x, current_path), contents_list))

    return "\n".join(result_list)
    

def define_file(file_obj, current_path):
    current_file = file_obj
    is_dir = os.path.isdir(current_path+"/"+current_file)
    file_size = os.path.getsize(current_path+"/"+current_file)
    return f"- {file_obj}: file_size={file_size}, is_dir={is_dir}"
