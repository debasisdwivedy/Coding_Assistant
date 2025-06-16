import os,subprocess
from subprocess import CompletedProcess

def get_files_info(working_directory, directory=None):
    if working_directory is None:
        working_directory = os.getcwd()
    try:
        if os.path.exists(working_directory) and os.path.isdir(working_directory):
            full_path = os.path.join(working_directory,directory.replace("./","").replace("/.",""))
            full_path = full_path.rstrip("./").rstrip("/.").rstrip("/").rstrip(".")
            if directory !="." and directory !="./" and full_path == working_directory:
                #print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory "{working_directory}"')
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory "{working_directory}"'
                
            if os.path.exists(full_path) and os.path.isdir(full_path):
                results = os.listdir(full_path)
                files = []
                for result in results:
                    file_path = os.path.join(full_path,result)
                    size_in_bytes = os.path.getsize(file_path)
                    is_dir = os.path.isdir(file_path)
                    #print(f"- {result}: file_size={size_in_bytes} bytes, is_dir={is_dir}")
                    files.append(f"- {result}: file_size={size_in_bytes} bytes, is_dir={is_dir}")
                return str(files)
            else:
                #print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory "{working_directory}"')
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory "{working_directory}"'
        else:
            #print(f'Error: "{working_directory}" is does not exsist')
            return f'Error: "{working_directory}" is does not exsist'
    except Exception as e:
        #print(f"Error while listing files of {directory} from {working_directory}",e)
        return f"Error while listing files of {directory} from {working_directory} with exception {e}"

def get_file_content(working_directory, file_path=None):
    if working_directory is None:
        working_directory = os.getcwd()
    try:
        if os.path.exists(working_directory) and os.path.isdir(working_directory):
            full_path = os.path.join(working_directory,file_path)
            if (os.path.exists(full_path) and 
                os.path.isfile(full_path) and 
                not file_path.startswith(".") and 
                not file_path.startswith("/")
            ):
                with open(full_path,"r") as f:
                    content = f.read()
                    if len(content) > 10000:
                        content = content[:10000]
                #print(content)
                return content
            else:
                #print(f'Error: File not found or is not a regular file: "{file_path}"')
                #print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
                return f'Error: File not found or is not a regular file: "{file_path}" OR Cannot read "{file_path}" as it is outside the permitted working directory'
        else:
            #print(f'Error: "{working_directory}" is does not exsist')
            return f'Error: "{working_directory}" is does not exsist'
    except Exception as e:
        #print(f"Error while reading file {file_path} from {working_directory}",e)
        return f"Error while reading file {file_path} from {working_directory} with exception {e}"
    
def write_file(working_directory, file_path=None, content=None):
    if working_directory is None:
        working_directory = os.getcwd()
    try:
        if os.path.exists(working_directory) and os.path.isdir(working_directory):
            full_path = os.path.join(working_directory,file_path)
            folder_path = os.path.dirname(full_path)

            if (
                os.path.exists(folder_path) and 
                os.path.isdir(folder_path) and
                not file_path.startswith(".") and 
                not file_path.startswith("/")
                ):
                with open(full_path,"w") as f:
                    f.write(content)
                #print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            else:
                #print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        else:
            #print(f'Error: "{working_directory}" is does not exsist')
            return f'Error: "{working_directory}" is does not exsist'
    except Exception as e:
        #print(f"Error while writing file {file_path} from {working_directory}",e)
        return f"Error while writing file {file_path} from {working_directory} with exception {e}"

