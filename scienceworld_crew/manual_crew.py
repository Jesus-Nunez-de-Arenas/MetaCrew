"""
Manual Science World Crew Implementation
This bypasses CrewAI's LLM integration issues while maintaining the agent workflow structure
"""
import os
import json
import argparse
import logging
import time
import tiktoken
import ollama
from logging import INFO
from PIL import Image
from io import BytesIO
import base64
from typing import Dict, List
from tqdm import tqdm
from fastchat.conversation import Conversation, SeparatorStyle
from fastchat.model.model_adapter import get_conversation_template
from scienceworld import ScienceWorldEnv
from manual_crew_utils.eval_utils import findValidActionNew, is_action_failed, load_variation
import re
import requests

INIT_PROMPT = '''
Interact with a household to solve a task. Each turn, you can choose from one of the following options:
1. Think: You could think step-by-step to tell your reasoning and planning to solve the task, which will help you handle the task easier.
2. Action: You could interact with the environment freely to solve the task, but remember to refer to your thought and act accordingly.
Prepend your action with "Think: " or "Action: ", e.g. "Think: Now I have picked up the object. Next, I need to move to the location of the answer box." or "Action: go to kitchen".
Exactly only one option could be chosen in a turn.
'''.strip()


class ManualAgent:
    """Simple agent that calls Llama2:7b via Ollama API"""
    
    def __init__(self, name, role, goal, backstory):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory

    def execute_task(self, task_description, image_tool=None, context=""):
        """Execute a task using the Llama2:7b model via Ollama API"""
        # Compose the prompt
        full_prompt = f"""
You are {self.name}, a {self.role}.
Goal: {self.goal}
Backstory: {self.backstory}

Context: {context}

Task: {task_description}

Provide a detailed response.
"""
        try:
            # Call Ollama API for llama2:7b
            response = ollama.chat(
                model="llama2:7b",
                messages=[{"role": "user", "content": full_prompt}]
            )
            text = response['message']['content']
            return f"[{self.name}]: {text}"
        except Exception as e:
            return f"[{self.name}] Error: {e}"

