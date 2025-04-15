############################################################################
# --------------------------- Crewai Imports ----------------------------- #
############################################################################

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai_tools import JSONSearchTool
import os

############################################################################
# ---------------------------- Other Imports ----------------------------- #
############################################################################

from typing import List, Optional
from pydantic import BaseModel, Field
from tfg.tools.custom_tool import CleanJSON


############################################################################
# --------------------------------- Code --------------------------------- #
############################################################################

# llm = LLM(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     model="gemini/gemini-2.0-flash",
# )



@CrewBase
class TfgCrew():
	"""Tfg crew"""

	@agent
	def master(self) -> Agent:
		return Agent(
			config=self.agents_config['master'],
			verbose=True,
		)
  
	@agent
	def hhrr(self) -> Agent:
		return Agent(
			config=self.agents_config['hhrr'],
			verbose=True,
			tools=[
				JSONSearchTool(json_path=os.getenv("OUTPUT_DIR") + 'subtasks.json')
			]
		)
  
	@agent
	def planner(self) -> Agent:
		return Agent(
			config=self.agents_config['planner'],
			verbose=True,
			tools=[
				JSONSearchTool(json_path=os.getenv("OUTPUT_DIR"))
			]
		)

	@task
	def subtasks(self) -> Task:
		return Task(
			config=self.tasks_config['subtasks'],
			output_file= os.getenv("OUTPUT_DIR") + 'subtasks.json'
		)
  
	@task
	def experts(self) -> Task:
		return Task(
			config=self.tasks_config['experts'],
			output_file= os.getenv("OUTPUT_DIR") + 'experts.json'
		)
  
	@task
	def workflow(self) -> Task:
		return Task(
			config=self.tasks_config['workflow'],
			output_file=os.getenv("OUTPUT_DIR") + 'workflow.json'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Tfg crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# memory=True,
			# long_term_memory=LongTermMemory(
			# 	storage=LTMSQLiteStorage(
			# 		db_path=os.getenv("CREWAI_STORAGE_DIR") + "long_term/"
			# 	)
			# ),
			# short_term_memory=ShortTermMemory(
			# 	storage=RAGStorage(
			# 		crew=self,
			# 		type="short_term",
			# 		path=os.getenv("CREWAI_STORAGE_DIR") + "short_term/",
			# 		embedder_config={
			# 			"provider": "openai",
			# 			"config": {
			# 				"model": 'text-embedding-3-small',
			# 				"api_key": os.getenv("OPENAI_API_KEY")
			# 			}
			# 		},
			# 	),
			# ),
			# entity_memory=EntityMemory(
			# 	storage=RAGStorage(
			# 		crew=self,
			# 		type="entities",
			# 		path=os.getenv("CREWAI_STORAGE_DIR") + "entities/",
			# 		embedder_config={
			# 			"provider": "openai",
			# 			"config": {
			# 				"model": 'text-embedding-3-small',
       		# 				"api_key": os.getenv("OPENAI_API_KEY")
			# 			}
			# 		},
			# 	),
			# )
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)