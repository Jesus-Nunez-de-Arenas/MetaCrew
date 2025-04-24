from langchain_openai import ChatOpenAI
import yaml
from .util_functions import clean_json_file, eliminate_folder, clean_all_python_files, strip_markdown_fencing_yaml, copy_file, strip_markdown_fencing_python
from .util_functions import initialize_crew, create_workflow, create_single_crew, create_multi_crews, run_new_crew
from .langchain_utils import run_agent_on_file, run_subtask_agent_on_file, modify_single_main_python_code, modify_single_crew_python_code
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
    
    initialize_crew(os.path.abspath(os.path.join(__file__, "../../../../..")))
    
    
    eliminate_folder(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                                os.getenv("CREW_NAME") + "/knowledge/")))
    
    clean_json(os.getenv("OUTPUT_DIR"))
    
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
    
    try:
        copy_file(
            src=os.path.abspath(os.path.join(os.path.dirname(__file__), "logging_utils.py")),
            dst=os.path.abspath(os.path.join(__file__, "../../../../../" +
                                              os.getenv("CREW_NAME") + "/src/" +
                                              os.getenv("CREW_NAME") + "/utils/logging_utils.py"))
        )
    except Exception as e:
        raise Exception(f"Error copying logging_utils.py: {e}")
    
    workflow_path = os.path.join(os.getenv("OUTPUT_DIR"), "workflow.json")
    
    clean_all_python_files(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                                        os.getenv("CREW_NAME") + "/src/")))
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
    
    task_yaml_path = os.path.abspath(os.path.join(__file__, "../../../../../" +
                                                os.getenv("CREW_NAME") + "/src/" + 
                                                os.getenv("CREW_NAME") + "/config/tasks.yaml"))
    
    agents_yaml_path = os.path.abspath(os.path.join(__file__, "../../../../../" +
                                                os.getenv("CREW_NAME") + "/src/" + 
                                                os.getenv("CREW_NAME") + "/config/agents.yaml"))
    
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


    # run_new_crew(os.path.abspath(os.path.join(__file__, "../../../../..")))
    
def clean_folders() -> None:
    """
    Eliminate folders not needed for the execution.
    """
    
    eliminate_folder(os.path.join(__file__, "../../../..", "db"))
    eliminate_folder(os.path.join(__file__, "../../../..", "output"))
    eliminate_folder(os.path.join(__file__, "../../../../..", os.getenv("CREW_NAME")))
    