import sys
import warnings
import logging
import atexit
from writing_crew.crew import Writing_Crew
import json
import os
from writing_crew.utils.logging_utils import close_log_file, setup_logging

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not found. Please install it with: poetry add python-dotenv")

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
    output_dir = os.getenv("OUTPUT_DIR", "./output_logic/")
    os.makedirs(output_dir, exist_ok=True)
    
    questions_file = os.getenv("QUESTIONS_FILE", "trivia_creative_writing_100_n_5.jsonl")
    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"{questions_file} not found.")

    with open(questions_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                question_data = json.loads(line)
                questions = question_data.get("questions", "")
                topic = question_data.get("topic", "")
                if isinstance(questions, list):
                    questions = "; ".join(str(question) for question in questions)
                
                inputs = {
                    'topic' : topic,
                    'prompt': f'''Write a short and coherent story about {topic} that incorporates the answers to the questions''',
                    'questions': questions
                }
                try:
                    Writing_Crew(question_number=line_num).crew().kickoff(inputs=inputs)
                except Exception as e:
                    raise Exception(f"An error occurred while running the crew: {e}")
            except Exception as e:
                logging.error(f"Error processing question at line {line_num}: {e}")