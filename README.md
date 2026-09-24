# QueryMind AI

> **LLM-Powered Natural Language to SQL Analytics Platform**

QueryMind AI is an AI-powered analytics platform that allows users to interact with relational databases using natural language instead of writing SQL queries manually.

The system uses a Large Language Model (LLM) to understand a user's question, identify the relevant database schema, generate SQL, validate the generated query, execute it safely against the database, and return the results in an understandable format.

## 🎯 Problem Statement

Interacting with relational databases often requires users to have SQL knowledge. Business users, analysts, and other non-technical users may understand the questions they want to ask but may not know how to translate those questions into SQL queries.

QueryMind AI aims to bridge this gap by allowing users to ask questions about their data using natural language.

### Example

**User:**

> Which five customers generated the highest revenue last month?

**QueryMind AI:**

```sql
SELECT customer_id, SUM(amount) AS total_revenue
FROM orders
WHERE order_date >= ...
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 5;
```

The generated query is validated, executed against the database, and the results are returned to the user.

---

## 🚀 Planned Features

* Natural language to SQL generation
* LLM-powered query understanding
* Database schema awareness
* Multi-table SQL generation and joins
* SQL validation and safety guardrails
* Read-only database execution
* Automatic SQL error correction
* Conversational follow-up questions
* Query result summarization
* Automatic data visualization
* Query history
* Evaluation framework for Text-to-SQL performance
* Docker-based deployment
* AWS deployment
* Authentication and access control

---

## 🏗️ Architecture

The planned system architecture is:

```text
User
  │
  ▼
Natural Language Question
  │
  ▼
FastAPI
  │
  ▼
Query Understanding
  │
  ▼
Schema Retrieval
  │
  ▼
LLM
  │
  ▼
SQL Generation
  │
  ▼
SQL Validation & Guardrails
  │
  ▼
PostgreSQL
  │
  ▼
Query Results
  │
  ▼
Result Interpretation
  │
  ▼
Natural Language Response
```

---

## 🛠️ Technology Stack

| Component            | Technology   |
| -------------------- | ------------ |
| Programming Language | Python 3.11  |
| Backend              | FastAPI      |
| LLM Runtime          | Ollama       |
| Database             | PostgreSQL   |
| Database Access      | SQLAlchemy   |
| SQL Validation       | SQLGlot      |
| Data Validation      | Pydantic     |
| Testing              | Pytest       |
| Linting              | Ruff         |
| Containerization     | Docker       |
| Version Control      | Git / GitHub |
| Cloud                | AWS          |

The initial implementation will use an existing open-source LLM locally through Ollama. Model selection and benchmarking will be performed during development.

---

## 📁 Project Structure

```text
querymind-ai/
│
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Configuration and core utilities
│   ├── db/           # Database connection and database utilities
│   ├── llm/          # LLM integration
│   ├── schema/       # Database schema extraction and retrieval
│   ├── sql/          # SQL generation and validation
│   ├── services/     # Application/business logic
│   ├── models/       # Application and data models
│   └── main.py       # FastAPI application entry point
│
├── tests/            # Automated tests
├── scripts/          # Utility and setup scripts
├── docs/             # Technical documentation
├── data/             # Development/sample data
├── docker/           # Docker-related configuration
│
├── .env.example      # Environment variable template
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## 🔐 Security Approach

Since the system executes LLM-generated SQL, security is a core part of the design.

The planned system will include:

* Read-only database credentials
* SQL statement validation
* Prevention of destructive SQL operations
* Query execution limits
* Query timeouts
* Table and column validation
* Controlled database permissions
* Error handling without exposing sensitive information
* Authentication and authorization for production deployments

The LLM will not be given unrestricted database privileges.

---

## 🧪 Evaluation

The system will eventually include a Text-to-SQL evaluation framework.

Metrics will include:

* SQL execution accuracy
* Query correctness
* SQL syntax error rate
* Query correction rate
* Response latency
* LLM token usage
* Failure/retry rate

A benchmark dataset containing natural-language questions, database schemas, expected SQL queries, and expected results will be used to evaluate the system.

---

## 🗺️ Development Roadmap

### Phase 1 — Foundation

* [x] Project initialization
* [x] Python virtual environment
* [x] Git repository
* [x] GitHub repository
* [x] Python project configuration
* [ ] PostgreSQL setup

### Phase 2 — Core Text-to-SQL

* [ ] Database schema
* [ ] Ollama setup
* [ ] LLM integration
* [ ] Natural language → SQL
* [ ] SQL execution

### Phase 3 — Safety & Reliability

* [ ] SQL validation
* [ ] Read-only execution
* [ ] Query limits
* [ ] Error handling
* [ ] Automatic SQL correction

### Phase 4 — AI Intelligence

* [ ] Schema retrieval
* [ ] Conversation context
* [ ] Follow-up questions
* [ ] Result interpretation

### Phase 5 — Analytics

* [ ] Automatic visualization
* [ ] Query history
* [ ] Analytics interface

### Phase 6 — Evaluation & Production

* [ ] Text-to-SQL benchmark
* [ ] Automated testing
* [ ] Logging and observability
* [ ] Docker
* [ ] CI/CD
* [ ] AWS deployment

---

## 💻 Local Development

### Prerequisites

* Python 3.11+
* Git
* Docker
* Docker Compose
* Ollama

### Setup

Clone the repository:

```bash
git clone https://github.com/KUNALKANK1737/querymind-ai.git
cd querymind-ai
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -e ".[dev]"
```

Additional setup instructions will be added as the database and LLM components are implemented.

---

## 📌 Project Status

**Current status: Early development**

The project foundation, Python environment, dependency configuration, Git repository, and GitHub repository have been established.

The next milestone is setting up PostgreSQL and designing the database schema used for the initial Text-to-SQL implementation.

---

## 👨‍💻 Author

**Kunal Kank**

GitHub: [KUNALKANK1737](https://github.com/KUNALKANK1737)

---

## 📄 License

License information will be added before the first public release.
