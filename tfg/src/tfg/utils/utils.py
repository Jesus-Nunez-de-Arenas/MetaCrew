from .util_functions import clean_json_file, eliminate_folder, clean_all_python_files
from .util_functions import initialize_crew, create_workflow, create_agent_yaml, create_task_yaml, create_single_crew, create_multi_crews, run_new_crew
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
    

def new_crew() -> None:
    
    """
    Creates the crew composed by the agents created.
    """
    
    crew_name = os.getenv("CREW_NAME")
    
    initialize_crew(os.path.abspath(os.path.join(__file__, "../../../../..")), crew_name)
    
    
    eliminate_folder(os.path.abspath(os.path.join(__file__, "../../../../../" + crew_name + "/knowledge/")))
    
    
    create_agent_yaml(json_path=os.getenv("OUTPUT_DIR") + 'experts.json',
                      yaml_path=os.path.abspath(os.path.join(__file__, "../../../../../" + crew_name + "/src/" + crew_name + "/config/agents.yaml")))
    
    
    create_task_yaml(task_path=os.getenv("OUTPUT_DIR") + 'subtasks.json',
                     expert_path=os.getenv("OUTPUT_DIR") + 'experts.json',
                     workflow_path=os.getenv("OUTPUT_DIR") + 'workflow.json',
                     yaml_path=os.path.abspath(os.path.join(__file__, "../../../../../" + crew_name + "/src/" + crew_name + "/config/tasks.yaml")))
    
    # run_new_crew(os.path.abspath(os.path.join(__file__, "../../../../..")), crew_name)


    clean_all_python_files(os.path.abspath(os.path.join(__file__, "../../../../../" + crew_name + "/src/")))
    
def clean_folders() -> None:
    """
    Eliminate folders not needed for the execution.
    """
    
    crew_name = os.getenv("CREW_NAME")
    
    eliminate_folder(os.path.join(__file__, "../../../..", "db"))
    eliminate_folder(os.path.join(__file__, "../../../..", "output"))
    eliminate_folder(os.path.join(__file__, "../../../../..", crew_name))
    