# 🤖 AI Agent

A modular AI assistant built with **FastAPI, LangChain, LangGraph, Ollama, and Streamlit**.

The project provides a containerized architecture where a Streamlit frontend communicates with a FastAPI backend, which manages the AI agent and communicates with an Ollama LLM server.

---

## ✨ Features

* 🤖 AI assistant powered by LLMs
* 🧠 LangChain integration
* 🔀 LangGraph-based agent workflow
* 🦙 Local LLM inference with Ollama
* ⚡ FastAPI REST API
* 🎨 Streamlit frontend
* 🐳 Dockerized backend and frontend
* 🔗 Docker Compose networking
* ❤️ FastAPI health-check endpoint
* 🔌 Modular architecture for adding tools and agents
* 🚀 Ready for future horizontal scaling

---

## 🛠️ Tech Stack

| Technology           | Purpose                             |
| -------------------- | ----------------------------------- |
| **Python 3.12**      | Core programming language           |
| **FastAPI**          | Backend REST API                    |
| **Uvicorn**          | ASGI server                         |
| **LangChain**        | LLM and agent framework             |
| **LangGraph**        | Agent workflow and state management |
| **LangChain Ollama** | LangChain ↔ Ollama integration      |
| **Ollama**           | Local LLM inference                 |
| **Streamlit**        | Frontend                            |
| **Docker**           | Containerization                    |
| **Docker Compose**   | Multi-container orchestration       |

---

# 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │     Browser     │
                         └────────┬────────┘
                                  │
                                  │ :8501
                                  ▼
                         ┌─────────────────┐
                         │    Streamlit    │
                         │    Frontend     │
                         └────────┬────────┘
                                  │
                                  │ HTTP
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         │  AI Assistant   │
                         │      :8000      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    LangChain    │
                         │    / LangGraph  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Ollama      │
                         │     :11434      │
                         └────────┬────────┘
                                  │
                                  ▼
                              Local LLM
```

---

# 📁 Project Structure

```text
AI_Agent/
│
├── AI_Assistant/
│   ├── __init__.py
│   ├── main.py
│   ├── Ai_agent.py
│   ├── Chatbot.py
│   └── configs.py
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker/
│   └── ai_agent.Dockerfile
│
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

### Backend

The `AI_Assistant` package contains the AI backend.

```text
AI_Assistant/
├── main.py
├── Ai_agent.py
├── Chatbot.py
└── configs.py
```

**`main.py`**

FastAPI application entry point.

**`Ai_agent.py`**

Contains the agent workflow and LangGraph logic.

**`Chatbot.py`**

Handles LLM initialization and communication with the selected model.

**`configs.py`**

Contains model and application configuration.

### Frontend

```text
frontend/
├── app.py
├── requirements.txt
└── Dockerfile
```

The Streamlit application provides the user interface and communicates with the FastAPI backend.

---

# 🔄 Request Flow

A typical request follows this flow:

```text
User
 │
 ▼
Streamlit
 │
 │ HTTP Request
 ▼
FastAPI
 │
 ▼
LangGraph
 │
 ▼
LangChain
 │
 ▼
Ollama
 │
 ▼
Local LLM
 │
 ▼
Response
 │
 ▼
FastAPI
 │
 ▼
Streamlit
 │
 ▼
User
```

---

# ⚡ Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/i-Shreyansh/AI_Agent.git
cd AI_Agent
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

# 📦 Install Dependencies

Install the backend dependencies:

```bash
python -m pip install -r requirements.txt
```

The main dependencies include:

```text
fastapi[standard]
langchain
langchain-ollama
langgraph
```

Check installed packages:

```bash
python -m pip list
```

Check individual package versions:

```bash
python -m pip show fastapi
python -m pip show langchain
python -m pip show langchain-ollama
python -m pip show langgraph
```

---

# 🦙 Ollama Setup

This project uses **Ollama** for local LLM inference.

Ollama normally listens on:

```text
http://localhost:11434
```

When the application is running through Docker Compose, the FastAPI container communicates with Ollama using the Docker service name:

```text
http://ollama:11434
```

### Example Docker network

```text
ai_assistant
     │
     │ http://ollama:11434
     ▼
ollama
```

Docker Compose automatically provides DNS resolution for the service name `ollama`.

---

# 🐳 Docker

The project uses Docker Compose to run:

```text
┌───────────────────────────────┐
│         Docker Network        │
│                               │
│ ┌─────────────┐               │
│ │  Streamlit  │               │
│ │    :8501    │               │
│ └──────┬──────┘               │
│        │                      │
│        ▼                      │
│ ┌─────────────┐               │
│ │   FastAPI   │               │
│ │    :8000    │               │
│ └──────┬──────┘               │
│        │                      │
│        ▼                      │
│ ┌─────────────┐               │
│ │   Ollama    │               │
│ │   :11434    │               │
│ └─────────────┘               │
│                               │
└───────────────────────────────┘
```

## Build and Start

