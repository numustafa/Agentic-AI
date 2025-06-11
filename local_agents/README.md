# VS Code Agentic AI Development Setup

A comprehensive roadmap for mastering VSCode with AI-powered development workflows, from basic setup to advanced agentic systems deployment.

## 🎯 Goal and Objectives

### **Primary Goal: Ship a Fully Local AI Agent System**
Build a production-ready, observable, and secure AI agent that runs entirely on your local machine with **zero cloud dependencies**.

### **Core Objectives:**
- **🏗️ Architecture Mastery**: Create a complete local AI stack (LLM + Vector DB + Tools + Orchestration)
- **🔧 VS Code Expertise**: Wield VS Code like a lightsaber with dev containers, extensions, and workflows
- **📊 Production Standards**: Implement enterprise-grade observability, testing, and security
- **🛡️ Self-Sufficiency**: Eliminate dependence on cloud providers while maintaining professional quality
- **🚀 Deployment Ready**: Ship a containerized system that works anywhere

### **Success State After 8 Weeks:**
```bash
# Single command deployment of your complete AI agent:
docker-compose up

# Capabilities unlocked:
✅ Local ChatGPT-like interface (no API keys needed)
✅ Tool-calling capabilities (weather, document search, etc.)
✅ RAG-powered document Q&A system  
✅ Full observability dashboard (Jaeger + OpenTelemetry)
✅ Security monitoring and guardrails
✅ Enterprise-grade testing and CI/CD
✅ Zero cloud lock-in, 100% controllable
```

### **Professional Impact:**
- **Cost Control**: No per-token charges or API rate limits
- **Privacy**: All data and processing stays on your machine
- **Customization**: Full control over model behavior and capabilities  
- **Enterprise-Ready**: Production observability, security, and deployment patterns
- **Future-Proof**: Foundation for any AI project you build going forward

---

## 🧠 What You're Actually Building

### **Not Just a Weather Bot - A Complete AI Agent Platform**

This project builds a **general-purpose AI agent system** that can handle any task you give it. Weather is just one example tool to demonstrate capabilities.

### **Your Final Agent Will Handle Conversations Like:**

````bash
💬 You: "What's the weather in Paris and should I pack a jacket?"
🤖 Agent: 
   1. 🌤️ Calls weather API for Paris current conditions
   2. 📊 Analyzes temperature data and precipitation 
   3. 💡 Provides clothing recommendation based on forecast

💬 You: "Summarize that PDF I uploaded about AI safety"
🤖 Agent:
   1. 🔍 Searches your local vector database for the document
   2. 📝 Finds and retrieves relevant document chunks
   3. 🧠 Generates comprehensive summary using local LLM

💬 You: "Plan a 3-day trip to Tokyo, check weather and find restaurants"
🤖 Agent:
   1. 🌤️ Calls weather API for 3-day Tokyo forecast
   2. 🔍 Searches your travel documents in RAG system
   3. 🍜 Queries restaurant database or web search
   4. 📋 Creates complete itinerary with weather-appropriate activities
`````

---

## 📋 Essential Extensions Overview

| Extension | Purpose | Why You Need It |
|-----------|---------|-----------------|
| Dev Containers | Reproducible Python+Docker envs | Consistent development environment across machines |
| Python | Linting, run/debug | Core Python development support |
| Jupyter | In-editor notebooks | Interactive development and data analysis |
| Continue (OSS Copilot) | Local LLM coding help via ollama | AI assistance without cloud dependency |
| Docker | Compose & container logs | Container management and debugging |
| GitLens | Advanced Git workflow | Enhanced version control visualization |
| LangChain Vis | Visualise agent graphs | Debug and understand AI agent flows |
| OpenTelemetry Insight | View traces inline | Monitor and debug distributed systems |

## 🔒 Non-Negotiable Workflow Rules

- [✅] **All code in dev-container** — no "works-on-my-machine" bugs (use `.devcontainer/`)
- [ ] **Weekly git tag and docker push** — consistent versioning
- [ ] **≤ 45 min video → write code immediately** (Bootcamp clips only when matching current step)
- [ ] **Trace everything** — if span missing in Jaeger/Tempo, you're not done
- [ ] **Fail-fast security** — CI must block merge on jailbreak success

*Pin this plan; tick boxes weekly. Finish Loop A → Loop B → optional Loop C.*

**Goal:** By the end, you'll wield VS Code like a lightsaber, drive your own LLMs, and deploy agentic systems anywhere—cloud optional, skill maximal. 🚀

---

## 🎯 LOOP A: "Ship Local Agent" - 8 Weeks (≈ 7h/wk)

### Week 0: Prep
**Steps (in order):**
- [✅] Install Docker Desktop + VS Code <br>
        Since I am using WSL on a Windows machine, I will first install [Docker](https://docs.docker.com/desktop/setup/install/windows-install/) Desktop and then enable WSL integration in Docker settings.
- [✅] Install VSCode Server in the WSL workspace (`code .`) and complete the extensions stack: Dev Containers, Python, Jupyter, Docker, GitLens. 
        This way I can use the same VSCode instance in WSL and Windows. Windows VSCode (Client) ←→  VS Code Server (WSL)  (Bridge) ←→  Project Files (Linux filesystem). The VSCode runs on Windows machine, the project files and code run in WSL (Linux) environment, while the VS Code Server runs in WSL to provide the bridge between the two.                        
- [✅] Create clean `.devcontainer/` with simple Dockerfile: `python:3.11`, `node`, `git`, `uv`
      Windows Machine
        └── VS Code (WSL: Ubuntu) ← Same window, enhanced!
            └── Dev Container ← This runs INSIDE your WSL VS Code
                ├── Python 3.11 environment
                ├── Node.js
                ├── Git & UV tools
                ├── All extensions auto-installed
                └── Connection to ollama or vLLM server
- [✅] Test: Open Project in Dev Container
        - Open the project folder in VS Code, then run `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
        - Wait for the container to build and start
        - Open a terminal inside the container and run `python --version` to verify Python is set up correctly
