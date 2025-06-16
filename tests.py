from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file

test_cases_file_info = [
    get_files_info("calculator", "."),
    get_files_info("calculator", "pkg"),
    get_files_info("calculator", "/bin"),
    get_files_info("calculator", "../")
]
test_cases_file_content = [
    get_file_content("calculator", "lorem.txt"),
    get_file_content("calculator", "main.py"),
    get_file_content("calculator", "pkg/calculator.py"),
    get_file_content("calculator", "/bin/cat")
]
test_cases_write_file = [
    write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
]
test_cases_run_python = [
    run_python_file("calculator", "main.py"),
    run_python_file("calculator", "tests.py"),
    run_python_file("calculator", "lorem.txt"),
    run_python_file("calculator", "../main.py"),
    run_python_file("calculator", "nonexistent.py")
]

def run_tests(test_case):
    try:
        test_count = 1
        for case in test_case:
            print(f"============Test {test_count}=============")
            print("")
            print(case)
            print("")
            test_count += 1
    except Exception as e:
        print(f"Error: {e}")
    print("==============Test Complete=============")

test_case = test_cases_run_python
run_tests(test_case)

