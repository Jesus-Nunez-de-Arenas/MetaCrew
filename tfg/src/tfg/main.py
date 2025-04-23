#!/usr/bin/env python
import sys
import os
import logging
from datetime import datetime
import warnings
from tfg.crew import TfgCrew
from tfg.utils.utils import new_crew, clean_folders
from time import sleep
import atexit

############################################################################
# ------------------------ Logging Setup --------------------------------- #
############################################################################

# Create a logs folder if it doesn't exist
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)

# Create a log file with a timestamp
log_file = open(os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"), 'w')

class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()  # Ensure immediate writing

    def flush(self):
        for stream in self.streams:
            stream.flush()

# Redirect stdout and stderr to both terminal and log file
sys.stdout = Tee(sys.stdout, log_file)
sys.stderr = Tee(sys.stderr, log_file)

# Ensure the log file is closed when the program exits
@atexit.register
def close_log_file():
    log_file.close()


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


############################################################################
#                                                                          #
#                                                                          #
#                                  RUN CREW                                #
#                                                                          #
#                                                                          #
############################################################################

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Create a story'
    }
    
    #clean_folders()
    
    #TfgCrew().crew().kickoff(inputs=inputs)
    
    new_crew()
    
    
############################################################################
#                                                                          #
#                                                                          #
#                                 TRAIN CREW                               #
#                                                                          #
#                                                                          #
############################################################################


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


############################################################################
#                                                                          #
#                                                                          #
#                                REPLAY CREW                               #
#                                                                          #
#                                                                          #
############################################################################


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TfgCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


############################################################################
#                                                                          #
#                                                                          #
#                                  TEST CREW                               #
#                                                                          #
#                                                                          #
############################################################################

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
