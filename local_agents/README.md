# VS Code Agentic AI Development Setup

A comprehensive roadmap for mastering VS Code with AI-powered development workflows, from basic setup to advanced agentic systems deployment.

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

- [ ] **All code in dev-container** — no "works-on-my-machine" bugs
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
- [ ] Install Docker Desktop + VS Code
- [ ] Create `.devcontainer/` with: `python:3.11`, `node`, `git`, `uv`
- [ ] Add Dev Containers, Python, Remote-Containers extensions

**Core tools mastered:** Dev Containers • uv • Git basics
**🎯 Outcome:** Repo scaffold + Devcontainer JSON

---

### Week 1: Raw LLM API
**Steps:**
- [ ] Install ⚡ ollama or ⚡ vLLM (GPU) as local OpenAI-compatible server
- [ ] Call it from Python (requests) inside container
- [ ] Benchmark prompt/latency with ⚡ httpx async

**Core tools mastered:** ollama / vLLM • httpx • asyncio
**🎯 Outcome:** `hello_llm.py` benchmark script

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
- [ ] Week 0: Environment Setup
- [ ] Week 1: Raw LLM API Integration
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