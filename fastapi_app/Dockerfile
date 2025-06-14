FROM python:3.13.3-slim-bookworm

# Install required system dependencies
RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Astral UV
RUN pip install uv
 
# Set workdir
WORKDIR /app


COPY . .

# Install python dependencies
RUN uv pip install --system --requirements pyproject.toml

# Expose port (use the same as in your Nginx config)
EXPOSE 17560

# Run the app with Astral UV
CMD ["python", "-m", "app"]
