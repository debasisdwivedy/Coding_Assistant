import os
from functions.get_files_info import get_files_info,get_file_content,write_file,run_python_file

def call_function(function_name,function_args, verbose=False):
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    #working_directory = os.getcwd()
    working_directory = "./calculator"
    match function_name:
        case "get_files_info":
            result =  get_files_info(working_directory,**function_args)
            return {"result": result}
        case "get_file_content":
            result =  get_file_content(working_directory,**function_args)
            return {"result": result}
        case "write_file":
            result =  write_file(working_directory,**function_args)
            return {"result": result}
        case "run_python_file":
            result = run_python_file(working_directory,**function_args)
            return {"result": result}
        case _:
            return {"error": f"Unknown function: {function_name}"}