- [✅] Test ollama or vLLM server connection: `curl http://host.docker.internal:11434/v1/models`
        - Downloaded and installed ollama directly on Windows host machine
        - Pulled Qwen3 8B parameter model using `ollama run qwen3` (which auto-started ollama service)
        - Verified ollama was running with `Get-Process ollama` and `netstat -an | findstr 11434`
        - Tested connection from PowerShell: `curl http://localhost:11434/v1/models` ✅
        - Initially tried `curl http://localhost:11434/v1/models` from dev container ❌ (failed - localhost refers to container)
        - Tried `curl http://172.17.0.1:11434/v1/models` from dev container ❌ (failed - ollama bound to 127.0.0.1 only)
        - Successfully tested `curl http://host.docker.internal:11434/v1/models` from dev container ✅
        - Confirmed JSON response: `{"object":"list","data":[{"id":"qwen3:latest","object":"model","created":1749224147,"owned_by":"library"}]}`
        - Updated devcontainer.json with `"runArgs": ["--network=host"]` and `"forwardPorts": [8000, 11434]`
        - Security verified: Container isolation working, external access blocked ✅
        - Key insight: Use `host.docker.internal:11434` for dev container → host communication on Windows/WSL

**Core tools mastered:** Dev Containers • uv • Git basics
**🎯 Outcome:** Clean, minimal dev container setup
---


### Week 1: Raw LLM API
**Steps:**
- [✅] Call it from Python (requests) inside container
- [✅] Benchmark prompt/latency with ⚡ httpx async

**Detailed Implementation:**
- [✅] **Basic Connection Setup** 
        - Created `hello_llm.py` with requests library for synchronous API calls to ollama
        - Implemented connection testing function using `GET /api/tags` endpoint
        - Verified JSON response parsing and error handling for network issues
        - Established `OLLAMA_BASE_URL = "http://host.docker.internal:11434"` as standard connection pattern

- [✅] **Performance Benchmark Development**
        - Built comprehensive sync vs async vs concurrent comparison framework
        - Implemented three request patterns:
          - 🐌 **Synchronous**: Sequential requests using `requests` library
          - ⚡ **Async Sequential**: Sequential requests using `httpx.AsyncClient` 
          - 🚀 **Concurrent**: Parallel requests using `asyncio.gather()`
        - Added Rich console styling for clear performance visualization
        - Created timing measurements with `time.perf_counter()` for microsecond precision

- [✅] **Cold Start vs Warm Performance Analysis**
        - Discovered critical LLM performance concept: model loading overhead
        - Built `hello_llm_explained.py` educational module with 5-step diagnostic process:
          1. Basic connection testing (`GET /api/tags`)
          2. Model availability checking (`GET /api/tags` with detailed parsing)
          3. Memory loading status (`GET /api/ps` for active models)
          4. Cold/warm concepts explanation with real-world analogies
          5. Live demonstration with timing comparisons
        - Identified 20-30 second cold start penalty vs 1-3 second warm requests

- [✅] **Advanced Workflow Optimization** 
        - **Strategy 1**: Intelligent Model State Management
          - Added `ModelStateManager` class for proactive model state detection
          - Implemented user choice for warmup vs cold start measurement
          - Created smart warmup process with progress tracking
        - **Strategy 2**: Adaptive Timeout Management  
          - Built `AdaptiveTimeoutManager` with performance history learning
          - Dynamic timeout calculation: 45s for cold start, 15s for warm, adaptive based on history
          - Eliminated timeout failures through intelligent timeout selection
        - **Strategy 3**: Development Workflow Orchestration
          - Created `dev_workflow.py` as central command hub for all Week 1 tools
          - Quick 30-second connectivity tests for rapid iteration
          - Tool selection menu for different analysis needs

