FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data
COPY eval ./eval
COPY mcp_server ./mcp_server
COPY POLICY.md .
COPY LEARNING_LOG.md .
COPY README.md .

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]