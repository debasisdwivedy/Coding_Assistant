from enum import Enum

class ToolSchema(Enum):
    LIST_FOLDER_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": (
            "Retrieves metadata (file name, size, and type) for all contents (files and subdirectories) inside a specific directory. "
            "This function is used when a user wants to browse, inspect, or list files/folders inside a particular path. "
            "Useful when the user asks to 'see what's inside a folder', 'list files in a path', 'show contents of a directory', or similar queries."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": (
                        "The path (relative or absolute to the working_directory) of the folder whose contents are to be listed. "
                        "This can be '.' for the current working directory, or any valid subfolder path."
                    )
                },
            },
            "required": ["directory"]
        }
    }
}

    GET_FILE_CONTENT_SCHEME = {
        "type": "function",
        "function": {
            "name": "get_file_content",
            "description": (
                "Reads and returns the textual content of a specific file (up to 10,000 characters). "
                "Only works if the path points to a file; returns an error if it's a directory or invalid. "
                "Use this function when a user says things like 'open this file', 'read the contents of xyz.py', 'show me what’s inside the file', etc."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": (
                            "The relative or absolute path (within the working_directory) to the file that should be read. "
                            "It must point to a valid file and not a folder."
                        )
                    },
                },
                "required": ["file_path"]
            }
        }
    }

    WRITE_FILE_SCHEMA = {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Writes text content to a file at the given path. If the file already exists, it is overwritten. "
                "If it does not exist, a new file is created. "
                "Use this function when a user asks to 'save this code', 'write to a file', 'update the file', or 'create a new file with this content'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": (
                            "The relative or absolute file path (within the working_directory) where the content will be written. "
                            "If the file already exists, it will be replaced."
                        )
                    },
                    "content": {
                        "type": "string",
                        "description": (
                            "The full textual content to be written into the file. Could be source code, plain text, JSON, etc."
                        )
                    },
                },
                "required": ["file_path", "content"]
            }
        }
    }

    RUN_PYTHON_FILE_SCHEMA = {
        "type": "function",
        "function": {
            "name": "run_python_file",
            "description": (
                "Executes a Python script located at the specified path and returns its output (stdout or error message). "
                "Use this when a user says things like 'run this code', 'execute the file', 'test the script', or anything related to launching a Python program."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": (
                            "The relative or absolute path (within working_directory) to the Python file to be executed. "
                            "It must be a valid Python (.py) file."
                        )
                    },
                    "arguments": {
                        "type": "array",
                        "items": { "type": "string" },
                        "description": (
                            "The list of arguments required to be send to the python script."
                        )
                    },
                    "install_pkg": {
                        "type": "array",
                        "items": { "type": "string" },
                        "description": (
                            "The pip package if any required to be installed before running the python script."
                        )
                    },
                },
                "required": ["file_path"]
            }
        }
    }