From the project root:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up --build -d
```

---

# 🔍 Check Containers

```bash
docker compose ps
```

You should have three main services:

```text
ollama
ai_assistant
frontend
```

---

# 📜 View Logs

### FastAPI

```bash
docker compose logs -f ai_assistant
```

### Streamlit

```bash
docker compose logs -f frontend
```

### Ollama

```bash
docker compose logs -f ollama
```

---

# 🛑 Stop Containers

```bash
docker compose down
```

To rebuild after making Dockerfile or dependency changes:

```bash
docker compose down
docker compose build --no-cache
docker compose up
```

---

# 🌐 Services

| Service   | Internal Port | Host Port |
| --------- | ------------: | --------: |
| FastAPI   |        `8000` |    `8000` |
| Streamlit |        `8501` |    `8501` |
| Ollama    |       `11434` |   `11434` |

## FastAPI

Open:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

## Streamlit

Open:

```text
http://localhost:8501
```

## Ollama

Ollama is available at:

```text
http://localhost:11434
```

---

# ❤️ Health Check

The FastAPI application provides a health endpoint:

```http
GET /health
```

Example response:

```json
{
    "status": "healthy"
}
```

Docker can use this endpoint to determine whether the FastAPI container is healthy.

---

# 🔌 API

The FastAPI application acts as the communication layer between the frontend and the AI agent.

Example structure:

```text
POST /chat
       │
       ▼
FastAPI
       │
       ▼
LangGraph Agent
       │
       ▼
LLM
       │
       ▼
Response
```

Example request:

```json
{
    "message": "Hello"
}
```

---

# 🧠 LangGraph Agent

The AI workflow is designed around LangGraph.

A simplified workflow is:

```text
             ┌──────────────┐
             │ User Request │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ LangGraph    │
             │ Agent        │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │     LLM      │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │   Response   │
             └──────────────┘
```

The architecture can later be extended with:

* 🛠️ Tools
* 🔎 RAG
* 🌐 Web search
* 🧮 Calculator
* 🗄️ Database tools
* 🧠 Persistent memory
* 👥 Multi-agent workflows
* 🔐 Human-in-the-loop
* 📋 Background tasks

---

# 🐳 Dockerfile Optimization

Both the FastAPI and Streamlit containers use **multi-stage Docker builds**.

The general pattern is:

```text
Builder Stage
     │
     ├── Create virtual environment
     ├── Install dependencies
     │
     ▼
Production Stage
     │
     ├── Copy virtual environment
     ├── Copy application
     └── Run application
```

This keeps build-related files out of the final image and helps keep the production image smaller.

---

# 📈 Future Scaling

The current architecture runs a single FastAPI instance:

```text
Streamlit
    │
    ▼
FastAPI
    │
    ▼
Ollama
```

For higher traffic, the backend can be scaled horizontally:

```text
                    Load Balancer
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          FastAPI #1 FastAPI #2 FastAPI #3
              │          │          │
              └──────────┼──────────┘
                         │
                         ▼
                    AI Workers
                         │
                  ┌──────┴──────┐
                  ▼             ▼
               Ollama        Ollama
                 GPU            GPU
```

Future infrastructure can include:

* Load balancer
* Multiple FastAPI replicas
* Redis for shared state
* Background workers
* Message queues
* Multiple GPU inference servers
* Kubernetes

---

# 🔐 Security

Before deploying publicly:

* Never commit API keys.
* Keep `.env` files out of Git.
* Use strong secrets.
* Restrict access to Ollama.
* Add authentication to protected endpoints.
* Add rate limiting.
* Use HTTPS in production.
* Validate incoming requests.
* Configure appropriate CORS policies.

Example `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# 🧪 Development

Run FastAPI locally:

```bash
python -m uvicorn AI_Assistant.main:app --host 0.0.0.0 --port 8000 --reload
```

Run Streamlit locally:

```bash
python -m streamlit run frontend/app.py
```

---

# 🐞 Troubleshooting

### Streamlit cannot find `app.py`

Make sure the Dockerfile's working directory and `COPY` command match the location of your Streamlit application.

For example:

```dockerfile
WORKDIR /app
COPY . .
```

followed by:

```dockerfile
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

### Port 8501 already in use

Check the port on Windows:

```powershell
netstat -ano | findstr :8501
```

Alternatively, change the host port:

```yaml
ports:
  - "8502:8501"
```

Then access:

```text
http://localhost:8502
```

### FastAPI container cannot connect to Ollama

Inside Docker, use:

```text
http://ollama:11434
```

instead of:

```text
http://localhost:11434
```

### Rebuild dependencies

If `requirements.txt` changes:

```bash
docker compose build --no-cache ai_assistant
```

Then:

```bash
docker compose up
```

---

# 🚀 Roadmap

* [x] FastAPI backend
* [x] Streamlit frontend
* [x] Ollama integration
* [x] LangChain integration
* [x] LangGraph agent workflow
* [x] Docker support
* [x] Docker Compose
* [x] FastAPI health check
* [ ] Agent tools
* [ ] Persistent conversation memory
* [ ] Redis integration
* [ ] Authentication
* [ ] Rate limiting
* [ ] Background task processing
* [ ] Horizontal FastAPI scaling
* [ ] Load balancing
* [ ] Kubernetes deployment

---

# 👨‍💻 Author

**Shreyansh**

GitHub: **[@i-Shreyansh](https://github.com/i-Shreyansh)**

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**Built with Python, FastAPI, LangChain, LangGraph, Ollama & Docker.**
