#!/usr/bin/env python
import socket
import sys
import os
import logging
from datetime import datetime
import warnings
from tfg.crew import TfgCrew
from tfg.utils.utils import new_crew, clean_folders
from tfg.utils.logging_utils import close_log_file, setup_logging
from time import sleep
import atexit

############################################################################
# ------------------------ Warnings Supressions -------------------------- #
############################################################################

# Suppress Pydantic deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")
# Suppress specific warnings from chromadb
warnings.filterwarnings("ignore", category=DeprecationWarning, module="chromadb")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")


############################################################################
# ------------------------ Global Logging Setup -------------------------- #
############################################################################

# Set up logging
log_file, log_file_path = setup_logging()

# Ensure the log file is closed when the program exits
@atexit.register
def cleanup():
    close_log_file(log_file)

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
    try:
        inputs = {
            'topic': 'Create a story',
        }
        
        clean_folders()
        
        TfgCrew().crew().kickoff(inputs=inputs)
        
        new_crew()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    sys.exit(0)
    
    
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
    
    sys.exit(0)


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
    
    sys.exit(0)


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

    sys.exit(0)