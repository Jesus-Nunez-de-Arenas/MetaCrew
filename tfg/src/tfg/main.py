#!/usr/bin/env python
import sys
import os
import warnings
from tfg.crew import TfgCrew
from tfg.utils.utils import clean, new_crew, clean_folders
from time import sleep

############################################################################
# ----------------------- Environment Variables -------------------------- #
############################################################################

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'
os.environ["OPENAI_EMBEDDING_MODEL_NAME"] = 'text-embedding-3-small'
os.environ["CREWAI_STORAGE_DIR"] = './storage/'
os.environ["OUTPUT_DIR"] = './output/'
os.environ["CREW_NAME"] = 'tfg_answer_crew'
# os.environ["GOOGLE_MODEL_NAME"] = 'gemini-2.0-flash'

############################################################################
# ------------------------ Warnings Supressions -------------------------- #
############################################################################

# Suppress Pydantic deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")
# Suppress specific warnings from chromadb
warnings.filterwarnings("ignore", message="Accessing the 'model_fields' attribute on the instance is deprecated")
warnings.filterwarnings("ignore", message="The `schema` method is deprecated; use `model_json_schema` instead")
# Suppress warnings about deprecated Pydantic V1 validators
warnings.filterwarnings("ignore", message="Pydantic V1 style `@validator` validators are deprecated")
# Suppress warnings about deprecated class-based `config` in Pydantic
warnings.filterwarnings("ignore", message="Support for class-based `config` is deprecated, use ConfigDict instead")
# Suppress warnings about extra keyword arguments in Pydantic `Field`
warnings.filterwarnings("ignore", message="Using extra keyword arguments on `Field` is deprecated and will be removed")
# Suppress specific warnings from local_persistent_hnsw
warnings.filterwarnings("ignore", message="Number of requested results .* is greater than number of elements in index .*")

############################################################################
# --------------------------------- Code --------------------------------- #
############################################################################


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Create a story'
    }
    
    clean_folders()
    
    TfgCrew().crew().kickoff(inputs=inputs)
    
    #clean(os.getenv("OUTPUT_DIR"))
    
    new_crew()
    
    
def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        TfgCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TfgCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        TfgCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
