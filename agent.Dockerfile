# For more information, please refer to https://aka.ms/vscode-docker-python
FROM ghcr.io/astral-sh/uv:0.9.10-python3.14-bookworm-slim

WORKDIR /src

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Set uv environment variables for better Docker performance
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV UV_SYSTEM_PYTHON=1
ENV UV_NO_SYNC=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Install pip requirements
COPY pyproject.toml .
RUN uv pip install --system --verbose -r pyproject.toml

# Copy everything into the working directory
COPY src/ ./app/

# Expose default port (Cloud Run sets $PORT at runtime; expose for clarity)
EXPOSE 8501

# Allow Cloud Run to override the port via the PORT env var. Default to 8501 for local runs.
ENV PORT=8501

# Health check for FastAPI application - use the /health endpoint which the app exposes
HEALTHCHECK CMD curl --fail http://localhost:${PORT}/health || exit 1

# Run the application using uv run with correct module path
CMD ["uv", "run", "--no-sync", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8501"]
