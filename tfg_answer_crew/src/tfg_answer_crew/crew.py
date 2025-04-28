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
    model=os.getenv("OPENAI_EMBEDDING_MODEL_NAME", "text-embedding-ada-002"),
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

vectorstore_entity = Chroma(
    embedding_function=embedding_model,
    persist_directory=os.getenv("CREWAI_STORAGE_DIR") + "./entity/chroma_db"
)

vectorstore_short_term = Chroma(
    embedding_function=embedding_model,
    persist_directory=os.getenv("CREWAI_STORAGE_DIR") + "./short_term/chroma_db"
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
        verbose=True,
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
    def alice_harper(self) -> Agent:
        return Agent(
            role="Character Designer",
            goal="To create intricate character profiles that include backgrounds, motivations, and growth arcs.",
            backstory="Alice is a seasoned character designer who has worked on multiple best-selling novels. With a background in psychology, she deeply understands human behavior, allowing her to craft realistic and relatable characters.",
            verbose=True
        )

    @agent
    def james_bennett(self) -> Agent:
        return Agent(
            role="Character Consultant",
            goal="To ensure character consistency and depth throughout the narrative.",
            backstory="With over 15 years in the industry, James has provided support for major film and TV franchises. His expertise lies in character motivation and interpersonal dynamics.",
            verbose=True
        )

    @agent
    def sophia_cheng(self) -> Agent:
        return Agent(
            role="Plot Strategist",
            goal="To outline the main components and structure of the story, ensuring a compelling narrative flow.",
            backstory="A former screenwriter, Sophia has transitioned to plot strategy and has helped numerous authors outline their novels, ensuring key plot points resonate effectively with audiences.",
            verbose=True
        )

    @agent
    def oliver_green(self) -> Agent:
        return Agent(
            role="World Builder",
            goal="To define the environment, time period, and cultural influences that shape the narrative.",
            backstory="Oliver has a background in anthropology and has traveled extensively, gathering insights that help him create rich and immersive settings that enhance the story's context.",
            verbose=True
        )

    @agent
    def emily_sanders(self) -> Agent:
        return Agent(
            role="Theme Analyst",
            goal="To identify and articulate the central themes and messages within the story.",
            backstory="A literature professor, Emily specializes in thematic analysis and has published multiple papers on the role of themes in modern storytelling. Her insights help refine the story's core message.",
            verbose=True
        )

    @task
    def character_development(self) -> Task:
        return Task(
            config=self.tasks_config['Character_Development'],
            output_file=os.getenv("OUTPUT_DIR") + 'character_development.md'
        )

    @task
    def plot_structure(self) -> Task:
        return Task(
            config=self.tasks_config['Plot_Structure'],
            output_file=os.getenv("OUTPUT_DIR") + 'plot_structure.md'
        )

    @task
    def setting_definition(self) -> Task:
        return Task(
            config=self.tasks_config['Setting_Definition'],
            output_file=os.getenv("OUTPUT_DIR") + 'setting_definition.md'
        )

    @task
    def theme_exploration(self) -> Task:
        return Task(
            config=self.tasks_config['Theme_Exploration'],
            output_file=os.getenv("OUTPUT_DIR") + 'theme_exploration.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Tfg crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            manager_agent=create_manager_agent(),
            process=Process.hierarchical,
            verbose=True,
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path=self.db_path,
                )
            ),
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