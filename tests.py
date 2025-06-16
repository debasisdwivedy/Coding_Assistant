import unittest
from functions.get_files_info import get_files_info
from functions.get_files_info import get_file_content
from functions.get_files_info import write_file
from functions.get_files_info import run_python_file

class TestFunctions(unittest.TestCase):
    def test_get_files_info(self):
        get_files_info("calculator", ".")
        get_files_info("calculator", "./")
        get_files_info("calculator", "pkg")
        get_files_info("calculator", "pkg/../../../")
        get_files_info("calculator", "/bin")
        get_files_info("calculator", "../")
    
    def test_get_file_content(self):
        get_file_content("calculator","main.py")
        get_file_content("calculator","pkg/calculator.py")
        get_file_content("calculator","/bin/cat")

    
    def test_write_file(self):
        write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

    def test_run_python_file(self):
        run_python_file("calculator", "main.py")
        run_python_file("calculator", "tests.py")
        run_python_file("calculator", "../main.py")
        run_python_file("calculator", "nonexistent.py")
    

if __name__ == "__main__":
    unittest.main()