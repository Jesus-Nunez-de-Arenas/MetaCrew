import os
import re
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from langchain_community.document_loaders import (
    TextLoader,
    JSONLoader,
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
    UnstructuredXMLLoader,
)
from langchain.schema import SystemMessage, Document
from langchain.prompts import PromptTemplate
from .util_functions import extract_text_from_file
import yaml


llm = ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_MODEL_NAME"))

# Tool to extract YAML from expert info
@tool
def extract_expert_yaml(text: str) -> str:
    """Extract expert details and return them in a formatted YAML string."""
    prompt = f"""
You will be given a text that contains information about one or more experts. 
Your task is to extract each expert's information (name, role, goal, backstory),
in the names, put a _ instead of a blank space, and return it in this exact(> symbol included) YAML format:

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
    response = llm.invoke(prompt)
    yaml_str = re.sub(r"^yaml|$", "", response.content.strip(), flags=re.MULTILINE).strip()
    return yaml_str

# Tool to extract YAML from subtask info
@tool
def extract_subtask_yaml(text: str) -> str:
	"""Extract expert details and return them in a formatted YAML string."""
	prompt = f"""
You will be given a text that contains information about one or more experts. 
Your task is to extract each expert's information (name, description and expected output), 
in the names, put a _ instead of a blank space, and return it in this exact (> symbol included) YAML format:

<name>:
  description: >
    <description> 
  expected_output: >
    <expected_output>

Only output the YAML. Here is the input text:
{text}
"""
	response = llm.invoke(prompt)
	yaml_str = re.sub(r"^yaml|$", "", response.content.strip(), flags=re.MULTILINE).strip()
	return yaml_str


def load_file_content(file_path: str) -> str:
	"""
 	Load the content of a file based on its extension.

	Args:
		file_path (str): path to the file

	Raises:
		ValueError: if the file type is not supported

	Returns:
		str: content of the file as a string
	"""
	ext = os.path.splitext(file_path)[1].lower()

	if ext == '.json':
		loader = JSONLoader(file_path, jq_schema='.', text_content=False)
	elif ext == '.txt':
		loader = TextLoader(file_path)
	elif ext == '.pdf':
		loader = UnstructuredPDFLoader(file_path)
	elif ext in ['.doc', '.docx']:
		loader = UnstructuredWordDocumentLoader(file_path)
	elif ext == '.md':
		loader = UnstructuredMarkdownLoader(file_path)
	elif ext == '.xml':
		loader = UnstructuredXMLLoader(file_path)
	else:
		raise ValueError(f"Unsupported file type: {ext}")

	docs = loader.load()
	return "\n\n".join(doc.page_content for doc in docs)


def run_agent_on_file(file_path) -> str:
	"""
	Run the subtask agent on a file to extract YAML information.

	Args:
		file_path (any): path to the file containing agent information

	Returns:
		str: YAML string containing the extracted subtask information.
	"""
	raw_text = load_file_content(file_path)

	# Initialize ChatOpenAI instance
	tools = [extract_expert_yaml]
	agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

	yaml_output = agent.invoke(f"extract_expert_yaml: {raw_text}")

	return yaml_output['output']

def run_subtask_agent_on_file(file_path) -> str:
	"""
	Run the subtask agent on a file to extract YAML information.

	Args:
		file_path (any): _path to the file containing subtask information_

	Returns:
		str: YAML string containing the extracted subtask information.
	"""
    
	raw_text = load_file_content(file_path)

	# Initialize ChatOpenAI instance

	tools = [extract_subtask_yaml]
	agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

	yaml_output = agent.invoke(f"extract_subtask_yaml: {raw_text}")
  
	return yaml_output['output']