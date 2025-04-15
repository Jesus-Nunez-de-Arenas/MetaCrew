#!/usr/bin/env python
import sys
import os
from tfg.crew import TfgCrew
from tfg.utils.utils import clean, create_crew, clean_folders
from time import sleep

############################################################################
# ----------------------- Environment Variables -------------------------- #
############################################################################

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'
os.environ["OPENAI_EMBEDDING_MODEL_NAME"] = 'text-embedding-3-small'
os.environ["CREWAI_STORAGE_DIR"] = './storage/'
os.environ["OUTPUT_DIR"] = './output/'
# os.environ["GOOGLE_MODEL_NAME"] = 'gemini-2.0-flash'


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
    
    create_crew()
    
    
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
