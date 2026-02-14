# Adatacom Autonomous Regulatory Auditor Agent

![Mainpage](docs/input.png)
![ChainofThought](docs/cot.png)

## Set up

`.env`

```bash
LLAMA_PARSE_API_KEY=llx-xxx
GROQ_API_KEY=gsk_xxx
OPENAI_API_KEY=sk-proj-xxx
```

From the project root, install dependencies and run the UI:

```bash
pip install -r requirements.txt
```

To run local model, install them:

```bash
ollama run llama3.1:8b-instruct-q8_0 # must install
ollama run llama3-groq-tool-use # optional
ollama run mistral:7b # optional
```

## Prepare knowledge base

The Knowledge base is prepared for LLM model `llama3.1:8b-instruct-q8_0` and Embedding Model `BAAI/bge-small-en-v1.5` (free from HuggingFace)

Therefore, the search tool in `regulatory_server.py` is always used with LLM model `llama3.1:8b-instruct-q8_0`. (More adjustment will be done in the future)

The file `stcced2022.pdf` is already parsed using LlamaParse and stored as `docs.md`

To build the index (takes 32 seconds):

```bash
python app/index_server.py
```

If there is a need to parse the data again, run this. This script already included index building step. This may take up to 40 minutes.

```bash
python app/index_server_improved.py
```

## Run on local machine

Run the FastAPI server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

1. NiceGUI
   Open [http://localhost:8000/ui](http://localhost:8000/ui) in your browser. The UI has a left sidebar with conversation list, a main area for input (or process/conversation view), and a plus button (top right) to start a new prompt.

2. Run agent alone and view CoT in NiceGUI

```bash
curl --location 'http://localhost:8000/agent' \
--header 'Content-Type: application/json' \
--data '{
    "user_input": "What is the HS-Code of Personal Deodorant?",
    "model": "llama-3.3-70b-versatile",
    "host": "cloud groq"
}'
```

> Note: The model is llama-3.3-70b-versatile from Cloud Groq by default if no information is provided. Only the following models are supported right now.

```python
[
("Cloud OpenAI", "gpt-4o"),
("Cloud Groq", "llama-3.3-70b-versatile"),
("Cloud Groq", "llama3.1:8b-instruct-q8_0"),
("Local", "llama3.1:8b-instruct-q8_0"),
("Local", "llama3-groq-tool-use"),
("Local", "mistral:7b"),
]
```

## Run with Dockerfile

This may take a long time to build. Can try [Running on local machine](#run-on-local-machine)

```bash
docker build -t agent-ui --no-cache .
```

```bash
docker run -p 8888:8888 --name agent-ui agent-ui
```

1. NiceGUI UI

Access: `http://localhost:8888/ui`

---

## Pareto Frontier Evaluation

| Model                              | Latency           | accuracy | Token cost/permit   |
| ---------------------------------- | ----------------- | -------- | ------------------- |
| cloud openai gpt4o                 | 125s              |          | 5700 token/$0.0108  |
| cloud groq llama-3.3-70b-versatile | 110s              |          | 27900 token/$0.00   |
| local llama3.1:8b-instruct-q8_0    | 112s              |          | 41000 token (local) |
| local llama3-groq-tool-use         | 117s              | High     | 13200 token (local) |
| local mistral:7b                   | Cannot call tools |

## Chain of Thought

To access Chain of Thought, please access [NiceGUI](#run-on-local-machine) to view all current chains of thought.

https://github.com/user-attachments/assets/4c9ca981-8997-4503-b459-5e8e0f6e4689

# What is still Missing?

- Ensure Accuracy of the agent in different models
- Latency is still higher than the required threshold
- Dockerfile run requires more testing, still not stable

# Acknowledgement

- NiceGUI implementation by Cursor AI