- [✅] **Performance Results Achieved**
        - **Before Optimization**: 26+ second average latency, 67% timeout failure rate
        - **After Optimization**: 2.9 second average latency, 100% success rate  
        - **9.1x Performance Improvement** through state management and adaptive timeouts
        - **Production-Grade Reliability**: Eliminated all timeout failures

- [✅] **Key Learning Outcomes**
        - Model lifecycle management: Understanding memory vs disk storage
        - Async programming patterns: True concurrency benefits only visible with warm models
        - Production LLM considerations: Cold start penalties, timeout strategies, state awareness
        - Professional workflow development: Tool orchestration, rapid iteration, diagnostic capabilities

**Core tools mastered:** ollama • httpx • asyncio • Rich console • Model state management
**🎯 Outcome:** 
- `hello_llm.py` - Enhanced benchmark with intelligent state management
- `hello_llm_explained.py` - Educational module for deep LLM performance understanding  
- `dev_workflow.py` - Development workflow orchestration tool
- `cold_warm_benchmark.py` - Specialized cold vs warm analysis utility

**Performance Achievement:** 🚀 **9.1x faster, 100% reliable LLM API benchmark system**

---

### Week 2: Prompt Craft
**Steps:**
- [ ] Install 🔗 Jupyter & Continue extensions
- [ ] Study CoT / ReAct – test in notebook
- [ ] Save best prompts under `prompts/*.yaml`

**Core tools mastered:** Jupyter in VS Code • Prompt techniques
**🎯 Outcome:** `prompt_playbook.ipynb`

---

### Week 3: Structured Outputs & Tools
**Steps:**
- [ ] Add ⚡ pydantic-v2 & FastAPI
- [ ] Build `weather_tool/` (FastAPI micro-svc) returning Pydantic model
- [ ] Use `openai.FunctionCaller` (or litellm) to call from LLM

**Core tools mastered:** FastAPI • Pydantic-v2 • litellm
**🎯 Outcome:** Docker-built `weather_tool` image

---

### Week 4: Vector RAG
**Steps:**
- [ ] Spin up ⚡ pgvector in `docker-compose.yml`
- [ ] Install ⚡ langchain + chromadb
- [ ] Load a PDF, chunk & embed with local `ollama` model, store to pgvector

**Core tools mastered:** pgvector • LangChain Embeddings
**🎯 Outcome:** `rag_demo/` with REST endpoint

---

### Week 5: Agent v1
**Steps:**
- [ ] Install ⚡ LangGraph 🔗 extension LangChain Vis
- [ ] Implement Planner-Executor graph that:
  - ⭕ calls `weather_tool` ⭕ queries pgvector ⭕ returns answer

**Core tools mastered:** LangGraph • LangChain Tools
**🎯 Outcome:** `agents/core_agent.py` + Graph viz

---

### Week 6: Observability & Tests
**Steps:**
- [ ] Add ⚡ OpenTelemetry SDK + ⚡ pytest-asyncio
- [ ] Trace every agent span to Jaeger (local docker)
- [ ] Write unit + eval tests; gate with GitHub Actions

**Core tools mastered:** OTEL • Pytest • GitHub CI
**🎯 Outcome:** Passing CI + Jaeger UI screenshot

---

### Week 7: Security, Guardrails, Release
**Steps:**
- [ ] Install ⚡ GuardrailsAI + Rebuff
- [ ] Add input/output guards & jailbreak tests
- [ ] Publish multi-service `docker-compose` to Docker Hub

**Core tools mastered:** GuardrailsAI • Compose • Hub
**🎯 Outcome:** v1.0 tag + Docker Hub link

---

**✅ LOOP A COMPLETE:** You now have a fully local, observable, guarded agent running on your machine—no cloud lock-in, 100% controllable from VS Code.

---

## 🔥 LOOP B: Deep-Dive Sprints - 6 Weeks (≈ 4h/sprint)