class ManualMMmuCrew:
    """Manual implementation of MMMU crew that bypasses CrewAI LLM issues"""
    
    def __init__(self):
        self.setup_agents()
    
    def setup_agents(self):
        """Create the 5 agents manually"""
        self.agents = {
            'emily_carter': ManualAgent(
                name="Dr. Emily Carter",
                role="Environmental Analyst",
                goal="To pinpoint the key environmental factors affecting the problem-solving process.",
                backstory="With a background in Environmental Science and years of research experience, Dr. Carter specializes in identifying influences on ecological and societal issues, making her vital for this task."
            ),
            'mark_robinson': ManualAgent(
                name="Mark Robinson",
                role="Constraints Specialist",
                goal="To identify limitations that affect potential solutions based on the key factors observed.",
                backstory="Mark has a decade of experience in project management and risk assessment, with a focus on spotting operational constraints that could impede problem-solving endeavors."
            ),
            'sarah_lewis': ManualAgent(
                name="Sarah Lewis",
                role="Solution Strategist", 
                goal="To develop feasible solutions in light of the identified key factors and constraints.",
                backstory="A strategic planner with an MBA and significant experience in consulting, Sarah excels in crafting solutions tailored to complex situations requiring multi-faceted approaches."
            ),
            'james_pinto': ManualAgent(
                name="Dr. James Pinto",
                role="Feasibility Analyst",
                goal="To assess the practicality and potential impact of the proposed solutions.",
                backstory="Dr. Pinto's background in Environmental Policy and years of experience evaluating project outcomes make him a critical contributor to determining the feasibility of suggested strategies."
            ),
            'linda_green': ManualAgent(
                name="Linda Green",
                role="Communication Specialist",
                goal="To effectively communicate the final solution to stakeholders and facilitate understanding of the proposed strategies.",
                backstory="With extensive experience in public relations and presentation skills, Linda is adept at translating complex environmental strategies into accessible formats for diverse audiences."
            )
        }
    
    def process_sample(self, question, options, correct_answer=None):
        """Process a single Science World sample through all agents"""
        print(f"\n{'='*60}")
        print(f"PROCESSING QUESTION: {question}")
        print(f"OPTIONS: {options}")
        if correct_answer:
            print(f"CORRECT ANSWER: {correct_answer}")
        print(f"{'='*60}")
        
        results = []
        context = ""
        
        # Task 1: Emily Carter - Identify Key Environmental Factors
        task1 = f"Analyze the question: '{question}'. Options: {options}. Determine the environmental cues that are relevant to the science-based problem and how they may affect the solution."
        result1 = self.agents['emily_carter'].execute_task(task1, context=context)
        results.append(result1)
        context += f"\n\nEmily's Analysis: {result1}"
        print(f"\n{result1}")
            
        # Task 2: Mark Robinson - Assess Constraints
        task2 = f"Based on Emily's analysis, identify constraints related to the problem that could influence the problem-solving process, based on the key factors. Question: '{question}' Options: {options}"
        result2 = self.agents['mark_robinson'].execute_task(task2, context=context)
        results.append(result2)
        context += f"\n\nMark's Analysis: {result2}"
        print(f"\n{result2}")
            
        # Task 3: Sarah Lewis - Formulate Solution Strategy
        task3 = f"Develop a strategy to address the science problem by considering the key factors and constraints previously identified. Question: '{question}' Options: {options}"
        result3 = self.agents['sarah_lewis'].execute_task(task3, context=context)
        results.append(result3)
        context += f"\n\nSarah's Analysis: {result3}"
        print(f"\n{result3}")
            
        # Task 4: James Pinto - Evaluate Solution Feasibility
        task4 = f"Analyze the proposed solution to ensure it is feasible, given the constraints and environmental factors identified. Question: '{question}' Options: {options}"
        result4 = self.agents['james_pinto'].execute_task(task4, context=context)
        results.append(result4)
        context += f"\n\nJames's Analysis: {result4}"
        print(f"\n{result4}")
            
        # Task 5: Linda Green - Present Final Solution
        task5 = f"Based on all previous analyses, compile the findings and proposed solution into a coherent presentation format for review or implementation. Question: '{question}' Options: {options}. Choose the best answer and explain your reasoning."
        result5 = self.agents['linda_green'].execute_task(task5, context=context)
        results.append(result5)
        print(f"\n{result5}")

        return results

def clean(s):
    clean_toks = ['\n', '\t']
    for tok in clean_toks:
        s = s.replace(tok, ' ')
    return s


def process_examples(conv: Conversation, example: List[str]):
    for i, ex in enumerate(example):
        conv.append_message(conv.roles[i % 2], ex)
        
def get_prompt(conv: Conversation) -> str:
    if conv.name == 'openchat':
        ret = ''
        for role, message in conv.messages:
            if message:
                ret += role + ": " + message + conv.sep
            else:
                ret += role + ":"
        return ret
    else:
        # pdb.set_trace()
        ls = conv.messages
        ret = ''
        for role, message in ls:
            if message:
                ret += role + ": " + message + '\n'
            else:
                ret += role + ":"

        # pdb.set_trace()
        return ret
        return conv.get_prompt()

def llm_llama(prompt: List[Dict[str, str]], model: str) -> str:
    # Call the ManualMMmuCrew to process the prompt as a ScienceWorld crew
    # prompt: List[Dict[str, str]], model: str
    # We'll assume prompt is a list of dicts, take the last user message as question
    if isinstance(prompt, str):
        question = prompt
        options = []
    elif isinstance(prompt, list) and len(prompt) > 0:
        # Try to extract question and options from the last user message
        last_msg = prompt[-1].get("content", "")
        question = last_msg
        options = []
    else:
        question = ""
        options = []

    # Optionally, try to extract options if present in the prompt
    options_match = re.findall(r'Options: (.*)', question)
    if options_match:
        options_str = options_match[-1]
        # Try to split options by common delimiters
        if ';' in options_str:
            options = [opt.strip() for opt in options_str.split(';')]
        elif ',' in options_str:
            options = [opt.strip() for opt in options_str.split(',')]
        else:
            options = [options_str.strip()]
        # Remove options from question
        question = re.sub(r'Options: .*', '', question).strip()

    # Instantiate the crew and run the process
    crew = ManualMMmuCrew()
    results = crew.process_sample(question, options)
    # Return the final agent's output (Linda Green)
    if results:
        return results[-1]
    else:
        return "No result from crew."

