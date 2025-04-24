import sys
import warnings
import logging
import atexit

from tfg_answer_crew.crew import TfgAnswerCrew
from tfg_answer_crew.utils.logging_utils import close_log_file, setup_logging

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Global Logging Setup
log_file, log_file_path = setup_logging()

@atexit.register
def cleanup():
    close_log_file(log_file)

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Create a story'
    }
    TfgAnswerCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "Create a story"
    }
    try:
        TfgAnswerCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TfgAnswerCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "Create a story"
    }
    try:
        TfgAnswerCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")