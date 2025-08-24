#!/usr/bin/env python
import sys
import os

# Disable CrewAI telemetry to avoid connection errors
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not found. Please install it with: poetry add python-dotenv")

# Set UTF-8 encoding for Windows
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Set console encoding for Windows
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')


import socket
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
            #'topic': 'Create a story with a topic given that incorporates the answers to 5 trivia questions that the user will provide',
            #'topic': 'Identify the 3 words best associated with a specific word from a word list given by the user',
            # 'topic': 'Q: There are <n> houses in a row, numbered 1 on the left to <n> on the right. There is one person living in each house. The people in these houses have different characteristics: <characteristics> Clue(s): <Clues>.  <Question>?   <n choices>',
            # 'topic': 'You have to solve a test on a specific subject. The test consists of multiple-choice questions, each with a set of possible answers and a correct answer. Some questions will include images or diagrams. You will have to answer the questions based on the information provided in the test. The goal is to answer all questions correctly.',
            # 'topic': 'You have to solve a science-based problem given environmental cues. You have to identify the key factors and constraints and take them into account.'
            'topic': 'Create a vacation planner'
        }
        
        clean_folders()
        
        TfgCrew().crew().kickoff(inputs=inputs)
        
        #new_crew()
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
    try:
        
        inputs = {
            #'topic': 'Create a story with a topic given that incorporates the answers to 5 trivia questions that the user will provide',
            #'topic': 'Identify the 3 words best associated with a specific word from a word list given by the user',
            # 'topic': 'Q: There are <n> houses in a row, numbered 1 on the left to <n> on the right. There is one person living in each house. The people in these houses have different characteristics: <characteristics> Clue(s): <Clues>.  <Question>?   <n choices>',
            # 'topic': 'You have to solve a test on a specific subject. The test consists of multiple-choice questions, each with a set of possible answers and a correct answer. Some questions will include images or diagrams. You will have to answer the questions based on the information provided in the test. The goal is to answer all questions correctly.',
            # 'topic': 'You have to solve a science-based problem given environmental cues. You have to identify the key factors and constraints and take them into account.'
            'topic': 'Create a vacation planner'
        }
        
        clean_folders()
        
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
    
    try:
        
        inputs = {
            #'topic': 'Create a story with a topic given that incorporates the answers to 5 trivia questions that the user will provide',
            #'topic': 'Identify the 3 words best associated with a specific word from a word list given by the user',
            # 'topic': 'Q: There are <n> houses in a row, numbered 1 on the left to <n> on the right. There is one person living in each house. The people in these houses have different characteristics: <characteristics> Clue(s): <Clues>.  <Question>?   <n choices>',
            # 'topic': 'You have to solve a test on a specific subject. The test consists of multiple-choice questions, each with a set of possible answers and a correct answer. Some questions will include images or diagrams. You will have to answer the questions based on the information provided in the test. The goal is to answer all questions correctly.',
            # 'topic': 'You have to solve a science-based problem given environmental cues. You have to identify the key factors and constraints and take them into account.'
            'topic': 'Create a vacation planner'
        }
        
        clean_folders()
        
        TfgCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

    sys.exit(0)