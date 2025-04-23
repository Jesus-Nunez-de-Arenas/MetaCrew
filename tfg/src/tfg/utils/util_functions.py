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
#                         CLEAN FOLDERS AND FILES                          #
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

def strip_markdown_fencing(yaml_string: str) -> str:
    if yaml_string.strip().startswith("```yaml"):
        return "\n".join(
            line for line in yaml_string.strip().splitlines()
            if not line.strip().startswith("```")
        )
    return yaml_string
    
    
############################################################################
#                                                                          #
#                                                                          #
#                             CREATE CUSTOM CREW                           #
#                                                                          #
#                                                                          #
############################################################################
    
def initialize_crew(crew_path):
    
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


def create_agent_yaml(json_path: str, yaml_path: str) -> None:
    """
    Creates an agents.yaml file with the agents created.
    The agents come from the experts.json file created by the crew.
    The agents.yaml file is created in the output folder.
    
    Args:
        json_path (str): The path to the experts.json file.
        yaml_path (str): The path to the agents.yaml file.
        
    Raises:
        Exception: If the agents.yaml file cannot be created, an exception is raised with the error message.

    """
    try:
        # Load experts.json
        with open(json_path, 'r') as file:
            try:
                experts = json.load(file)
            except json.JSONDecodeError:
                clean_json_file(json_path)
                with open(json_path, 'r') as file:
                    experts = json.load(file)

        # Eliminate the first level of the JSON if necessary
        if isinstance(experts, dict):
            experts = experts.get(next(iter(experts)), experts)

        # Transform experts into the agents.yaml structure
        agents = {}
        for expert in experts:
            name = expert["name"].lower().replace(" ", "_")
            agents[name] = {
                "role": f"{expert['role']}",
                "goal": f"The main task is {{topic}}. {expert['goal']}",
                "backstory": f"{expert['backstory']}"
            }

        # Overwrite the agents.yaml file
        with open(yaml_path, 'w') as file:
            yaml.safe_dump(agents, file, default_flow_style=False)

    except Exception as e:
        raise Exception(f"Error creating agents.yaml file: {e}")


def create_task_yaml(task_path: str, expert_path: str, yaml_path: str) -> None:
    """
    Creates a tasks.yaml file with the tasks created.
    The tasks come from the subtasks.json file created by the crew.
    The tasks.yaml file is created in the output folder.
    
    Args:
        task_path (str): The path to the subtasks.json file.
        expert_path (str): The path to the experts.json file.
        workflow_path (str): The path to the workflow.json file.
        yaml_path (str): The path to the tasks.yaml file.
        
    Raises:
        Exception: If the tasks.yaml file cannot be created, an exception is raised with the error message.
        ValueError: If the tasks data is not a list or if the workflow data is not a dictionary or valid list.

    """
    try:
        # Load experts.json
        with open(expert_path, 'r') as file:
            try:
                experts = json.load(file)
            except json.JSONDecodeError:
                clean_json_file(expert_path)
                with open(expert_path, 'r') as file:
                    experts = json.load(file)

        # Load subtasks.json
        with open(task_path, 'r') as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                clean_json_file(task_path)
                with open(task_path, 'r') as file:
                    tasks = json.load(file)

        # Eliminate the first level of the JSON if necessary
        if isinstance(experts, dict):
            experts = experts.get(next(iter(experts)), experts)

        if isinstance(tasks, dict):
            tasks = tasks.get(next(iter(tasks)), tasks)

        # Ensure tasks is a list
        if not isinstance(tasks, list):
            raise ValueError("Tasks data is not a list. Please check the structure of subtasks.json.")

        # Transform tasks into the tasks.yaml structure
        tasks_yaml = {}
        for task in tasks:
            if not isinstance(task, dict):
                raise ValueError("Each task must be a dictionary. Please check the structure of subtasks.json.")
            name = task["name"].lower().replace(" ", "_")
            tasks_yaml[name] = {
                "description": task.get("description", "No description provided."),
                "expected_output": task.get("expected_output", "No expected output provided."),
            }

        # Write the tasks.yaml file
        with open(yaml_path, 'w') as file:
            yaml.safe_dump(tasks_yaml, file, default_flow_style=False)

    except Exception as e:
        raise Exception(f"Error creating tasks.yaml file: {e}")


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


def run_new_crew(crew_path):
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
    
############################################################################
#                                                                          #
#                                                                          #
#                           LANGCHAIN PREPROCESSING                        #
#                                                                          #
#                                                                          #
############################################################################

def extract_text_from_file(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".json":
        return extract_from_json(file_path)
    elif ext in [".yaml", ".yml"]:
        return extract_from_yaml(file_path)
    elif ext == ".csv":
        return extract_from_csv(file_path)
    else:
        return extract_from_unstructured(file_path)

def extract_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return flatten_json(data)

def extract_from_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return flatten_json(data)

def extract_from_csv(file_path):
    rows = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return flatten_json(rows)

def extract_from_unstructured(file_path):
    elements = partition(file_path)
    return "\n".join([el.text for el in elements if el.text])

def flatten_json(y):
    out = []

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], f'{name}{a}_')
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, f'{name}{i}_')
        else:
            out.append(f"{name[:-1]}: {x}")

    flatten(y)
    return "\n".join(out)