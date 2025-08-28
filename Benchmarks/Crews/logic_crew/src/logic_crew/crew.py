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
        # tools = []
        # output_dir = os.getenv("OUTPUT_DIR")
        # if output_dir and os.path.exists(output_dir):
        #     tools.append(TXTSearchTool(txt=os.getenv("OUTPUT_DIR") + 'Analyze_Define_VariablesClues.txt'))
        
        Clara_Watson = Agent(
            config=self.agents_config['Clara_Watson'],
            verbose=False,
            # tools=tools
        )
        Clara_Watson.config = self.agents_config['Clara_Watson']
        return Clara_Watson

    @agent
    def Oliver_Smith(self) -> Agent:
        # tools = []
        
        Oliver_Smith = Agent(
            config=self.agents_config['Oliver_Smith'],
            verbose=False,
            # tools=tools
        )
        Oliver_Smith.config = self.agents_config['Oliver_Smith']
        return Oliver_Smith
    
    @agent
    def Emily_Davis(self) -> Agent:
        # tools = []
        # output_dir = os.getenv("OUTPUT_DIR")
        # if output_dir and os.path.exists(output_dir):
        #     tools.append(TXTSearchTool(txt=os.getenv("OUTPUT_DIR") + 'Identify_Entities.txt'))
        
        Emily_Davis = Agent(
            config=self.agents_config['Emily_Davis'],
            verbose=False,
            # tools=tools
        )
        Emily_Davis.config = self.agents_config['Emily_Davis']
        return Emily_Davis
    
    @agent
    def Michael_Brown(self) -> Agent:
        # tools = []
        # output_dir = os.getenv("OUTPUT_DIR")
        # if output_dir and os.path.exists(output_dir):
        #     tools.append(TXTSearchTool(txt=os.getenv("OUTPUT_DIR") + 'Formulate_Relationships.txt'))
        
        Michael_Brown = Agent(
            config=self.agents_config['Michael_Brown'],
            verbose=False,
            # tools=tools
        )
        Michael_Brown.config = self.agents_config['Michael_Brown']
        return Michael_Brown
    
    @agent
    def Sophia_Green(self) -> Agent:
        Sophia_Green = Agent(
            config=self.agents_config['Sophia_Green'],
            verbose=False,
            # tools=tools
        )
        Sophia_Green.config = self.agents_config['Sophia_Green']
        return Sophia_Green

    @task
    def Define_Variables(self) -> Task:
        Define_Variables = Task(
            config=self.tasks_config['Define_Variables'],
            agent=self.Oliver_Smith(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Analyze_Define_VariablesClues.txt'
        )
        Define_Variables.config = self.tasks_config['Define_Variables']
        return Define_Variables

    @task
    def Analyze_Clues(self) -> Task:
        Analyze_Clues = Task(
            config=self.tasks_config['Analyze_Clues'],
            agent=self.Clara_Watson(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Identify_Entities.txt'
        )
        Analyze_Clues.config = self.tasks_config['Analyze_Clues']
        return Analyze_Clues
    
    @task
    def Formulate_Relationships(self) -> Task:
        Formulate_Relationships = Task(
            config=self.tasks_config['Formulate_Relationships'],
            agent=self.Emily_Davis(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Formulate_Relationships.txt'
        )
        Formulate_Relationships.config = self.tasks_config['Formulate_Relationships']
        return Formulate_Relationships

    @task
    def Generate_Possible_Arrangements(self) -> Task:
        Generate_Possible_Arrangements = Task(
            config=self.tasks_config['Generate_Possible_Arrangements'],
            agent=self.Michael_Brown(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Generate_Possible_Arrangements.txt'
        )
        Generate_Possible_Arrangements.config = self.tasks_config['Generate_Possible_Arrangements']
        return Generate_Possible_Arrangements

    @task
    def Identify_Valid_Solutions(self) -> Task:
        Identify_Valid_Solutions = Task(
            config=self.tasks_config['Identify_Valid_Solutions'],
            agent=self.Sophia_Green(), 
            output_file=os.getenv("OUTPUT_DIR") + 'question_' + str(self.question_number) + '/' + 'Identify_Valid_Solutions.txt'
        )
        Identify_Valid_Solutions.config = self.tasks_config['Identify_Valid_Solutions']
        return Identify_Valid_Solutions

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