# [PROJECT_NAME]

[PROJECT_DESCRIPTION]

---

## Getting Started

### 1. Clone and set up environment
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
# source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Fill in .env with real values — never commit this file
```

### 3. Run the app
```bash
python app.py
```

---

## Project Structure

```
[PROJECT_NAME]/
├── models/          # Data structures, DB interactions
├── views/           # Output formatting, templates
├── controllers/     # Business logic, orchestration
├── tests/           # All test files (pytest)
├── app.py           # Entry point
├── CLAUDE.md        # AI coding standards (auto-loaded by Claude Code)
├── pyproject.toml   # Python project config + Black settings
├── .prettierrc      # JS formatting config
├── .env.example     # Environment variable template
└── requirements.txt # Python dependencies
```

---

## Standards

This project follows Emplicit engineering standards defined in `CLAUDE.md`.
All contributors must read `CLAUDE.md` before writing code.

---

## Running Tests
```bash
pytest
```
