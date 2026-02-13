FROM python:3.12-slim

WORKDIR /app

# Install curl for Ollama install + wait, then install Ollama
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates zstd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* \
    && curl -fsSL https://ollama.com/install.sh | sh

# Pre-pull Ollama model at build time (set OLLAMA_MODEL when building to change)
ARG OLLAMA_MODEL_1=llama3.1:8b-instruct-q8_0 # Keep this
ARG OLLAMA_MODEL_2=llama3-groq-tool-use # comment any of this if not used
ARG OLLAMA_MODEL_3=mistral:7b # comment any of this if not used
RUN (ollama serve &) \
    && until curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; do sleep 2; done \
    && ollama pull ${OLLAMA_MODEL_1}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY .env .
COPY chroma_db/ ./chroma_db/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8888

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888"]
