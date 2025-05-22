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
class TfgAnswerCrew():
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
    def Emily_Johnson(self) -> Agent:
        """
        Creates the scrum master agent.
        This agent is responsible for managing the tasks of the crew.

        Returns:
            Agent: The scrum master agent.
        """
        Emily_Johnson = Agent(
            config=self.agents_config['Emily_Johnson'],
            verbose=True,
            tools=[
                JSONSearchTool(json_path=os.getenv("OUTPUT_DIR"))
            ]
        )
        Emily_Johnson.config = self.agents_config['Emily_Johnson']
        return Emily_Johnson
    
    @agent
    def David_Smith(self) -> Agent:
        """
        Creates the developer agent.
        This agent is responsible for developing the tasks of the crew.

        Returns:
            Agent: The developer agent.
        """
        David_Smith = Agent(
            config=self.agents_config['David_Smith'],
            verbose=True,
            tools=[
                JSONSearchTool(json_path=os.getenv("OUTPUT_DIR"))
            ]
        )
        David_Smith.config = self.agents_config['David_Smith']
        return David_Smith
    
    @agent
    def Sarah_Lee(self) -> Agent:
        """
        Creates the tester agent.
        This agent is responsible for testing the tasks of the crew.
        Returns:
            Agent: The tester agent.
        """
        Sarah_Lee = Agent(
            config=self.agents_config['Sarah_Lee'],
            verbose=True
        )
        Sarah_Lee.config = self.agents_config['Sarah_Lee']
        return Sarah_Lee
    
    @agent
    def Michael_Brown(self) -> Agent:
        """
        Creates the designer agent.
        This agent is responsible for designing the tasks of the crew.
        Returns:
            Agent: The designer agent.
        """
        Michael_Brown = Agent(
            config=self.agents_config['Michael_Brown'],
            verbose=True
        )
        Michael_Brown.config = self.agents_config['Michael_Brown']
        return Michael_Brown
    
    @agent
    def Jessica_White(self) -> Agent:
        """
        Creates the project manager
        This agent is responsible for managing the tasks of the crew.
        Returns:
            Agent: The project manager agent.
        """
        Jessica_White = Agent(
            config=self.agents_config['Jessica_White'],
            verbose=True
        )
        Jessica_White.config = self.agents_config['Jessica_White']
        return Jessica_White
  
    @task
    def Define_Variables(self) -> Task:
        """
        Creates the workflow task.
        This task is responsible for creating the workflow of the crew.
  
        Returns:
            Task: The workflow management task.
        """
        define_variables = Task(
            config=self.tasks_config['Define_Variables'],
            output_file=os.getenv("OUTPUT_DIR") + 'define_variables.md'
        )
        define_variables.config = self.tasks_config['Define_Variables']
        return define_variables
    
    @task
    def Set_Up_Equations(self) -> Task:
        """
        Creates the workflow task.
        This task is responsible for creating the workflow of the crew.
  
        Returns:
            Task: The workflow management task.
        """
        set_up_equations = Task(
            config=self.tasks_config['Set_Up_Equations'],
            output_file=os.getenv("OUTPUT_DIR") + 'set_up_equations.md'
        )
        set_up_equations.config = self.tasks_config['Set_Up_Equations']
        return set_up_equations
    
    @task
    def Substitute_and_Rearrange(self) -> Task:
        """
        Creates the workflow task.
        This task is responsible for creating the workflow of the crew.
        Returns:
            Task: The workflow management task.
        """
        substitute_and_rearrange = Task(
            config=self.tasks_config['Substitute_and_Rearrange'],
            output_file=os.getenv("OUTPUT_DIR") + 'substitute_and_rearrange.md'
        )
        substitute_and_rearrange.config = self.tasks_config['Substitute_and_Rearrange']
        return substitute_and_rearrange
    
    @task
    def Solve_for_C(self) -> Task:
        """
        Creates the workflow task.
        This task is responsible for creating the workflow of the crew.
        Returns:
            Task: The workflow management task.
        """
        solve_for_c = Task(
            config=self.tasks_config['Solve_for_C'],
            output_file=os.getenv("OUTPUT_DIR") + 'solve_for_c.md'
        )
        solve_for_c.config = self.tasks_config['Solve_for_C']
        return solve_for_c
    
    @task
    def Confirm_Results(self) -> Task:
        """
        Creates the workflow task.
        This task is responsible for creating the workflow of the crew.
        Returns:
            Task: The workflow management task.
        """
        confirm_results = Task(
            config=self.tasks_config['Confirm_Result'],
            output_file=os.getenv("OUTPUT_DIR") + 'confirm_results.md'
        )
        confirm_results.config = self.tasks_config['Confirm_Result']
        return confirm_results
  
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