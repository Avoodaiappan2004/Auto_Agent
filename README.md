# 🚀 AutoDevAgent – Autonomous AI Developer

AutoDevAgent is a fully autonomous AI agent that can **discover problems, plan solutions, generate code, verify outputs, and deploy projects** — all without human intervention.

Built for the **"No Humans Required" Autonomous Agent Challenge**, this project demonstrates real-world autonomous agent behavior using multiple tools, blockchain simulation, and trust scoring.

---

## 🧠 Key Features

* 🔄 **Full Autonomous Loop**
  `discover → plan → execute → verify → submit`

* 🤖 **Multi-Agent Architecture**

  * PlannerAgent → Task planning
  * CoderAgent → Code generation
  * VerifierAgent → Output validation
  * GitHubAgent → Deployment

* 🛠️ **Multi-Tool Integration**

  * Groq API (AI generation)
  * File system (project creation)
  * GitHub (auto deployment)
  * SMTP (email automation)
  * Blockchain simulator (logs + identity)

* 🔐 **Safety Guardrails**

  * Blocks unsafe commands
  * Validates generated outputs
  * Prevents invalid execution

* ⚡ **Compute Budget Awareness**

  * Limits API usage
  * Prevents infinite loops

* ⛓️ **Blockchain + Trust System (Simulated ERC-8004)**

  * Logs agent actions
  * Maintains trust score
  * Tracks agent reputation

---

## 📁 Project Structure

```
auto_python/
│
├── agent.py
├── tools.py
├── blockchain.py
├── agent.json
├── server.py
├── .env
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── projects/
├── agent_log.json
├── chain.json
├── trust.json
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd auto_python
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

GITHUB_USERNAME=your_username
GITHUB_TOKEN=your_token
```

---

### 5️⃣ Run Backend Server

```bash
python server.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

### 6️⃣ Run Frontend

```bash
cd frontend
python -m http.server 5500
```

Open:

```
http://localhost:5500
```

---

## 🎯 How to Use

### Example Tasks


create calculator web app


create todo app and push to github


send email to example@gmail.com saying hello


## 📊 Outputs

* 📁 Projects → `projects/`
* 📜 Logs → `agent_log.json`
* 🔗 GitHub repo → `auto created`
* ⛓️ Blockchain logs → `chain.json`
* ⭐ Trust score → `trust.json`

---

## 🔐 Safety & Guardrails

* Blocks destructive commands
* Validates outputs before execution
* Prevents unsafe operations

---

## ⚡ Compute Budget

* Max API calls: **10**
* Retry limit: **2**

---

## ⛓️ ERC-8004 Identity (Simulated)

Agent identity is maintained using:

* `agent.json`
* `chain.json`

> Note: ERC-8004 is simulated using local blockchain logging.

---

## 🤖 Multi-Agent System

| Agent         | Role               |
| ------------- | ------------------ |
| PlannerAgent  | Task decomposition |
| CoderAgent    | Code generation    |
| VerifierAgent | Output validation  |
| GitHubAgent   | Deployment         |

---

## 📈 Trust System

* Success → +1
* Failure → -1

Stored in `trust.json`

---

## 🏆 Why This Project?

This agent proves that AI can:

* Operate independently
* Use multiple tools
* Self-correct errors
* Deploy real applications
* Maintain identity & trust

---

## 📹 Demo

(Add your demo video link here)

---

## 👨‍💻 Author

**Avoodaiappan M**
Autonomous AI Developer 🚀

---