| Sprint | Focus | Action | Tooling Detail | Status |
|--------|-------|--------|----------------|--------|
| **B1** | Async Power-Up | Replace all blocking LangChain calls with `await` + `asyncio.gather`; prove ≥ 40% latency drop in Grafana | python-asyncio-tools • fastapi-concurrency | ⬜ |
| **B2** | Hybrid Search & Re-rank | Plug colbert-torrent or tart-rerank; compare top-k accuracy vs baseline | ColBERT • qdrant-client | ⬜ |
| **B3** | Memory (mem0 + MCP) | Run mem0 via Docker; hot-swap session memory; store long-term notes | mem0 • MCP protocol | ⬜ |
| **B4** | Model Routing | Add liteLLM gateway → route queries: local (vLLM) ↔ remote (OpenRouter / Gemini) on budget rules | liteLLM • yaml routing | ⬜ |
| **B5** | Red-Team & Eval | Integrate prompt-inject dataset; CI fails on jailbreak success; add cost metric in report | prompt-inject • pandas-report | ⬜ |
| **B6** | OpenTelemetry Full Chain | Export non (if used) + FastAPI + pgvector traces to Grafana Tempo; link spans | Tempo • Grafana Loki | ⬜ |

---

## 🚀 LOOP C: Frontier Spikes - Pick Any (2 wks each)

| Spike | Mini-project | Extra tools / extensions |
|-------|-------------|-------------------------|
| **Edge Quantisation** | Run Gemma-2b Q4_K.gguf in ⚡ llama.cpp; compare throughput vs API | llama.cpp • gperftools |
| **Voice / Vision Agent** | VS Code + ⚡ whisper-cpp + webcam → transcribe & reason locally | whisper-cpp • opencv-python |
| **Robotics** | ESP32 bot listens to agent via MQTT; executes move commands | micropython-tools • mqtt-asyncio |
| **Auto-Prompt (DsPy)** | Use DsPy to evolve your RAG prompt & log eval gain | DsPy • matplotlib |
| **LangGraph UI** | Embed graphviz view inside VS Code Webview extension you write yourself | VS Code Webview API |

---

## 📊 Progress Tracking

### ✅ Completed Tasks
- [✅] Week 0: Environment Setup
- [✅] Week 1: Raw LLM API Integration
- [ ] Week 2: Prompt Engineering Mastery
- [ ] Week 3: Structured Outputs & Tools
- [ ] Week 4: Vector RAG Implementation
- [ ] Week 5: Agent v1 Development
- [ ] Week 6: Observability & Testing
- [ ] Week 7: Security & Release

### 🔄 Current Sprint Progress
- [ ] **Current Week:** ___________
- [ ] **Hours Spent This Week:** _____ / 7
- [ ] **Blockers:** ___________
- [ ] **Next Priority:** ___________

### 🎯 Loop Completion Status
- [ ] **Loop A Complete** (Ship Local Agent)
- [ ] **Loop B Sprints:** _____ / 6 completed
- [ ] **Loop C Spikes:** _____ selected and completed

---

## 🛠️ Quick Setup Commands

```bash
# Initial setup
git clone <your-repo>
cd agentic-ai-setup
code .

# Open in Dev Container
# Ctrl+Shift+P → "Dev Containers: Reopen in Container"

# Start local LLM server
docker run -d -p 11434:11434 ollama/ollama
ollama pull llama2

# Install core dependencies
pip install -r requirements.txt
```

---

## 📚 Resources & References

- **VS Code Dev Containers:** [Official Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- **LangChain:** [Getting Started Guide](https://python.langchain.com/docs/get_started/introduction)
- **OpenTelemetry Python:** [Instrumentation Guide](https://opentelemetry.io/docs/instrumentation/python/)
- **Docker Compose:** [Compose File Reference](https://docs.docker.com/compose/compose-file/)

---

## 🎉 Success Metrics

By completing this roadmap, you will have:

1. **🏗️ Built** a fully functional local AI agent system
2. **🔧 Mastered** VS Code development containers and extensions
3. **📊 Implemented** comprehensive observability and testing
4. **🛡️ Secured** your AI system with guardrails and security measures
5. **🚀 Deployed** a production-ready agentic AI application

**Time Investment:** 8 weeks × 7 hours = 56 hours total for Loop A
**Skill Level:** Beginner → Advanced AI Developer
**Outcome:** Production-ready, observable, secure AI agent system 🎯

---

## 🏠 Your Local Machine
├── 🧠 LLM Brain (Qwen3 via Ollama)
│   └── Core reasoning, conversation, planning
├── 🔧 Tool Layer (Extensible)
│   ├── 🌤️ Weather API (FastAPI microservice)
│   ├── 📚 Document Search (pgvector RAG)
│   ├── 🌐 Web Search (future)
│   └── 📧 Email/Calendar (future)
├── 🤖 Agent Orchestrator (LangGraph)
│   └── Plans tasks, calls tools, manages workflow
├── 💾 Memory System (pgvector + embeddings)
│   └── Remembers conversations, stores knowledge
├── 📊 Observability Stack (OpenTelemetry + Jaeger)
│   └── Traces every decision and action
└── 🛡️ Security Layer (GuardrailsAI)
    └── Prevents jailbreaks and harmful outputs