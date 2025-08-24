############################################################################
# --------------------------- Crewai Imports ----------------------------- #
############################################################################

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai_tools import JSONSearchTool
import os

############################################################################
# ---------------------------- Other Imports ----------------------------- #
############################################################################

import sqlite3
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

############################################################################
# --------------------------------- Code --------------------------------- #
############################################################################


embedding_model = OpenAIEmbeddings(
    model=os.getenv("OPENAI_EMBEDDING_MODEL_NAME", "text-embedding-3-small"),
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

vectorstore_entity = Chroma(
    embedding_function=embedding_model,
    persist_directory= os.getenv("CREWAI_STORAGE_DIR") + "./entity/chroma_db"
)

vectorstore_short_term = Chroma(
	embedding_function=embedding_model,
	persist_directory= os.getenv("CREWAI_STORAGE_DIR") + "./short_term/chroma_db"
)

def create_manager_agent() -> Agent:
		"""
		Creates the manager agent.
		This agent is responsible for managing the crew.

		Returns:
			Agent: The manager agent.
		"""
		return Agent(
			role="Project Manager",
			goal="Efficiently manage the crew and ensure high-quality task completion.",
			backstory="""You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. 
			Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time 
			and to the highest standard.""",
			verbose=False,
			allow_delegation=True,
		)

@CrewBase
class TfgCrew():
	"""Tfg crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
 
	# Ensure the database directory exists
	db_dir = os.path.join(os.getenv("CREWAI_STORAGE_DIR", "./storage/"), "long_term")
	os.makedirs(db_dir, exist_ok=True)

	# Ensure the database file exists
	db_path = os.path.join(db_dir, "long_term_memory.db")
	if not os.path.exists(db_path):
		# Create an empty SQLite database
		with sqlite3.connect(db_path) as conn:
			pass  # The database file will be created if it doesn't exist


	@agent
	def scrum_master(self) -> Agent:
		"""
		Creates the scrum master agent.
		This agent is responsible for managing the tasks of the crew.

		Returns:
			Agent: The scrum master agent.
		"""
     
		scrum_master = Agent(
			config=self.agents_config['scrum_master'],
			verbose=False,
			tools=[
				JSONSearchTool(json_path=os.getenv("OUTPUT_DIR"))
			]
		)
  
		scrum_master.config = self.agents_config['scrum_master']
  
		return scrum_master
  
	@agent
	def human_resources(self) -> Agent:
		"""
		Creates the human resources agent.
		This agent is responsible for managing the human resources of the crew.

		Returns:
			Agent: The human resources agent.
		"""
  
		human_resources = Agent(
			config=self.agents_config['human_resources'],
			verbose=False,
			tools=[
				JSONSearchTool(json_path=os.getenv("OUTPUT_DIR"))
			]
		)
  
		human_resources.config = self.agents_config['human_resources']

		return human_resources
  
	@agent
	def planner(self) -> Agent:
		"""
		Creates the workflow planner agent.
		This agent is responsible for planning the workflow of the crew.
  
		Returns:
			Agent: The workflow planner agent.
		"""
  
		workflow_planner = Agent(
			config=self.agents_config['planner'],
			verbose=False,
			tools=[
				JSONSearchTool(json_path=os.getenv("OUTPUT_DIR"))
			]
		)
  
		workflow_planner.config = self.agents_config['planner']
  
		return workflow_planner

	@task
	def subtasks(self) -> Task:
		"""
		Creates the subtasks task.
		This task is responsible for creating the subtasks of the crew.
  
		Returns:
			Task: The subtasks division task.
		"""
  
		subtasks = Task(
			config=self.tasks_config['subtasks'],
			output_file= os.getenv("OUTPUT_DIR") + 'subtasks.json'
		)
  
		subtasks.config = self.tasks_config['subtasks']
  
		return subtasks

	@task
	def experts(self) -> Task:
		"""
		Creates the experts task.
		This task is responsible for creating the experts of the crew.
  
		Returns:
			Task: The experts recruitment task.
		"""

		experts = Task(
			config=self.tasks_config['experts'],
			output_file= os.getenv("OUTPUT_DIR") + 'experts.json'
		)
  
		experts.config = self.tasks_config['experts']
  
		return experts
  
	@task
	def workflow(self) -> Task:
		"""
		Creates the workflow task.
		This task is responsible for creating the workflow of the crew.
  
		Returns:
			Task: The workflow management task.
		"""
		workflow = Task(
			config=self.tasks_config['workflow'],
			output_file=os.getenv("OUTPUT_DIR") + 'workflow.json'
		)
  
		workflow.config = self.tasks_config['workflow']
  
		return workflow
  
	@crew
	def crew(self) -> Crew:
		"""Creates the Tfg crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
   			manager_agent=create_manager_agent(),
			process=Process.hierarchical,
			verbose=False,
			# verbose=True, # Uncomment for debugging
			# long_term_memory=LongTermMemory(
			# 	storage=LTMSQLiteStorage(
			# 		db_path=self.db_path,
			# 	)
			# ),
			short_term_memory=ShortTermMemory(
				storage=vectorstore_short_term,
				crew=self,
				embedder_config={
						"provider": "openai",
						"config": {
							"model": os.getenv("OPENAI_EMBEDDING_MODEL_NAME"),
       						"api_key": os.getenv("OPENAI_API_KEY")
						}
					},
			),
			entity_memory=EntityMemory(
				storage=vectorstore_entity,
				crew=self,
				embedder_config={
						"provider": "openai",
						"config": {
							"model": os.getenv("OPENAI_EMBEDDING_MODEL_NAME"),
       						"api_key": os.getenv("OPENAI_API_KEY")
						}
					},
			)
		)