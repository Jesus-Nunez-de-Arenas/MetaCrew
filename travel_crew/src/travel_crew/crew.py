from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai_tools import JSONSearchTool
import os
import sqlite3
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

embedding_model = OpenAIEmbeddings(
    model=os.getenv("OPENAI_EMBEDDING_MODEL_NAME", "text-embedding-3-small"),
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

vectorstore_short_term = Chroma(
    embedding_function=embedding_model,
    persist_directory=os.getenv("CREWAI_STORAGE_DIR") + "./short_term/chroma_db"
)


@CrewBase
class TravelCrew():
    """TfgAnswerCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, question_number):
        self.question_number = question_number

    @agent
    def Emily_Johnson(self) -> Agent:
        Emily_Johnson = Agent(
            config=self.agents_config['Emily_Johnson'],
            verbose=True,
        )
        Emily_Johnson.config = self.agents_config['Emily_Johnson']
        return Emily_Johnson

    @agent
    def James_Smith(self) -> Agent:
        James_Smith = Agent(
            config=self.agents_config['James_Smith'],
            verbose=True,
        )
        James_Smith.config = self.agents_config['James_Smith']
        return James_Smith
    
    @agent
    def Samantha_Brown(self) -> Agent:
        Samantha_Brown = Agent(
            config=self.agents_config['Samantha_Brown'],
            verbose=True,
        )
        Samantha_Brown.config = self.agents_config['Samantha_Brown']
        return Samantha_Brown
    
    @agent
    def David_Lee(self) -> Agent:
        David_Lee = Agent(
            config=self.agents_config['David_Lee'],
            verbose=True,
        )
        David_Lee.config = self.agents_config['David_Lee']
        return David_Lee
    
    @agent
    def Rachel_Green(self) -> Agent:
        Rachel_Green = Agent(
            config=self.agents_config['Rachel_Green'],
            verbose=True,
        )
        Rachel_Green.config = self.agents_config['Rachel_Green']
        return Rachel_Green

    @task
    def Research_Destinations(self) -> Task:
        Research_Destinations = Task(
            config=self.tasks_config['Research_Destinations'],
            agent=self.Emily_Johnson(),
            output_file=os.getenv("OUTPUT_DIR") + 'plan_' + str(self.question_number) + '/research_destinations.txt'
        )
        Research_Destinations.config = self.tasks_config['Research_Destinations']
        return Research_Destinations

    @task
    def Establish_Budget(self) -> Task:
        Establish_Budget = Task(
            config=self.tasks_config['Establish_Budget'],
            agent=self.James_Smith(),
            output_file=os.getenv("OUTPUT_DIR") + 'plan_' + str(self.question_number) + '/establish_budget.txt'
        )
        Establish_Budget.config = self.tasks_config['Establish_Budget']
        return Establish_Budget
    
    @task
    def Plan_Itinerary(self) -> Task:
        Plan_Itinerary = Task(
            config=self.tasks_config['Plan_Itinerary'],
            agent=self.Samantha_Brown(),
            output_file=os.getenv("OUTPUT_DIR") + 'plan_' + str(self.question_number) + '/plan_itinerary.txt'
        )
        Plan_Itinerary.config = self.tasks_config['Plan_Itinerary']
        return Plan_Itinerary
    
    @task
    def Book_Accommodations(self) -> Task:
        Book_Accommodations = Task(
            config=self.tasks_config['Book_Accommodations'],
            agent=self.David_Lee(),
            output_file=os.getenv("OUTPUT_DIR") + 'plan_' + str(self.question_number) + '/book_accommodations.txt'
        )
        Book_Accommodations.config = self.tasks_config['Book_Accommodations']
        return Book_Accommodations
    
    @task
    def Arrange_Transportation(self) -> Task:
        Arrange_Transportation = Task(
            config=self.tasks_config['Arrange_Transportation'],
            agent=self.Rachel_Green(),
            output_file=os.getenv("OUTPUT_DIR") + 'plan_' + str(self.question_number) + '/arrange_transportation.txt'
        )
        Arrange_Transportation.config = self.tasks_config['Arrange_Transportation']
        return Arrange_Transportation

    @crew
    def crew(self) -> Crew:
        """Creates the TfgAnswerCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
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
            )
        )