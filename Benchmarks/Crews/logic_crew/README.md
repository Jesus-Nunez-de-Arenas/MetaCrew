# Logic Crew

Welcome to the Logic Grid Puzzle Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Schema
```
logic_crew/ # Logic Grid Puzzle code and agent implementations
├── src/logic_crew/ # Logic Grid Puzzle code and agent implementations
│   ├── main.py
│   ├── crew.py
│   ├── config/ # Configuration files of the agents and tasks
│   └── tools/ # Tools used by the agents
├── output_logic/ # Output directoy of the Logic Grid Puzzle benchmark
├── storage/ # Memory storage
│   └── short_term/
├── logic_grid_puzzle_200.jsonl # Dataset of the Logic Grid Puzzle benchmark
├── pyproject.toml # Poetry configuration file
├── .env
└── README.md
```

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
OUTPUT_DIR='./output_codenames/'
CREWAI_STORAGE_DIR='./storage/'

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ poetry run run_crew
```

This command initializes the Logic Grid Puzzle Crew, assembling the agents and assigning them tasks guided by the manager.

## Output

The project will create a folder for each question. In each folder, we have the output of each task.

## Scoring

To calculate the score of this benchmark, we will have to go through each Identify_Valid_Solutions.txt manually. As there is not standarized output for each question, the output of the agents may differ, so we cannot rely in a script to calculate the score automatically.