# MMMU Crew

Welcome to the MMMU Crew project. This template is designed to help you set up a multi-agent AI system with ease emulating the CrewAI framework for the use of crews with Ollama based models.

## Schema
mmmu_crew/ # MMMU code and agent implementations
├── MMMU/ # MMMU Dataset
├── output_mmmu/ # Output directoy of the MMMU benchmark
├── storage/ # Memory storage
│   └── short_term/
├── benchmark_monitor.py # Benchmark monitor progress
├── compare_answers.py # Sum up the results to make it more readable
├── custom_tool.py # Tool created to read images
├── manual_crew.py # Implentation of the crew of agents
├── merged_answers.jsonl # Result of compare_answers.py
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
OUTPUT_DIR='./output_mmmu/'
CREWAI_STORAGE_DIR='./storage/'

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ poetry python manual_crew.py
```

This command initializes the MMMU Crew, assembling the agents and assigning them tasks guided by the manager.

## Output

The project will create a .jsonl for each topic. In each .jsonl, we have the different questions with the answer for each question given by the group of agents and correct answer.

## Scoring

To calculate the score of this benchmark, we will have to go through each .jsonl manually. As there is not standarized output for each question, the output of the agents may differ, so we cannot rely in a script to calculate the score automatically. In order to facilitate the scoring, we created the compare_answers.py that returns the name of the topic with the question number, the options, the correct options and the answer of the agent that responds to the question.

```bash
$ python compare_answers.py
```