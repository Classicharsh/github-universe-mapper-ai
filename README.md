# GitHub Universe Mapper AI 🌌

An AI-powered technology trend analytics and visualization platform designed to analyze the global open-source software ecosystem. By mapping repositories, developers, and packages, this platform detects emerging technologies, trending frameworks, declining tools, skill clusters, and future developer skill demands.

---

## 🚀 Project Overview

GitHub Universe Mapper AI is a serious portfolio project that ingests public GitHub data (via GitHub Archive, Event Streams, and API) to build a multi-dimensional graph of the open-source world. It leverages Graph Neural Networks (GNNs), Natural Language Processing (NLP), and classic machine learning to generate foresight on technology adoption curves and developer skill evolution.

### Key Capabilities
- **Trend Detection**: Early-stage tracking of rising libraries, frameworks, and packages.
- **Sentiment & Vitality Analysis**: Measuring community health, code activity, and repository sentiment.
- **Skill Clustering & Demand Forecasting**: Identifying related technology clusters (e.g., ML-Ops, Web3, Edge Computing) and forecasting which skills will be in high demand next.
- **Interactive Map**: A visual interface mapping the dependencies, developers, and repositories as an interactive universe of code.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, FastAPI (Asynchronous API layer)
- **Frontend**: React, Recharts (Modern data dashboards), Vite
- **Databases**:
  - **PostgreSQL**: Relational storage for repos, users, and time-series metrics.
  - **Neo4j**: Graph database to map complex developer-to-repo and repo-to-dependency relationships.
- **Machine Learning & AI**: 
  - Sentence-Transformers / PyTorch (Embedding codebases, topics, and developer profiles)
  - NetworkX / GNNs (Graph feature extraction)
- **Visualization**: 3D Graph visualization, React-Three-Fiber, Recharts

---

## 📁 Repository Structure

```text
github-universe-mapper/
├── backend/          # FastAPI API layer, routers, and ingestion services
│   └── main.py       # Application entry point with basic API routing
├── frontend/         # React application (Vite-powered UI dashboard)
├── ml/               # Python ML models, embeddings generator, and training code
│   └── models/       # Saved model checkpoints and hyperparameter configs
├── data/             # Sample datasets, raw JSON outputs (gitignored)
├── notebooks/        # Jupyter Notebooks for data analysis, EDA, and model testing
├── docs/             # API specifications, architecture diagrams, and roadmap details
├── requirements.txt  # Python environment dependencies
└── .gitignore        # Version control excludes for environments, data, and keys
```

---

## 📖 Getting Started (Day 1 Starter Setup)

### Prerequisites
- **Python 3.10+** installed
- **pip** (Python package installer)

### Backend Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI development server:
   ```bash
   uvicorn backend.main:app --reload
   ```

4. Verify the server is running by visiting:
   - Homepage: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
   - Interactive Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📅 30-Day Development Roadmap

- **Day 1**: Project foundation, API starter setup, requirements management, and directory structures.
- **Days 2–10**: Data ingestion pipelines (GitHub API, archive ingestion), PostgreSQL schema, and database connections.
- **Days 11–20**: Neo4j integration, Graph modeling, training machine learning models for clustering and forecasting.
- **Days 21–28**: React dashboard implementation, Recharts visualizations, interactive maps, and API consumption.
- **Days 29–30**: Optimization, styling, deployment configs, and documentation completion.
