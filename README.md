# SmartDoc CLI

**SmartDoc CLI** is a command-line tool that automatically generates Markdown, HTML, and PDF API documentation for web frameworks like **FastAPI**, **Flask**, and **Django**.

---
## Installation

```bash
pip install smartdoc-cli
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
## ModuleNotFoundError Fix
You may often encounter the following error when using SmartDoc:

```bash
ModuleNotFoundError: No module named 'apps'
```
### Solution:
Set the PYTHONPATH to the current directory (.) or to your project folder:

```bash
# For Windows PowerShell
$env:PYTHONPATH="."
```
Or if your project is in a specific folder:

```bash
$env:PYTHONPATH="project_folder"
```
Then run the smartdoc generate command as usual.

### Example:
```bash
$env:PYTHONPATH="."
smartdoc generate --app main --framework fastapi --output api_docs.md --html --pdf
```
### Tip: This sets your base import path, so Python knows where to find your app module.

## Troubleshooting SmartDoc

---
|  Checkpoint       | Description                                          |
| ----------------- |------------------------------------------------------|
| PYTHONPATH set?   | Point to folder where `apps/`, `main.py`, etc. exist |
| Module correct?   | Use `--app main` not full path like `project.main`   |
| Inside virtualenv? | Make sure `.venv` is activated                       |
| Imports relative? | Use `from apps...`, not `project.apps...`            |

### Tip: Reusable PowerShell Script
If you want to avoid setting PYTHONPATH every time, create a PowerShell script run_smartdoc.ps1:
```bash
$env:PYTHONPATH="project"
smartdoc generate --app main --framework fastapi --output api_docs.md --html --pdf
```
---
## smartdoc.json – Custom Configuration File
Place this in your root directory (same level as .venv, your_projects, etc.):

### For FastApi
```bash
{
  "app": "main",
  "framework": "fastapi",
  "output": "api_docs.md",
  "html": true,
  "pdf": true,
  "pythonpath": "project_folder"
}

```

### For Django
```bash
{
  "app": "project_name.urls",
  "framework": "django",
  "output": "api_docs.md",
  "html": true,
  "pdf": true,
  "pythonpath": "project_name",
  "django-settings": "project_name.settings"
}
```

### For Flask
```bash
{
  "app": "app",  // path to your Flask app file (e.g. app.py without .py)
  "framework": "flask",
  "output": "api_docs.md",
  "html": true,
  "pdf": true,
  "pythonpath": "."
}
```
### 1. Then use a custom script to run it:
Here’s a reusable Python script (run_smartdoc.py) to load from this config:

### `run_smartdoc.py`
```python
import os
import subprocess
import json

with open("smartdoc.json") as f:
    config = json.load(f)

os.environ["PYTHONPATH"] = config["pythonpath"]

cmd = [
    "smartdoc",
    "generate",
    "--app", config["app"],
    "--framework", config["framework"],
    "--output", config["output"]
]

if config.get("html"):
    cmd.append("--html")
if config.get("pdf"):
    cmd.append("--pdf")

subprocess.run(cmd)
```
Run it with:
`python run_smartdoc.py
`

### Note: Additional step for Django and Flask:
#### 1. Django
```text
In Python Script you need to set the DJANGO_SETTINGS_MODULE environment variable.
```
Update run_smartdoc.py like this:

```python
os.environ["DJANGO_SETTINGS_MODULE"] = config.get("django-settings", "")
```

#### 2. Flask
```text
In flask you only have to give the path of .py file which contains `Flask(__name__)` in the place of app.
```
---
### 2. Makefile (For Mac/Linux or Git Bash)
If you're on Linux/macOS or using Git Bash on Windows, you can use a Makefile.
### `Makefile`
```bash
PYTHONPATH=your-path

generate-docs:
	PYTHONPATH=$(PYTHONPATH) smartdoc generate \
		--app main \
		--framework fastapi \
		--output api_docs.md \
		--html \
		--pdf
```
Run it with:
`make generate-docs
`
#### NOTE: Make the necessary changes for Django and Flask
---
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

This project is licensed under the MIT License.

---

```txt
MIT License

Copyright (c) 2025 Mohammad Safwan Athar aka DevSaifOps

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
