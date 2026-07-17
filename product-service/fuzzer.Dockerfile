# Use a modern Python base image
FROM python:3.12-slim

# Set environment variables for Python and Poetry 2.x
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.2.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=/app

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies (and clean up to keep image slim)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install the exact version of Poetry using the official layout
RUN python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install --upgrade pip setuptools && \
    $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION

# Set work directory
WORKDIR /app

# Copy dependency definition files
COPY poetry.lock pyproject.toml /app/

# Poetry 2.x Syntax: Install only the main dependencies, skipping dev groups
RUN poetry install --only main --no-root

# Copy your application code
COPY . /app/

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["poetry", "run", "python3", "scripts/fuzzer.py"]
