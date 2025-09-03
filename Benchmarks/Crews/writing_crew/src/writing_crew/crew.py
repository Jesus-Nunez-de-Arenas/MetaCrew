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
class Writing_Crew():
    """Writing crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, question_number):
        self.question_number = question_number

    @agent
    def Alice_Thompson(self) -> Agent:
        """Agent for Alice Thompson

        Returns:
            Agent: The agent for Alice Thompson.
        """
        Alice_Thompson = Agent(
            config=self.agents_config['Alice_Thompson'],
            verbose=True
        )
        Alice_Thompson.config = self.agents_config['Alice_Thompson']
        return Alice_Thompson

    @agent
    def Bob_Johnson(self) -> Agent:
        """Agent for Bob Johnson

        Returns:
            Agent: The agent for Bob Johnson.
        """
        Bob_Johnson = Agent(
            config=self.agents_config['Bob_Johnson'],
            verbose=True
        )
        Bob_Johnson.config = self.agents_config['Bob_Johnson']
        return Bob_Johnson
    
    @agent
    def Catherine_Lee(self) -> Agent:
        """Agent for Catherine Lee

        Returns:
            Agent: The agent for Catherine Lee.
        """
        Catherine_Lee = Agent(
            config=self.agents_config['Catherine_Lee'],
            verbose=True
        )
        Catherine_Lee.config = self.agents_config['Catherine_Lee']
        return Catherine_Lee
    
    @agent
    def David_Kim(self) -> Agent:
        """Agent for David Kim

        Returns:
            Agent: The agent for David Kim.
        """
        David_Kim = Agent(
            config=self.agents_config['David_Kim'],
            verbose=True
        )
        David_Kim.config = self.agents_config['David_Kim']
        return David_Kim

    @agent
    def Eva_Martinez(self) -> Agent:
        """Agent for Eva Martinez

        Returns:
            Agent: The agent for Eva Martinez.
        """
        Eva_Martinez = Agent(
            config=self.agents_config['Eva_Martinez'],
            verbose=True
        )
        Eva_Martinez.config = self.agents_config['Eva_Martinez']
        return Eva_Martinez

    @task
    def Define_Story_Topic(self) -> Task:
        """
        Task for defining the story topic.

        Returns:
            Task: The task for defining the story topic.
        """
        Define_Story_Topic = Task(
            config=self.tasks_config['Define_Story_Topic'],
            agent=self.Alice_Thompson(),
            output_file=os.getenv("OUTPUT_DIR") + 'story_'+ str(self.question_number) + '/Define_Story_Topic.txt'
        )
        Define_Story_Topic.config = self.tasks_config['Define_Story_Topic']
        return Define_Story_Topic

    @task
    def Collect_Trivia_Questions(self) -> Task:
        """
        Task for collecting trivia questions.

        Returns:
            Task: The task for collecting trivia questions.
        """
        Collect_Trivia_Questions = Task(
            config=self.tasks_config['Collect_Trivia_Questions'],
            agent=self.Bob_Johnson(),
            output_file=os.getenv("OUTPUT_DIR") + 'story_'+ str(self.question_number) + '/Collect_Trivia_Questions.txt'
        )
        Collect_Trivia_Questions.config = self.tasks_config['Collect_Trivia_Questions']
        return Collect_Trivia_Questions
    
    @task
    def Develop_Story_Structure(self) -> Task:
        """
        Task for developing the story structure.

        Returns:
            Task: The task for developing the story structure.
        """
        Develop_Story_Structure = Task(
            config=self.tasks_config['Develop_Story_Structure'],
            agent=self.Catherine_Lee(),
            output_file=os.getenv("OUTPUT_DIR") + 'story_'+ str(self.question_number) + '/Develop_Story_Structure.txt'
        )
        Develop_Story_Structure.config = self.tasks_config['Develop_Story_Structure']
        return Develop_Story_Structure
    
    @task
    def Draft_the_Story(self) -> Task:
        """
        Task for drafting the story.

        Returns:
            Task: The task for drafting the story.
        """
        Draft_the_Story = Task(
            config=self.tasks_config['Draft_the_Story'],
            agent=self.David_Kim(),
            output_file=os.getenv("OUTPUT_DIR") + 'story_'+ str(self.question_number) + '/Draft_the_Story.txt'
        )
        Draft_the_Story.config = self.tasks_config['Draft_the_Story']
        return Draft_the_Story
    
    @task
    def Review_and_Edit_the_Story(self) -> Task:
        """
        Task for reviewing and editing the story.

        Returns:
            Task: The task for reviewing and editing the story.
        """
        Review_and_Edit_the_Story = Task(
            config=self.tasks_config['Review_and_Edit_the_Story'],
            agent=self.Eva_Martinez(),
            output_file=os.getenv("OUTPUT_DIR") + 'story_'+ str(self.question_number) + '/Review_and_Edit_the_Story.txt'
        )
        Review_and_Edit_the_Story.config = self.tasks_config['Review_and_Edit_the_Story']
        return Review_and_Edit_the_Story

    @crew
    def crew(self) -> Crew:
        """Creates the Writing crew"""
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