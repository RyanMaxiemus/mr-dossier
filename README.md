# 🕵️‍♂️ Mr. Dossier

> The local-first, AI-powered career strategist that audits your professional claims against your actual technical output to identify "Hidden Gems," "Skill Gaps," and your "Bullshit Rating."

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Tech: Python](https://img.shields.io/badge/Tech-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![AI: Ollama](https://img.shields.io/badge/AI-Ollama-000000?logo=ollama&logoColor=white)](https://ollama.com/)
[![Orchestration: LangChain](https://img.shields.io/badge/Orchestration-LangChain-22C55E?logo=langchain&logoColor=white)](https://www.langchain.com/)

---

## 🧐 What is this? (TL;DR)

**Mr. Dossier** is a command-line utility designed for the modern developer who values **privacy** and **technical honesty**. It solves the problem of resume inflation and underselling by performing a deep, evidence-based audit.

Unlike cloud-based resume tools, Mr. Dossier operates entirely on your local machine (Zero-Cloud principle). It uses a **Local Large Language Model (LLM)**, orchestrated by **LangChain**, to:

1.  **Crawl** your designated project directories (`/Dev`, `/Projects`).
2.  **Parse** your source code, extracting functions, classes, and technical context.
3.  **Compare** this technical output against the claims and keywords in your resume (PDF format).
4.  **Generate** a comprehensive report highlighting:
    - **Hidden Gems:** Skills and libraries you've used extensively but failed to mention.
    - **Skill Gaps:** Technologies you claim to know but have minimal code evidence for.
    - **Bullshit Rating:** A metric for the overall technical accuracy of your document.

The result is a resume that is not just optimized for keywords, but is **technically defensible** and grounded in your actual work.

## 🛠️ Tech Stack

This project is a Python-based command-line application that leverages the power of local LLMs for secure, private analysis.

| Component            | Technology    | Key Libraries/Frameworks                 |
| :------------------- | :------------ | :--------------------------------------- |
| **Language**         | Python 3.10+  | `argparse`, `os`, `dotenv`               |
| **AI Engine**        | Ollama        | Runs local LLMs (e.g., Llama 3, Mistral) |
| **Orchestration**    | LangChain     | `langchain-community`, `langchain-core`  |
| **Document Parsing** | PyPDF         | `pypdf`                                  |
| **Configuration**    | Python-dotenv | `python-dotenv`                          |

## 🚀 Quick Start

The following instructions are optimized for a Linux environment (Ubuntu/Debian) and assume you have Python 3.10+ installed.

### Prerequisites

1.  **Python 3.10+** and **pip**.
2.  **Ollama:** The local LLM runner. You must install Ollama and pull a model (e.g., `llama3`) before running the application.

### Step-by-step Installation

1.  **Install Ollama and Pull a Model**

    The application defaults to using `llama3`.

    ```bash
    # Install Ollama (see ollama.com for platform-specific instructions)
    # Then pull the default model:
    ollama pull llama3
    ```

2.  **Clone the Repository**

    ```bash
    git clone https://github.com/RyanMaxiemus/mr-dossier.git
    cd mr-dossier
    ```

3.  **Install Dependencies**

    Install all necessary Python packages using `pip`.

    ```bash
    pip install -r requirements.txt
    ```

### Usage

Run the main script, pointing it to your resume (PDF format) and your code directory.

```bash
python src/main.py --resume ~/Documents/MyResume.pdf --code ~/Development/Codebase
```

#### Advanced Options

You can customize the audit's tone and the LLM model used:

| Argument    | Description                                            | Example Value                          |
| :---------- | :----------------------------------------------------- | :------------------------------------- |
| `--model`   | Specify a different Ollama model to use for the audit. | `mistral`                              |
| `--persona` | Adjust the tone of the audit report.                   | `"Hardcore Tech Lead"`, `"HR Manager"` |
| `--output`  | Save the suggestions directly to a file.               | `./audit_report.md`                    |

## 🤝 Contributing

Found a bug, or have an idea for a new feature? We welcome all contributions, from code to documentation!

1.  **Open an Issue:** Before starting any major work, please open an issue to discuss the bug or feature you're working on. This helps prevent duplicate effort and ensures alignment with the project's direction.
2.  **Fork and Branch:** Fork the repository and create a new branch for your contribution (e.g., `feat/add-json-output` or `fix/pypdf-bug`).
3.  **Code and Commit:** Write clean, well-documented Python code. Commit messages should be descriptive and follow a conventional format (e.g., `feat: add JSON output option`).
4.  **Submit a PR:** Submit a Pull Request against the `main` branch. We aim to review all contributions quickly.

Let's work together to make Mr. Dossier the gold standard for private, code-backed career auditing.

## ⚖️ License

Distributed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.

---

_Created by Ryan Maxie — Built to turn code into careers._
