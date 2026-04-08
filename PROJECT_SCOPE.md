# PROJECT_SCOPE.md — [PROJECT_NAME]

> This file contains all project-specific context, architecture, data sources, and build order.
> Claude Code must read this file at the start of every session alongside CLAUDE.md.
> For coding standards, behavior rules, and git workflow, see CLAUDE.md.

---

## Project Overview

[What does this project do and why does it exist? 2-3 sentences max.]

**Sprint:** [Sprint number and focus]
**Owner:** [Name]
**Approvers:** [Names]

---

## What This Sprint Delivers

- [Capability 1]
- [Capability 2]
- [Capability 3]

## Not in This Sprint

- [Deferred item 1]
- [Deferred item 2]

---

## Tech Stack

| Component | Tool |
|---|---|
| Language | [e.g., Python 3.11+] |
| Framework | [e.g., Anthropic Python SDK] |
| Database | [e.g., PostgreSQL] |
| APIs | [e.g., Slack, Teamwork] |
| UI | [e.g., Gradio] |
| Hosting | [e.g., Google Cloud Run] |
| Containerization | [e.g., Docker] |

---

## MVC Project Structure

Per CLAUDE.md, this project follows MVC architecture.

```
[project-name]/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── README.md
├── CLAUDE.md
├── PROJECT_SCOPE.md
├── memory.md
├── main.py
│
├── config/
│   └── settings.py
│
├── models/
│   └── [data models here]
│
├── controllers/
│   └── [business logic here]
│
├── views/
│   └── [output formatting / UI here]
│
├── tools/
│   └── [external API clients here]
│
└── tests/
    └── [test files here]
```

---

## Data Flow

```
[Describe how data moves through the system. Example:]
1. main.py triggers
2. Controller gets data from tools
3. Controller processes and classifies
4. View formats output
5. Tool delivers output (Slack, email, etc.)
```

---

## Data Sources

### [Source 1 Name]

| Table / Endpoint | Purpose |
|---|---|
| [table or URL] | [what it provides] |

### [Source 2 Name]

| Table / Endpoint | Purpose |
|---|---|
| [table or URL] | [what it provides] |

---

## Environment Variables (.env)

```
# [Service 1]
SERVICE_1_API_KEY=
SERVICE_1_URL=

# [Service 2]
SERVICE_2_HOST=
SERVICE_2_PORT=
SERVICE_2_USER=
SERVICE_2_PASSWORD=
```

---

## Build Order

Complete each step before moving to the next. Per CLAUDE.md, ask permission before every action.

### Step 0: Prerequisites
- [ ] [Credential or access needed]
- [ ] [Credential or access needed]

### Step 1: Project Setup
- [ ] Create MVC folder structure
- [ ] Set up Python venv
- [ ] Install dependencies
- [ ] Create `.env.example` and `.gitignore`
- [ ] Create `requirements.txt`

### Step 2: Models
- [ ] [Model 1]
- [ ] [Model 2]

### Step 3: Tool Layer — test each independently
- [ ] [Tool 1]
- [ ] [Tool 2]

### Step 4: Controllers
- [ ] [Controller 1]
- [ ] [Controller 2]

### Step 5: Views
- [ ] [View 1]
- [ ] [View 2]

### Step 6: Integration & Wiring
- [ ] Connect controllers to tools
- [ ] Connect controllers to views
- [ ] End-to-end test

### Step 7: UI (if applicable)
- [ ] [UI component]

### Step 8: Deploy
- [ ] Dockerfile
- [ ] Cloud deployment
- [ ] Scheduler / trigger
- [ ] Secrets management
- [ ] Logging + monitoring

### Step 9: Test & Validate
- [ ] [Acceptance criteria 1]
- [ ] [Acceptance criteria 2]

### Step 10: Feedback & Adjust
- [ ] Demo to stakeholders
- [ ] Adjust based on feedback
- [ ] Final validation

---

## Error Handling Rules

- [How to handle external API failures]
- [How to handle database failures]
- [How to handle missing data]
- [Never crash the entire run for one component]

---

## Pre-Sprint Blockers

| Blocker | Owner | Status |
|---|---|---|
| [Blocker 1] | [Name] | [Open/Requested/Resolved] |
| [Blocker 2] | [Name] | [Open/Requested/Resolved] |

---

## Effort & Timeline

| | Week 1 | Week 2 | Total |
|---|---|---|---|
| Dev | [hrs] | [hrs] | [hrs] |
| PM | [hrs] | [hrs] | [hrs] |
| Review | [hrs] | [hrs] | [hrs] |
| **TOTAL** | **[hrs]** | **[hrs]** | **[hrs]** |

---

*Last updated: [DATE]*
