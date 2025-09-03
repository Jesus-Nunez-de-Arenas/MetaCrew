from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai_tools import JSONSearchTool, TXTSearchTool
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
class LogicCrew():
    """LogicCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, question_number):
        self.question_number = question_number

    @agent
    def Clara_Watson(self) -> Agent:
        """Clara Watson agent

        Returns:
            Agent: Clara Watson agent instance
        """
        
        Clara_Watson = Agent(
            config=self.agents_config['Clara_Watson'],
            verbose=False,
        )
        Clara_Watson.config = self.agents_config['Clara_Watson']
        return Clara_Watson

    @agent
    def Oliver_Smith(self) -> Agent:
        """Oliver Smith agent

        Returns:
            Agent: Oliver Smith agent instance
        """
        
        Oliver_Smith = Agent(
            config=self.agents_config['Oliver_Smith'],
            verbose=False,
        )
        Oliver_Smith.config = self.agents_config['Oliver_Smith']
        return Oliver_Smith
    
    @agent
    def Emily_Davis(self) -> Agent:
        """Emily Davis agent

        Returns:
            Agent: Emily Davis agent instance
        """
        Emily_Davis = Agent(
            config=self.agents_config['Emily_Davis'],
            verbose=False,
        )
        Emily_Davis.config = self.agents_config['Emily_Davis']
        return Emily_Davis
    
    @agent
    def Michael_Brown(self) -> Agent:
        """Michael Brown agent

        Returns:
            Agent: Michael Brown agent instance
        """
        Michael_Brown = Agent(
            config=self.agents_config['Michael_Brown'],
            verbose=False,
        )
        Michael_Brown.config = self.agents_config['Michael_Brown']
        return Michael_Brown
    
    @agent
    def Sophia_Green(self) -> Agent:
        """Sophia Green agent

        Returns:
            Agent: Sophia Green agent instance
        """
        Sophia_Green = Agent(
            config=self.agents_config['Sophia_Green'],
            verbose=False,
        )
        Sophia_Green.config = self.agents_config['Sophia_Green']
        return Sophia_Green

    @task
    def Define_Variables(self) -> Task:
        """Define Variables task

        Returns:
            Task: Define Variables task instance
        """
        Define_Variables = Task(
            config=self.tasks_config['Define_Variables'],
            agent=self.Oliver_Smith(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Analyze_Define_VariablesClues.txt'
        )
        Define_Variables.config = self.tasks_config['Define_Variables']
        return Define_Variables

    @task
    def Analyze_Clues(self) -> Task:
        """Analyze Clues task

        Returns:
            Task: Analyze Clues task instance
        """
        Analyze_Clues = Task(
            config=self.tasks_config['Analyze_Clues'],
            agent=self.Clara_Watson(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Identify_Entities.txt'
        )
        Analyze_Clues.config = self.tasks_config['Analyze_Clues']
        return Analyze_Clues
    
    @task
    def Formulate_Relationships(self) -> Task:
        """Formulate Relationships task

        Returns:
            Task: Formulate Relationships task instance
        """
        Formulate_Relationships = Task(
            config=self.tasks_config['Formulate_Relationships'],
            agent=self.Emily_Davis(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Formulate_Relationships.txt'
        )
        Formulate_Relationships.config = self.tasks_config['Formulate_Relationships']
        return Formulate_Relationships

    @task
    def Generate_Possible_Arrangements(self) -> Task:
        """Generate Possible Arrangements task

        Returns:
            Task: Generate Possible Arrangements task instance
        """
        Generate_Possible_Arrangements = Task(
            config=self.tasks_config['Generate_Possible_Arrangements'],
            agent=self.Michael_Brown(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Generate_Possible_Arrangements.txt'
        )
        Generate_Possible_Arrangements.config = self.tasks_config['Generate_Possible_Arrangements']
        return Generate_Possible_Arrangements

    @task
    def Identify_Valid_Solutions(self) -> Task:
        """Identify Valid Solutions task

        Returns:
            Task: Identify Valid Solutions task instance
        """
        Identify_Valid_Solutions = Task(
            config=self.tasks_config['Identify_Valid_Solutions'],
            agent=self.Sophia_Green(), 
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Identify_Valid_Solutions.txt'
        )
        Identify_Valid_Solutions.config = self.tasks_config['Identify_Valid_Solutions']
        return Identify_Valid_Solutions

    @crew
    def crew(self) -> Crew:
        """Creates the Logic Crew"""
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