# Example user input console, to play through a game.
def eval(args, task_num, logger):
    # Initialize environment
    # env = ScienceWorldEnv("", args["jar_path"], envStepLimit = args["env_step_limit"], threadNum = 0)
    env = ScienceWorldEnv("", args["jar_path"], envStepLimit=args["env_step_limit"])
    taskNames = env.getTaskNames()
    taskName = taskNames[task_num]
    # pdb.set_trace()
    env.load(taskName, 0, args['simplification_str'])
    variations = load_variation(env, args, task_num, logger)
    filenameOutPrefixSeed = get_file_name(args, task_num)

    # Load init prompt
    with open(args["prompt_file"], 'r') as f:
        d = json.load(f)

    # Load encoding tool to count token numbers
    token_model = args["model_name"] if 'gpt' in args["model_name"] else 'gpt-4'
    encoding = tiktoken.encoding_for_model('gpt-4')
    # plans = get_plans(args)

    scores = []

    for variation in variations:

        # train_data = []
        env.load(taskName, variation, args["simplification_str"], generateGoldPath=True)
        task_description = env.taskdescription()[18:]
        recent_actions = ["look around"]

        obs, info = env.reset()

        done = False
        score = 0.0
        last_score = 0.0
        step = 0

        # The env has an internal step count, some actions like look around are free
        # however, the t5 model only generates the action "look around", which will result in a dead loop below
        # so the max_steps here is only used to avoid the model generating the same action forever
        max_steps = args["env_step_limit"] * 2

        
        
        conv = get_conversation_template('llama-2')
        conv.set_system_message("You are a helpful, respectful and honest assistant.")

        conv.append_message(conv.roles[0], INIT_PROMPT)
        conv.append_message(conv.roles[1], 'Ok.')

        examples = d[str(task_num)]
        process_examples(conv, examples)

        new_task = 'The preceding task has ended. Now, I will start a new task.\n' + clean(
            obs) + '\n' + task_description
        conv.append_message(conv.roles[0], new_task.strip())

        max_len = 4096

        # Kill agent if it provides more than 10 consecutive invalid actions
        fail_counter = 0

        while not done:
            # Cut the prompt to make it shorter than maximum token numbers
            while len(encoding.encode(get_prompt(conv))) > max_len - 60:
                # Remove the oldest actions in the few-shot
                del conv.messages[4:6]
                # Remove the few-shot if it is empty
                if conv.messages[4][1].startswith('The preceding task has ended.'):
                    del conv.messages[2:4]

            # conv.append_message(conv.roles[1], None)
            # pdb.set_trace()
            prompt = get_prompt(conv)

            # pdb.set_trace()
            # logger.info(f"###Prompt###\n{prompt}")

            action = llm_llama(prompt, args["model_name"])
            logger.info('###Response###\n' + action)

            conv.update_last_message(action)

            # Don't need to actually do think actions
            if action.startswith('Think:'):
                obs = 'OK.'
            else:
                action = action.replace('Action:', '').strip()
                # Get valid actions at this point
                action = findValidActionNew([action], env, info['look'], recent_actions, None, logger)
                if isinstance(prompt, str):
                    state = [{"role": "user", "content": prompt}]
                else:
                    state = prompt
                action = llm_llama(state, args["model_name"])
                action = findValidActionNew([action], env, info['look'], recent_actions, None, logger)
                obs, reward, done, info = env.step(action)

                if is_action_failed(obs):
                    fail_counter += 1
                    if fail_counter >= 10:
                        logger.info('Early stop due to consecutive invalid actions')
                        break
                else:
                    fail_counter = 0

                score = info['score']

                if score < 0:
                    # Our own solution for dealing with such cases
                    if args["no_stop"]:
                        done = True
                        score = last_score
                    else:
                        done = True
                        score = 0
                last_score = score

            obs = clean(obs)
            print(obs)

            # Add action and observation to game prompt
            conv.append_message(conv.roles[0], obs)

            recent_actions.append(f'({action}, {obs})')

            # logger.info("Input string: " + str(input_str))
            logger.info(f"Variation: {variation}, Step: {step}, Action: {action}")
            logger.info("Obs: " + obs)
            logger.info(f"Score: {score}")
            logger.info("")

            step += 1
            if (step >= max_steps) or done:
                break

            # logger.info("Recent Actions: " + str(recent_actions))

            # Early stopping if we're in a loop
            if len(recent_actions) >= 5 and len(set(recent_actions[-5:])) == 2:
                logger.info("Many recent actions in history are the same -- model is likely in a loop, stopping early.")
                break

        # Store results
        env.storeRunHistory(variation, notes={'mode': "react_baseline", 'lm': None})
        env.saveRunHistoriesBufferIfFull(filenameOutPrefixSeed, maxPerFile=args["max_episode_per_file"])

        scores.append(score)

        logger.info("Run completed...")
        logger.info("Scores: " + str(scores))

        time.sleep(2)

    # Episodes are finished -- manually save any last histories still in the buffer
    env.saveRunHistoriesBufferIfFull(filenameOutPrefixSeed, maxPerFile=args["max_episode_per_file"], forceSave=True)

    avg = sum(scores) / len(scores)
    logger.info("Average score: " + str(avg))

    f = open(filenameOutPrefixSeed + "-score.txt", "a")
    f.write("\n" + "Task name:" + taskName + "Scores: " + str(scores) + " Average score: " + str(avg) + " Args: " + str(
        args) + "\n")
    f.close()

    logger.info("Shutting down server...")
    # env.shutdown()

    logger.info("Completed.")

