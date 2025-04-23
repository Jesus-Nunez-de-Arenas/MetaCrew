import os
import re
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from langchain.schema import SystemMessage
from langchain.prompts import PromptTemplate
from .util_functions import extract_text_from_file
import yaml

# Tool to extract YAML from expert info
@tool
def extract_expert_yaml(text: str) -> str:
    """Extract expert details and return them in a formatted YAML string."""
    prompt = f"""
You will be given a text that contains information about one or more experts. 
Your task is to extract each expert's information (name, role, goal, backstory),
in the names, put a _ instead of a blank space, and return it in this YAML format:

<name>:
  role: >
    <role>
  goal: >
    <goal>
  backstory: >
    <backstory>

Only output the YAML. Here is the input text:
{text}
"""
    llm = ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_MODEL_NAME"))
    response = llm.invoke(prompt)
    yaml_str = re.sub(r"^```yaml|```$", "", response.content.strip(), flags=re.MULTILINE).strip()
    return yaml_str

# Tool to extract YAML from subtask info
@tool
def extract_subtask_yaml(text: str) -> str:
    """Extract expert details and return them in a formatted YAML string."""
    prompt = f"""
You will be given a text that contains information about one or more experts. 
Your task is to extract each expert's information (name, description and expected output), 
in the names, put a _ instead of a blank space, and return it in this YAML format:

<name>:
  description: >
    <description> 
  expected_output: >
    <expected_output>

Only output the YAML. Here is the input text:
{text}
"""
    llm = ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_MODEL_NAME"))
    response = llm.invoke(prompt)
    yaml_str = re.sub(r"^```yaml|```$", "", response.content.strip(), flags=re.MULTILINE).strip()
    return yaml_str

# Expert agent setup
def create_agent():
    tools = [extract_expert_yaml]
    llm = ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_MODEL_NAME"))
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent

# Expert workflow
def run_agent_on_file(file_path):
    raw_text = extract_text_from_file(file_path)
    agent = create_agent()
    yaml_output = agent.invoke(f"extract_expert_yaml: {raw_text}")
    
    return yaml_output['output']

# Subtask agent setup
def create_subtask_agent():
    tools = [extract_subtask_yaml]
    llm = ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_MODEL_NAME"))
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent

# Subtask workflow
def run_subtask_agent_on_file(file_path):
    raw_text = extract_text_from_file(file_path)
    agent = create_subtask_agent()
    yaml_output = agent.invoke(f"extract_subtask_yaml: {raw_text}")

    return yaml_output['output']