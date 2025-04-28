import json
import os
import shutil
import subprocess
import yaml
from unstructured.partition.auto import partition
import json
import csv
from .langchain_utils import run_agent_on_file, run_subtask_agent_on_file, modify_single_main_python_code, modify_single_crew_python_code

############################################################################
# --------------------------------- Code --------------------------------- #
############################################################################




############################################################################
#                                                                          #
#                                                                          #
#                            FOLDERS AND FILES                             #
#                                                                          #
#                                                                          #
############################################################################


def clean_json_file(file_path: str) -> None:
    """
    Cleans a JSON file by removing unnecessary lines at the beginning and end,
    and formatting it properly.

    Args:
        file_path (str): The path to the JSON file to be cleaned.
        
    Raises:
        Exception: If the JSON file cannot be cleaned, an exception is raised with the error message.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove the first and last lines
        cleaned_lines = lines[1:-1]

        # Join the remaining lines and parse as JSON
        cleaned_content = ''.join(cleaned_lines)
        json_data = json.loads(cleaned_content)

        # Write the cleaned and formatted JSON back to the file
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)

    except Exception as e:
        raise Exception(f"Error cleaning JSON file {file_path}: {e}")
    
    
def clean_json(storage_path: str) -> None:
    
    """
    Cleans the JSON files in the specified storage path.
    This function removes unnecessary lines at the beginning and end of the JSON files,
    and formats them properly.

    Args:
        storage_path (str): The path to the storage directory containing the JSON files to be cleaned.
    """
    
    try:    
        with open(os.path.join(storage_path, 'subtasks.json'), 'r') as file:
            try: 
                json.load(file)
            except json.JSONDecodeError:
                clean_json_file(os.path.join(storage_path, 'subtasks.json'))
                
        with open(os.path.join(storage_path, 'experts.json'), 'r') as file:
            try: 
                json.load(file)
            except json.JSONDecodeError:
                clean_json_file(os.path.join(storage_path, 'experts.json'))
                
        with open(os.path.join(storage_path, 'workflow.json'), 'r') as file:
            try: 
                json.load(file)
            except json.JSONDecodeError:
                clean_json_file(os.path.join(storage_path, 'workflow.json'))
    except Exception as e:
        raise Exception(f"Error cleaning JSON files: {e}")
    
    
def eliminate_folder(storage_path: str) -> None:
    """
    Eliminate folders not needed for the execution.
    
    Args:
        storage_path (str): The path to the folder to be eliminated.
        
    Raises:
        Exception: If the folder cannot be eliminated, an exception is raised with the error message.
    """
    try:
        if os.path.exists(storage_path):
            shutil.rmtree(storage_path)

    except Exception as e:
        raise Exception(f"Error eliminating folder: {e}")
    
    
    
def clean_comments_python_file(file_path: str) -> None:
    """
    Cleans a Python file by removing comments.

    Args:
        file_path (str): The path to the Python file to be cleaned.

    """

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove comments
        cleaned_lines = [line for line in lines if not line.strip().startswith('#')]

        # Write the cleaned lines back to the file

        with open(file_path, 'w') as file:
            file.writelines(cleaned_lines)

    except Exception as e:
        raise Exception(f"Error cleaning Python file {file_path}: {e}")
    
    
def clean_all_python_files(storage_path: str) -> None:
    """
    Cleans all Python files in a directory by removing comments.
    
    Args:
        storage_path (str): The path to the directory containing the Python files to be cleaned.
        
        
    Raises:
        Exception: If the Python files cannot be cleaned, an exception is raised with the error message.
    """
    
    
    try:
        for root, dirs, files in os.walk(storage_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    clean_comments_python_file(file_path)
                    
    except Exception as e:
        
        raise Exception(f"Error cleaning Python files in {storage_path}: {e}")

def strip_markdown_fencing_yaml(yaml_string: str) -> str:
    if yaml_string.strip().startswith("```yaml"):
        return "\n".join(
            line for line in yaml_string.strip().splitlines()
            if not line.strip().startswith("```")
        )
    return yaml_string

def strip_markdown_fencing_python(text: str) -> str:
    if text.strip().startswith("```python"):
        return "\n".join(
            line for line in text.strip().splitlines()
            if not line.strip().startswith("```")
        )
    return text
    
def copy_file(src: str, dst: str) -> None:
    """
    Copy a file from source to destination.

    Args:
        src (str): The path to the source file.
        dst (str): The path to the destination file.
        
        
    Raises:
        Exception: If the file cannot be copied, an exception is raised with the error message.
    """
    
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
    except Exception as e:
        raise Exception(f"Error copying file from {src} to {dst}: {e}")
    
    
############################################################################
#                                                                          #
#                                                                          #
#                             CREATE CUSTOM CREW                           #
#                                                                          #
#                                                                          #
############################################################################
    
def initialize_crew(crew_path) -> None:
    
    """
    Initializes the crew using the crewai CLI.
    This function creates a crew with the specified configuration and API key.
    
    Args:
        crew_path (str): The path to the crew directory.

    Raises:
        Exception: If the crew creation fails, an exception is raised with the error message.
        The error message includes the details of the subprocess call that failed.
    """
    
    try:
        provider_choice = "1\n3\n" + os.getenv("OPENAI_API_KEY") + "\n"
        subprocess.run(
            ["crewai", "create", "crew", os.getenv("CREW_NAME")], 
            cwd=crew_path, 
            input=provider_choice.encode(),
            check=True
            )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to create crew: {e}")
    
    
def create_workflow():
    pass


def create_single_crew():
    """
    Creates a crew where the agents have each one task.
    
    """
    pass


def create_multi_crews():
    """
    Creates a crew where the agents have multiple tasks or a task has multiple agents.
    
    """
    pass


def run_new_crew(crew_path) -> None:
    """
    Run the new crew.
    
    Args:
        crew_path (str): The path to the crew directory.
        
    Raises:
        Exception: If the new crew cannot be run, an exception is raised with the error message.
        The error message includes the details of the subprocess call that failed.    
    """
    
    # Set the environment variable for the crew path
    # try:
    #     subprocess.run(
    #         ["poetry", "lock"], 
    #         cwd=crew_path, 
    #         check=True
    #         )   
    
    # except subprocess.CalledProcessError as e:
    #     raise Exception(f"Failed to run poetry: {e}")
    
    # Install the new crew using the crewai CLI
    try:
        subprocess.run(
            ["crewai", "install"], 
            cwd=crew_path, 
            check=True
            )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to install the new crew: {e}")
    
    
    # Run the new crew using the crewai CLI
    try:
        subprocess.run(
            ["crewai", "run"], 
            cwd=crew_path, 
            check=True
            )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to run the new crew: {e}")
    
############################################################################
#                                                                          #
#                                                                          #
#                                    CREW                                  #
#                                                                          #
#                                                                          #
############################################################################

def single_main_code(workflow_path: str) -> None:
    
    try:
    
        main_code = modify_single_main_python_code(
            file_path_python=os.path.abspath(os.path.join(__file__, "../../../../../" +
                                                        os.getenv("CREW_NAME") + "/src/" +
                                                        os.getenv("CREW_NAME") + "/main.py")),
            file_path_context=os.path.abspath(workflow_path)
        )
        try:
            clean_main_code = strip_markdown_fencing_python(main_code)
        except Exception as e:
            clean_main_code = main_code
        
        with open(os.path.abspath(os.path.join(__file__, "../../../../../" +
                                os.getenv("CREW_NAME") + "/src/" + 
                                os.getenv("CREW_NAME") + "/main.py")), 'w') as file:
            file.write(clean_main_code)
        
    except Exception as e:
        raise Exception(f"Error modifying main Python code: {e}")
    

def single_crew_code(task_yaml_path: str, agents_yaml_path: str) -> None:
    try:
        
        crew_code = modify_single_crew_python_code(file_path_python=os.path.abspath(os.path.join(__file__, "../../../../../" +
                                                os.getenv("CREW_NAME") + "/src/" + 
                                                os.getenv("CREW_NAME") + "/crew.py")), 
                                            file_path_context_task=task_yaml_path,
                                            file_path_context_agents=agents_yaml_path)
        
        try: 
            clean_crew_code = strip_markdown_fencing_python(crew_code)
        except Exception as e:
            clean_crew_code = crew_code
        
        with open(os.path.abspath(os.path.join(__file__, "../../../../../" +
                                os.getenv("CREW_NAME") + "/src/" + 
                                os.getenv("CREW_NAME") + "/crew.py")), 'w') as file:
            file.write(clean_crew_code)
            
    except Exception as e:
        raise Exception(f"Error modifying crew Python code: {e}")
    
def copy_logging_utils() -> None:
    """
    Copy the logging_utils.py file to the crew directory.
    
    Raises:
        Exception: If the file cannot be copied, an exception is raised with the error message.
    """
    
    try:
        copy_file(
            src=os.path.abspath(os.path.join(os.path.dirname(__file__), "logging_utils.py")),
            dst=os.path.abspath(os.path.join(__file__, "../../../../../" +
                                              os.getenv("CREW_NAME") + "/src/" +
                                              os.getenv("CREW_NAME") + "/utils/logging_utils.py"))
        )
    except Exception as e:
        raise Exception(f"Error copying logging_utils.py: {e}")
    
def copy_pyproject() -> None:
    """
    Copy the pyproject.toml file to the crew directory.
    
    Raises:
        Exception: If the file cannot be copied, an exception is raised with the error message.
    """
    
    try:
        copy_file(
            src=os.path.abspath(os.path.join(__file__, "../../../../" + "pyproject.toml")),
            dst=os.path.abspath(os.path.join(__file__, "../../../../../" +
                                              os.getenv("CREW_NAME") + "/pyproject.toml"))
        )
    except Exception as e:
        raise Exception(f"Error copying pyproject.toml: {e}")
    
def copy_env() -> None:
    """
    Copy the .env file to the crew directory.
    
    Raises:
        Exception: If the file cannot be copied, an exception is raised with the error message.
    """
    
    try:
        copy_file(
            src=os.path.abspath(os.path.join(__file__, "../../../../" + ".env")),
            dst=os.path.abspath(os.path.join(__file__, "../../../../../" +
                                              os.getenv("CREW_NAME") + "/.env"))
        )
    except Exception as e:
        raise Exception(f"Error copying .env: {e}")
    
def yaml_agents_tasks() -> None:
    """
    Create the YAML files for the agents and tasks.
    
    Raises:
        Exception: If the YAML files cannot be created, an exception is raised with the error message.
    """
    
    try:
        # Run the agent on the file and get the YAML
        agents_yaml = run_agent_on_file(file_path=os.getenv("OUTPUT_DIR") + 'experts.json')
        
        # Remove markdown-style triple backticks
        clean_yaml_str = strip_markdown_fencing_yaml(agents_yaml)
        
        with open(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                    os.getenv("CREW_NAME") + "/src/" + 
                                    os.getenv("CREW_NAME") + 
                                    "/config/agents.yaml")), 'w') as file:
            file.write(clean_yaml_str)
            
    except Exception as e:
        raise Exception(f"Error creating agent YAML file: {e}")
    try:
        # Run the agent on the file and get the YAML
        agents_yaml = run_agent_on_file(file_path=os.getenv("OUTPUT_DIR") + 'experts.json')

        # Remove markdown-style triple backticks
        clean_yaml_str = strip_markdown_fencing_yaml(agents_yaml)
        
        with open(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                os.getenv("CREW_NAME") + "/src/" + 
                                os.getenv("CREW_NAME") + 
                                "/config/agents.yaml")), 'w') as file:
            file.write(clean_yaml_str)
        
    except Exception as e:
        raise Exception(f"Error creating agent YAML file: {e}")
        
    try:
        # Run the agent on the file and get the YAML
        subtasks_yaml = run_subtask_agent_on_file(file_path=os.getenv("OUTPUT_DIR") + 'subtasks.json')
        
        # Remove markdown-style triple backticks
        clean_yaml_str = strip_markdown_fencing_yaml(subtasks_yaml)

        with open(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                os.getenv("CREW_NAME") + "/src/" + 
                                os.getenv("CREW_NAME") + 
                                "/config/tasks.yaml")), 'w') as file:
            file.write(clean_yaml_str)

    except Exception as e:
        raise Exception(f"Error creating task YAML file: {e}")