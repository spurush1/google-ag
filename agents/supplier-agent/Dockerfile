FROM python:3.11-slim

WORKDIR /app

# Copy shared requirements if any (none for now, but good practice)
# COPY shared/requirements.txt shared/requirements.txt

# Copy agent requirements
COPY agents/supplier-agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code
COPY shared /app/shared

# Copy agent code
COPY agents/supplier-agent /app/agent

# Set python path to include app
ENV PYTHONPATH=/app

CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8001"]
