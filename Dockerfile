# Python Railway Template - Selenium Grid Docker build
# Optimized for Railway deployment with Selenium Grid

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY . .

# Install the project
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim

# Copy the virtual environment
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Make sure scripts in .venv are usable
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY --from=builder --chown=app:app /app /app

# Create non-root user
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Create reports directory for outputs
RUN mkdir -p /app/reports && chown -R app:app /app/reports

# Change to non-root user
USER app

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

# Expose port (if needed for web apps)
EXPOSE 8000

# Run the application
CMD ["uv", "run", "app"]