def run_python_file(working_directory, file_path=None, arguments=None,install_pkg:list=[]):
    response = []
    if working_directory is None:
        working_directory = os.getcwd()

    if not file_path.endswith(".py"):
        #print(f'Error: "{file_path}" is not a Python file.')
        return f'Error: "{file_path}" is not a Python file.'
    try:
        #content = get_file_content(working_directory,file_path)
        cwd = os.getcwd()
        full_path = os.path.join(working_directory,file_path)
        folder_path = os.path.dirname(full_path)
        if os.path.isfile(full_path):
            # file_name = full_path.split(os.sep)[-1]
            # os.chdir(working_directory)
            # result = subprocess.run(
            #     ['python3', file_path],
            #     capture_output=True,
            #     text=True,
            #     timeout=30  # seconds
            # )

            result = run_python_file_docker(working_directory_full_path=os.path.abspath(working_directory),filename=file_path,arguments=arguments,install_pkg=install_pkg)
            if result.stdout:
                #print("STDOUT:", result.stdout)
                response.append(f"STDOUT:{result.stdout}")
            else:
                #print("No output produced.")
                response.append(f"STDOUT:No output produced.")
            if result.stderr:
                #print("STDERR:", result.stderr)
                response.append(f"STDERR:{result.stderr}")
            #print("Process exited with code ", result.returncode)
            response.append(f"Process exited with code {result.returncode}")
        else:
            response.append(f"Error: Invalid Python file: {full_path}")

        os.chdir(cwd)
    except Exception as e:
        #print(f"Error: executing Python file: {e}")
        response.append(f"Error: executing Python file: {e}")
        #raise Exception(f"Error: executing Python file: {e}")
    return "".join(response)

def run_python_file_docker(working_directory_full_path:str=None,filename=None,arguments:list=[],install_pkg:list=[])->CompletedProcess:
    import io,uuid
    try:
        import docker
    except ImportError as e:
        raise ImportError("You must install package `docker` to run this tool: for instance run `pip install docker`.") from e

    pkg = " ".join(install_pkg).strip()
    try:
        client = docker.from_env()
    except Exception as e:
        raise Exception("Please make sure the docker deamon is running!!!!")

    image_name = str(uuid.uuid4()) #"python-runner"

    if pkg is not None and len(pkg)> 0:
        pkg = "&& pip install --no-cache-dir {}".format(pkg)
    else:
        pkg = ''

    dockerfile_str = '''
    FROM python:3.13-slim

    # Create a non-root user and group
    RUN addgroup --system appuser && adduser --system --ingroup appuser appuser

    WORKDIR /app

    # Create virtual environment and install packages there
    RUN python -m venv /venv \\
        && . /venv/bin/activate \\
        {}

    # Change to non-root user
    USER appuser
    '''.format(pkg)

    result = {}
    # Build image using an in-memory file (BytesIO)
    image, logs = client.images.build(
        fileobj=io.BytesIO(dockerfile_str.encode('utf-8')),
        tag=image_name,
        rm=True,
        pull=False,
        custom_context=False,
        encoding="utf-8"
    )
    # for chunk in logs:
    #     print(chunk.get('stream', ''))

    # Run a container
    if arguments is not None and len(arguments) > 0:
        command = ["python3", filename] + arguments
    else:
        command = ["python3", filename]

    container = client.containers.create(
        image=image_name,
        command=command,
        volumes={
        working_directory_full_path: {
            "bind": "/app",
            "mode": "rw"  # or "ro" for read-only
        }
    },
        security_opt=["no-new-privileges:true"],
        user="appuser",  # run as non-root user
        environment={"PATH": "/venv/bin:$PATH"},  # activate venv
    )
    
    try:
        # Start the container
        container.start()

        # Wait for the container to finish and get the exit code
        docker_result = container.wait(timeout=30)  # returns dict like {'StatusCode': 0}
        exit_code = docker_result['StatusCode']
        result['returncode']=exit_code

        # Get logs (stdout)
        std_out_logs = container.logs(stdout=True, stderr=False).decode('utf-8')
        result['stdout']=std_out_logs

        # Get logs (stderr)
        std_err_logs = container.logs(stdout=False, stderr=True).decode('utf-8')
        result['stderr']=std_err_logs
    except Exception as e:
        raise Exception("Error starting the container",e)
    finally:
        # Clean up the container if needed
        container.remove()

        # Step 1: Remove the image
        try:
            client.images.remove(image=image_name, force=True)
            #print(f"Removed image: {image_name}")
        except docker.errors.ImageNotFound:
            print(f"Image '{image_name}' not found.")
        except docker.errors.APIError as e:
            print(f"Failed to remove image: {e}")

        # Step 2: Prune unused images
        prune_result = client.images.prune()
        #print("Pruned unused images:", prune_result)

    return fake_completed_process(command,result['returncode'],result['stdout'],result['stderr'])

def fake_completed_process(args, returncode=0, stdout='', stderr=''):
    #from subprocess import CompletedProcess
    return CompletedProcess(args=args, returncode=returncode, stdout=stdout, stderr=stderr)