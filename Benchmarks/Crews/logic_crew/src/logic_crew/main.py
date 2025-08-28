import sys
import warnings
import logging
import atexit
import os

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not found. Please install it with: poetry add python-dotenv")

from logic_crew.crew import LogicCrew
from logic_crew.utils.logging_utils import close_log_file, setup_logging
import json

# Set UTF-8 encoding for Windows
if os.name == 'nt':  # Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Also set console encoding for Windows
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

log_file, log_file_path = setup_logging()

@atexit.register
def cleanup():
    close_log_file(log_file)

def run():
    """
    Run the crew.
    """
    # Ensure output directory exists
    output_dir = os.getenv("OUTPUT_DIR", "./output_logic/")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load all questions from a JSONL file (one JSON object per line)
    questions_file = os.getenv("QUESTIONS_FILE", "logic_grid_puzzle_200.jsonl")
    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"{questions_file} not found.")

    with open(questions_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                question_data = json.loads(line)
                topic = question_data.get("inputs", "")
                choices = question_data.get("multiple_choice_targets", [])
                if isinstance(choices, list):
                    choices = "\n".join(str(choice) for choice in choices)

                inputs = {
                    'topic': topic,
                    'choices': choices,
                }
                LogicCrew(question_number=line_num).crew().kickoff(inputs=inputs)
            except Exception as e:
                logging.error(f"Error processing question at line {line_num}: {e}")