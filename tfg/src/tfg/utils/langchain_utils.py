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
from .langchain_promts import main_prompt_template_single, crew_prompt_template_single
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

Only output the YAML on natural language. Here is the input text:
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

Only output the YAML on natural language. Here is the input text:
{text}
"""
	response = llm.invoke(prompt)
	yaml_str = re.sub(r"^yaml|$", "", response.content.strip(), flags=re.MULTILINE).strip()
	return yaml_str


# @tool
# def update_python_code(base_code: str, context_info: str) -> str:
#     """Returns modified Python code based on context information."""
#     prompt = f"""You're an AI code editor. Given the original Python code and new context, adapt the code accordingly.

#     Context Info:
#     {context_info}

#     Original Code:
#     {base_code}

#     Updated Python Code:"""
    
#     return llm.invoke(prompt)

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
	elif ext == '.py':
		loader = TextLoader(file_path)
	elif ext == '.yaml' or ext == '.yml':
		with open(file_path, 'r') as file:
			return yaml.safe_load(file)
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

def modify_single_main_python_code(file_path_python: str, file_path_context: str) -> str:
	"""
	Modify Python code based on context information.

	Args:
		file_path_python (str): path to the Python file
		file_path_context (str): path to the context file

	Returns:
		str: modified Python code as a string
	"""
 
	base_code = load_file_content(file_path_python)
	context_info = load_file_content(file_path_context)
	main_example = load_file_content(os.path.abspath(os.path.join("./src/tfg/", "main.py")))
 
	tools = []
 
	agent = initialize_agent(
		tools, llm, agent="structured-chat-zero-shot-react-description", verbose=True
	)
 
	inputs = os.getenv("INPUTS")
 
	log_utils_path = os.path.abspath(os.path.join(__file__, "../../../../../" +
		os.getenv("CREW_NAME") + "/src/" + 
		os.getenv("CREW_NAME") + "/utils/logging_utils.py"))

	main_prompt = main_prompt_template_single.format(
		file_path_context=file_path_context,
		file_path_python=file_path_python,
		inputs=inputs,
		logging_utils=log_utils_path,
		base_code=base_code,
		context_info=context_info, 
		main_example=main_example
	)

	modified_code = agent.run(main_prompt)
	# modified_code = agent.invoke(f"update_python_code: {base_code} {context_info}")
	

	print(f"Modified main code: {modified_code}")

	return modified_code

def modify_single_crew_python_code(file_path_python: str, file_path_context_task: str, file_path_context_agents: str) -> str:
	"""
	Modify Python code based on context information.

	Args:
		file_path_python (str): path to the Python file
		file_path_context (str): path to the context file

	Returns:
		str: modified Python code as a string
	"""
	base_code = load_file_content(file_path_python)
	tasks_context_info = load_file_content(file_path_context_task)
	agents_context_info = load_file_content(file_path_context_agents)
	crew_example = load_file_content(os.path.abspath(os.path.join("./src/tfg/", "crew.py")))
 
	tools = []
 
	agent = initialize_agent(
		tools, llm, agent="structured-chat-zero-shot-react-description", verbose=True
	)
 
	crew_prompt_template = crew_prompt_template_single.format(
		file_path_context_task=file_path_context_task,
  		file_path_context_agents=file_path_context_agents,
		file_path_python=file_path_python,
		inputs=os.getenv("INPUTS"),
		base_code=base_code,
		tasks_context_info=tasks_context_info, 
		agents_context_info=agents_context_info,
		crew_example=crew_example
	)

	modified_code = agent.run(crew_prompt_template)
	# modified_code = agent.invoke(f"update_python_code: {base_code} {context_info}")
	
	print(f"Modified crew code: {modified_code}")
 
	return modified_code