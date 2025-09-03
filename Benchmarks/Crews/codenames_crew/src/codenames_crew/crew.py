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
class CodenamesCrew():
    """Codenames crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, question_number):
        self.question_number = question_number

    @agent
    def Emily_Carter(self) -> Agent:
        """
        Agent for Emily Carter
        This agent is responsible for selecting the target word in the Codenames game.

        Returns:
            Agent: The agent for Emily Carter.
        """
        Emily_Carter = Agent(
            config=self.agents_config['Emily_Carter'],
            verbose=True,
        )
        Emily_Carter.config = self.agents_config['Emily_Carter']
        return Emily_Carter

    @agent
    def Michael_Bowen(self) -> Agent:
        """
        Agent for Michael Bowen
        This agent is responsible for identifying associated words in the Codenames game.

        Returns:
            Agent: The agent for Michael Bowen.
        """
        Michael_Bowen = Agent(
            config=self.agents_config['Michael_Bowen'],
            verbose=True,
        )
        Michael_Bowen.config = self.agents_config['Michael_Bowen']
        return Michael_Bowen
    
    @agent
    def Sophia_Thompson(self) -> Agent:
        """
        Agent for Sophia Thompson
        This agent is responsible for preparing the results in the Codenames game.

        Returns:
            Agent: The agent for Sophia Thompson.
        """
        Sophia_Thompson = Agent(
            config=self.agents_config['Sophia_Thompson'],
            verbose=True,
        )
        Sophia_Thompson.config = self.agents_config['Sophia_Thompson']
        return Sophia_Thompson

    @task
    def Select_Target_Word(self) -> Task:
        """
        Task for selecting the target word in the Codenames game.

        Returns:
            Task: The task for selecting the target word.
        """
        Select_Target_Word = Task(
            config=self.tasks_config['Select_Target_Word'],
            agent=self.Emily_Carter(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_'+ str(self.question_number) + '/select_target_word.txt'
        )
        Select_Target_Word.config = self.tasks_config['Select_Target_Word']
        return Select_Target_Word

    @task
    def Identify_Associated_Words(self) -> Task:
        """
        Task for identifying associated words in the Codenames game.

        Returns:
            Task: The task for identifying associated words.
        """
        Identify_Associated_Words = Task(
            config=self.tasks_config['Identify_Associated_Words'],
            agent=self.Michael_Bowen(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_'+ str(self.question_number) + '/identify_associated_words.txt'
        )
        Identify_Associated_Words.config = self.tasks_config['Identify_Associated_Words']
        return Identify_Associated_Words
    
    @task
    def Prepare_Results(self) -> Task:
        """
        Task for preparing the results in the Codenames game.

        Returns:
            Task: The task for preparing the results.
        """
        Prepare_Results = Task(
            config=self.tasks_config['Prepare_Results'],
            agent=self.Sophia_Thompson(),
            output_file=os.getenv("OUTPUT_DIR") + 'question_'+ str(self.question_number) + '/prepare_results.txt'
        )
        Prepare_Results.config = self.tasks_config['Prepare_Results']
        return Prepare_Results

    @crew
    def crew(self) -> Crew:
        """Creates the Codenames crew"""
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