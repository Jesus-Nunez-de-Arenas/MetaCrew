import sys
import os
import warnings
import logging
import atexit
import json
from tqdm import tqdm
import openai
from travel_crew.crew import TravelCrew
from travel_crew.utils.logging_utils import close_log_file, setup_logging
from datasets import load_dataset

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
    
    query_data_list = load_dataset('osunlp/TravelPlanner', 'validation')['validation']
    
    numbers = [i for i in range(1, len(query_data_list) + 1)]
    

    for number in tqdm(numbers[0:180]):
        if not os.path.exists(os.path.join(f'{os.getenv("OUTPUT_DIR", "./output_codenames/")}')):
            os.makedirs(os.path.join(f'{os.getenv("OUTPUT_DIR", "./output_codenames/")}/'))
        if not os.path.exists(os.path.join(f'{os.getenv("OUTPUT_DIR", "./output_codenames/")}/generated_plan_{number}.json')):
            result = [{}]
        else:
            result = json.load(
                open(os.path.join(f'{os.getenv("OUTPUT_DIR", "./output_codenames/")}/generated_plan_{number}.json')))
            
        query_data = query_data_list[number - 1]
        reference_information = query_data['reference_information']
        query = query_data['query']
            
        topic = f'''You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and accommodation names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with commonsense. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B).

        ***** Example *****
        Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
        Travel Plan:
        Day 1:
        Current City: from Ithaca to Charlotte
        Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
        Breakfast: Nagaland's Kitchen, Charlotte
        Attraction: The Charlotte Museum of History, Charlotte
        Lunch: Cafe Maple Street, Charlotte
        Dinner: Bombay Vada Pav, Charlotte
        Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

        Day 2:
        Current City: Charlotte
        Transportation: -
        Breakfast: Olive Tree Cafe, Charlotte
        Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
        Lunch: Birbal Ji Dhaba, Charlotte
        Dinner: Pind Balluchi, Charlotte
        Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

        Day 3:
        Current City: from Charlotte to Ithaca
        Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
        Breakfast: Subway, Charlotte
        Attraction: Books Monument, Charlotte.
        Lunch: Olive Tree Cafe, Charlotte
        Dinner: Kylin Skybar, Charlotte
        Accommodation: -

        ***** Example Ends *****

        Given information: {reference_information}
        Query: {query}
        Travel Plan:
        '''
        inputs = {
            'topic': topic,
        }
        TravelCrew(question_number=number).crew().kickoff(inputs=inputs)
        
        os.makedirs(os.getenv("OUTPUT_DIR", "./output_codenames/"), exist_ok=True)

        with open(os.path.join(f'{os.getenv("OUTPUT_DIR", "./output_codenames/")}/generated_plan_{number}.json'), 'w') as f:
            json.dump(result, f, indent=4)