FROM python:3.11-slim

WORKDIR /app

COPY agents/bom-agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared
COPY agents/bom-agent /app/agent

ENV PYTHONPATH=/app

CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8004"]