def get_file_name(args, task_num):
    if (len(args["output_path"]) > 0):
        args["output_path"] = args["output_path"] + "/"

        # Make path if it doesn't exist
        if (not os.path.exists(args["output_path"])):
            try:
                os.makedirs(args["output_path"])
            except:
                pass

    # filenameOutPrefix = args["output_path"] + "transformer-" + args["mode"] + "-eval-" + str(args["lm_path"].split('/')[-1]) + "-task" + str(task_num)
    filenameOutPrefixSeed = args["output_path"] + "task" + str(task_num)

    return filenameOutPrefixSeed


def init_logger(args, task_num, log_level=INFO):
    filenameOutPrefixSeed = get_file_name(args, task_num)
    logger = logging.getLogger()
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s\t] %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logging_dir = args["output_path"]
    if logging_dir:
        os.makedirs(logging_dir, exist_ok=True)
        filename = f"{filenameOutPrefixSeed}.log"
        fh = logging.FileHandler(filename)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(fh)
    return logger

def main():
    """Main function to run the manual Science World crew"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar_path", type=str, default="")
    parser.add_argument("--env_step_limit", type=int, default=100)
    parser.add_argument("--simplification_str", default="easy")
    parser.add_argument("--max_episode_per_file", type=int, default=9999)
    parser.add_argument("--set", default="test")
    parser.add_argument("--output_path", default="logs/llama2")
    parser.add_argument("--no_stop", action="store_true", default=True)
    parser.add_argument("--prompt_file", default="manual_crew_utils/prompt.json")
    parser.add_argument("--task_nums", default="0")
    parser.add_argument("--model_name", default="llama2:7b")


    args = parser.parse_args()
    args = vars(args)

    task_nums = args["task_nums"].split(",")
    for task_num in task_nums:
        logger = init_logger(args, task_num)
        logger.info(args)
        eval(args, int(task_num), logger)


if __name__ == "__main__":
    main()
