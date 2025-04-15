from .util_functions import clean_json_file, eliminate_folder
from .util_functions import initialize_crew, create_workflow, create_agent_yaml, create_task_yaml, create_single_crew, create_multi_crews
import os


############################################################################
# --------------------------------- Code --------------------------------- #
############################################################################


def clean(storage_path: str) -> None:
    
    """
    Cleans the JSON files in the specified storage path.
    This function removes unnecessary lines at the beginning and end of the JSON files,
    and formats them properly.

    Args:
        storage_path (str): The path to the storage directory containing the JSON files to be cleaned.
    """
    
    try:    
        clean_json_file(os.path.join(storage_path, 'subtasks.json'))
    except Exception as e:
        raise Exception(f"JSON file in {storage_path} already cleaned: {e}")
    
    try:
        clean_json_file(os.path.join(storage_path, 'experts.json'))
    except Exception as e:
        raise Exception(f"JSON file in {storage_path} already cleaned: {e}")
    
    try:
        clean_json_file(os.path.join(storage_path, 'workflow.json'))
    except Exception as e:
        raise Exception(f"JSON file in {storage_path} already cleaned: {e}")
    

def create_crew() -> None:
    
    """
    Creates the crew composed by the agents created.
    """
    
    initialize_crew(os.path.abspath(os.path.join(__file__, "../../../../..")))
    create_agent_yaml(json_path=os.getenv("OUTPUT_DIR") + 'experts.json',
                      yaml_path=os.path.abspath(os.path.join(__file__, "../../../../../answer/src/answer/config/agents.yaml")))
    create_task_yaml(task_path=os.getenv("OUTPUT_DIR") + 'subtasks.json',
                     expert_path=os.getenv("OUTPUT_DIR") + 'experts.json',
                     workflow_path=os.getenv("OUTPUT_DIR") + 'workflow.json',
                     yaml_path=os.path.abspath(os.path.join(__file__, "../../../../../answer/src/answer/config/tasks.yaml")))

    
def clean_folders() -> None:
    """
    Eliminate folders not needed for the execution.
    """
    
    eliminate_folder(os.path.join(__file__, "../../../..", "db"))
    eliminate_folder(os.path.join(__file__, "../../../..", "output"))
    eliminate_folder(os.path.join(__file__, "../../../../..", "answer"))
    