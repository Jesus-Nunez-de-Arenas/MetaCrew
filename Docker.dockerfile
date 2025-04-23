# Use an official Python image as the base
FROM python:3.10-slim@sha256:3a1b3f4c1e8b1a2e5b5c5b6b7c8d9e0f1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1 \
    CREWAI_STORAGE_DIR=/app/storage \
    OUTPUT_DIR=/app/output \
    CREW_NAME=tfg_answer_crew

# Set the working directory
WORKDIR /app

# Copy only the necessary files
COPY tfg/pyproject.toml tfg/poetry.lock ./

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Install project dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the project files
COPY tfg/ ./tfg/

# Set the default command to run the project
CMD ["poetry", "run", "crewai", "run"]