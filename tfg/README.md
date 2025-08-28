# Tfg Crew

Welcome to the Tfg Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Schema
tfg/ # MetaCrew code and agent implementations
├── src/tfg/ # MetaCrew code and agent implementations
│   ├── main.py
│   ├── crew.py
│   ├── config/ # Configuration files of the agents and tasks
│   ├── tools/ # Tools used by the agents
│   └── utils/ # Utils functions for future refinement
│       ├── langchain_prompts.py # Unimplemented
│       ├── langchain_utils.py # Unimplemented
│       ├── logging_utils.py # Implemented for logging
│       ├── utils_functions.py # Unimplemented
│       └── utils.py # Unimplemented
├── output/ # Output directoy of MetaCrew
├── storage/ # Memory storage
│   ├── entity/
│   ├── short_term/
│   └── long_term/
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

**Add your `CREW_NAME` into the `.env` file**

**Add your `INSIDE_PATH` into the `.env` file**

**Add your `OUTPUT_PATH` into the `.env` file**

**Add your `OPENAI_MODEL_NAME` into the `.env` file**

**Add your `OPENAI_EMBEDDING_MODEL_NAME` into the `.env` file**

**Add your `CREWAI_STORAGE_DIR` into the `.env` file**

**Add your `OUTPUT_DIR` into the `.env` file**

**Add your `CREWAI_TELEMETRY_OPT_OUT` into the `.env` file**

The .env used to run this project has the next values.

OPENAI_MODEL_NAME='gpt-4o-mini'
OPENAI_EMBEDDING_MODEL_NAME='text-embedding-3-small'
CREWAI_STORAGE_DIR='./storage/'
OUTPUT_DIR='./output/'
CREW_NAME='logic_crew'
INSIDE_PATH='../../../../'
OUTPUT_PATH='../../../../../'
CREWAI_TELEMETRY_OPT_OUT='true'

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ poetry run run_crew
```

This command initializes the TFG Crew, assembling the agents and assigning them tasks guided by the manager.

## Output

The project will create .json with the output of each task. The outputs will decide the agents and tasks that will be used for each benchmark.