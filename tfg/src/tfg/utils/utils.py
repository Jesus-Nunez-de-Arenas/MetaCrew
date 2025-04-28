from langchain_openai import ChatOpenAI
import yaml
from .util_functions import clean_json, eliminate_folder, clean_all_python_files
from .util_functions import initialize_crew, create_workflow, create_single_crew, create_multi_crews, run_new_crew, single_main_code, single_crew_code
from .util_functions import copy_logging_utils, yaml_agents_tasks, copy_pyproject, copy_env
import os
import json


############################################################################
# --------------------------------- Code --------------------------------- #
############################################################################


def new_crew() -> None:
    
    """
    Creates the crew composed by the agents created.
    """
    
    initialize_crew(os.path.abspath(os.path.join(__file__, "../../../../..")))
    
    
    eliminate_folder(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                                os.getenv("CREW_NAME") + "/knowledge/")))
    
    clean_json(os.getenv("OUTPUT_DIR"))
    
    # Modifies the agents and tasks YAML files
    yaml_agents_tasks()
    
    # Copies the utils used for logging to the utils folder
    copy_logging_utils()
    
    workflow_path = os.path.join(os.getenv("OUTPUT_DIR"), "workflow.json")
    
    
    # Clean the comments in the .py files
    clean_all_python_files(os.path.abspath(os.path.join(__file__, "../../../../../" + 
                                                        os.getenv("CREW_NAME") + "/src/")))

    # Modify the main.py file based on the context information
    # single_main_code(workflow_path=workflow_path)
    
    task_yaml_path = os.path.abspath(os.path.join(__file__, "../../../../../" +
                                                os.getenv("CREW_NAME") + "/src/" + 
                                                os.getenv("CREW_NAME") + "/config/tasks.yaml"))
    
    agents_yaml_path = os.path.abspath(os.path.join(__file__, "../../../../../" +
                                                os.getenv("CREW_NAME") + "/src/" + 
                                                os.getenv("CREW_NAME") + "/config/agents.yaml"))
    
    # Modify the crew.py file based on the context information
    # single_crew_code(task_yaml_path=task_yaml_path, 
    #                  agents_yaml_path=agents_yaml_path)
    
    # copy_pyproject()
    
    # copy_env()

    # run_new_crew(os.path.abspath(os.path.join(__file__, "../../../../../" + 
    #                                             os.getenv("CREW_NAME"))))
    
    
def clean_folders() -> None:
    """
    Eliminate folders not needed for the execution.
    """
    
    eliminate_folder(os.path.join(__file__, "../../../..", "db"))
    eliminate_folder(os.path.join(__file__, "../../../..", "output"))
    eliminate_folder(os.path.join(__file__, "../../../../..", os.getenv("CREW_NAME")))
    