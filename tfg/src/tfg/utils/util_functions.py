import json
import os
import shutil
import subprocess
import yaml
from unstructured.partition.auto import partition
import json
import csv


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
    try:
        subprocess.run(
            ["poetry", "lock"], 
            cwd=crew_path, 
            check=True
            )   
    
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to run poetry: {e}")
    
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