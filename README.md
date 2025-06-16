# SmartDoc

SmartDoc is a CLI tool to automatically generate Markdown, HTML, and PDF API documentation for web frameworks like **FastAPI**, **Flask**, and **Django**.

---
## Installation

```bash
pip install smartdoc
```
(For testing with Test PyPI)

`pip install --index-url https://test.pypi.org/simple/ smartdoc
`

---
## Usage
Run this command inside your project directory.

### Example command:
```bash
smartdoc generate \
  --app your_app.main \
  --framework fastapi \
  --output api_docs.md \
  --html \
  --pdf

```
### For FastAPI:
```bash
smartdoc generate --app your_project.main --framework fastapi --output docs.md --html --pdf
```

### For Flask:
```bash
smartdoc generate --app your_project.main --framework flask --output docs.md --html --pdf
```

### For Django:
```bash
smartdoc generate --app your_project.main --framework django --django-settings your_project.settings --output docs.md --html --pdf
```

---
## CLI Options
| Option               | Description                                       |
| -------------------- | ------------------------------------------------- |
| `--app` / `-a`       | Python path to your app module                    |
| `--framework` / `-f` | One of `fastapi`, `flask`, `django`               |
| `--output` / `-o`    | Output Markdown filename (default: `api_docs.md`) |
| `--html`             | Generate HTML output                              |
| `--pdf`              | Generate PDF output                               |
| `--django-settings`  | Required for Django to specify settings module    |

---
## Output

Depending on options used:

`api_docs.md` — default markdown output

`api_docs.html` — HTML format (with `--html`)

`api_docs.pdf` — PDF format (with `--pdf`)

---
## Author
Built with 💻 by **Mohammad Safwan Athar** [@DevSaifOps](https://github.com/Dev-Saif-Ops)

---
## License


---


Use MIT license:

> `LICENSE` file:

```txt
MIT License

Copyright (c) 2025 Mohammad Safwan Athar aka DevSaifOps

Permission is hereby granted, free of charge, to any person obtaining a copy...

