# World of Science Crew

Welcome to the World of Science Crew project. This template is designed to help you set up a multi-agent AI system with ease emulating the CrewAI framework for the use of crews with Ollama based models.

## Schema
scienceworld_crew/ # World of Science code and agent implementations
├── manual_crew_utils/ # Utils from EvoAgent to execute the benchmark
├── logs/ # Output directoy of the World of Science benchmark
├── storage/ # Memory storage
│   └── short_term/
├── benchmark_monitor.py # Benchmark monitor progress
├── manual_crew.py # Implentation of the crew of agents
├── run_batch.py # Run all the tasks in the benchmark
├── pyproject.toml # Poetry configuration file
├── .env
└── README.md


## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and install them by using the Poetry command:
```bash
poetry install
```
2. Customize the environment

**Add your `OPENAI_API_KEY` into the `.env` file**

**Add your `OPENAI_MODEL_NAME` into the `.env` file**

**Add your `OPENAI_EMBEDDING_MODEL_NAME` into the `.env` file**

**Add your `OUTPUT_DIR` into the `.env` file**

**Add your `CREWAI_STORAGE_DIR` into the `.env` file**


The .env used to run this project has the next values.

OPENAI_MODEL_NAME='gpt-4o-mini'
OPENAI_EMBEDDING_MODEL_NAME='text-embedding-3-small'
OUTPUT_DIR='./output_scienceworld/'
CREWAI_STORAGE_DIR='./storage/'

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ poetry python manual_crew.py
```

This command initializes the World of Science Crew, assembling the agents and assigning them tasks guided by the manager.

## Output

The project will create a .log file, a .json file and a .txt fileder for each task done. In the .log file, we will find all of the sequence of execution of the task, in the .json file we have the different tasks that envolves a task and finally, in the .txt file we find the score for each task and their average that is considered for the job.

## Scoring

In a log folder each task will dump a .log file, a .json file and a .txt file. In the .txt file we have the score of the benchmark for that task.