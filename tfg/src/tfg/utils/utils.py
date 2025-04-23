import yaml
from .util_functions import clean_json_file, eliminate_folder, clean_all_python_files, strip_markdown_fencing
from .util_functions import initialize_crew, create_workflow, create_agent_yaml, create_task_yaml, create_single_crew, create_multi_crews, run_new_crew
from .langchain_utils import run_agent_on_file, run_subtask_agent_on_file
import os
import json


############################################################################
# --------------------------------- Code --------------------------------- #
############################################################################


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
    

def new_crew() -> None:
    
    """
    Creates the crew composed by the agents created.
    """
    
    #initialize_crew(os.path.abspath(os.path.join(__file__, "../../../../..")))
    
    
    #eliminate_folder(os.path.abspath(os.path.join(__file__, "../../../../../" + 
    #                                              os.getenv("CREW_NAME") + "/knowledge/")))
    
    #clean_json(os.getenv("OUTPUT_DIR"))
    
    try:
        # create_agent_yaml(json_path=os.getenv("OUTPUT_DIR") + 'experts.json',
        #                 yaml_path=os.path.abspath(os.path.join(__file__, "../../../../../" + 
        #                                                         os.getenv("CREW_NAME") + "/src/" + 
        #                                                         os.getenv("CREW_NAME") + 
        #                                                         "/config/agents.yaml")))
        
        # Run the agent on the file and get the YAML
        agents_yaml = run_agent_on_file(file_path=os.getenv("OUTPUT_DIR") + 'experts.json')
        
        # Remove markdown-style triple backticks
        clean_yaml_str = strip_markdown_fencing(agents_yaml)
        
        # Convert YAML string to a Python dict
        clean_dict = yaml.safe_load(clean_yaml_str)
        
        with open(os.path.abspath(os.path.join(__file__, "../../../../../" +
                                                        os.getenv("CREW_NAME") + "/src/" +
                                                        os.getenv("CREW_NAME") +
                                                        "/config/agents.yaml")), 'w') as file:

            yaml.safe_dump(clean_dict, file, default_flow_style=False, sort_keys=False)
        
    except Exception as e:
        raise Exception(f"Error creating agent YAML file: {e}")
        
    try:
        # create_task_yaml(task_path=os.getenv("OUTPUT_DIR") + 'subtasks.json',
        #                 expert_path=os.getenv("OUTPUT_DIR") + 'experts.json',
        #                 yaml_path=os.path.abspath(os.path.join(__file__, "../../../../../" + 
        #                                                         os.getenv("CREW_NAME") + "/src/" + 
        #                                                         os.getenv("CREW_NAME") + 
        #                                                         "/config/tasks.yaml")))

        # Run the agent on the file and get the YAML
        subtasks_yaml = run_subtask_agent_on_file(file_path=os.getenv("OUTPUT_DIR") + 'subtasks.json')

        # Remove markdown-style triple backticks
        clean_yaml_str = strip_markdown_fencing(subtasks_yaml)

        # Convert YAML string to a Python dict
        clean_dict = yaml.safe_load(clean_yaml_str)

        with open(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                                        os.getenv("CREW_NAME") + "/src/" + 
                                                        os.getenv("CREW_NAME") + 
                                                        "/config/tasks.yaml")), 'w') as file:
            yaml.safe_dump(clean_dict, file, default_flow_style=False, sort_keys=False)

    except Exception as e:
        raise Exception(f"Error creating task YAML file: {e}")    

    clean_all_python_files(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                                        os.getenv("CREW_NAME") + "/src/")))

    # run_new_crew(os.path.abspath(os.path.join(__file__, "../../../../..")))
    
def clean_folders() -> None:
    """
    Eliminate folders not needed for the execution.
    """
    
    eliminate_folder(os.path.join(__file__, "../../../..", "db"))
    eliminate_folder(os.path.join(__file__, "../../../..", "output"))
    eliminate_folder(os.path.join(__file__, "../../../../..", os.getenv("CREW_NAME")))
    