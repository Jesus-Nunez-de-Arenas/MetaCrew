import sys
import os
import warnings
import logging
import atexit
import json
import openai
from codenames_crew.crew import CodenamesCrew
from codenames_crew.utils.logging_utils import close_log_file, setup_logging

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
    output_dir = os.getenv("OUTPUT_DIR", "./output_codenames/")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load all questions from a JSONL file (one JSON object per line)
    questions_file = os.getenv("QUESTIONS_FILE", "codenames_50.jsonl")
    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"{questions_file} not found.")

    with open(questions_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                question_data = json.loads(line)
                word_list = question_data.get("word_list", "")
                if isinstance(word_list, list):
                    word_list = ",".join(str(choice) for choice in word_list)
                    
                target_words = question_data["target_words"]
                n = len(target_words)
                
                prompt = f'''Try to find a single word hint that can accurately represent and link the {n} given words: "{target_words}". The key is to select a hint that does not cause confusion with other words from the following word list: {word_list}.
You need to give reasons first and then give the answer with the format: \"Final Answer: <a single word from the word list>\" 
Answer:
'''

                messages = [
                    {"role": "user", "content": prompt},
                ]
                
                openai_api_key = os.getenv("OPENAI_API_KEY")
                if not openai_api_key:
                    raise EnvironmentError("OPENAI_API_KEY not set in environment variables.")

                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=messages,
                    temperature=0.1,
                )
                answer = response.choices[0].message.content.strip()
                
                hint_word = answer.split("Final Answer:")[-1].strip()
                
                topic = prompt = f'''Try to identify the {n} words best associated with the word "{hint_word}" from the following word list: {word_list}.
You need to give reasons first and then give the answer with the format: \"Final Answer: <a comma-separated list of {n} words from the word list>\" 
Answer:
'''
                inputs = {
                    'topic': topic,
                }
                CodenamesCrew(question_number=line_num).crew().kickoff(inputs=inputs)
            except Exception as e:
                logging.error(f"Error processing question at line {line_num}: {e}")