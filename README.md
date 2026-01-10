# 🕵️‍♂️ Mr. Dossier

**"Because your resume is lying to you, but your code isn't."**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Local-First](https://img.shields.io/badge/Privacy-100%25_Local-brightgreen)](#)
[![LLM](https://img.shields.io/badge/Powered_By-Ollama-blue)](https://ollama.com)

**Mr. Dossier** is a local-first, AI-powered career strategist that audits your professional claims against your actual technical output. It crawls your local project directories, analyzes your source code, and compares it to your resume to identify "Hidden Gems," "Skill Gaps," and your "Bullshit Rating."

## 🚀 Why Mr. Dossier?

Most developers undersell their work or forget the libraries they mastered three projects ago. Traditional "Resume Optimizers" are cloud-based privacy nightmares.

**Mr. Dossier** fixes this by:

- **Running 100% Locally:** Your resume and private source code never leave your machine.
- **Evidence-Based Writing:** It generates bullet points based on actual functions, classes, and commits it finds in your `/Dev` folders.
- **Brutal Honesty:** It doesn't just "fix" your resume; it audits it for technical accuracy.

## 🛠️ Tech Stack

- **Engine:** [Ollama](https://ollama.com/) (Running Llama 3 / Mistral)
- **Orchestration:** LangChain
- **Parsing:** PyPDF & Python Directory Loaders
- **Environment:** Python 3.10+

## 📦 Installation

1. **Install Ollama** and pull a model:

   ```bash
   ollama pull llama3
   ```

2. **Clone the Dossier:**

   ```bash
   git clone [https://github.com/RyanMaxiemus/mr-dossier.git](https://github.com/RyanMaxiemus/mr-dossier.git)
   cd mr-dossier

   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt

   ```

## 🕹️ Usage

Point Mr. Dossier at your career documents and your code base:

```bash
python src/main.py --resume ~/Docs/Resume.pdf --code ~/Dev/Projects

```

### Advanced Options

- `--persona "Hardcore Tech Lead"`: For a more critical, "code-review" style audit.
- `--persona "HR Manager"`: For a focus on buzzwords and readability.
- `--output ./updates.md`: Save the suggestions directly to a file.

## 🧠 Features to Come

- [ ] **Commit History Analysis:** Scanning Git logs to find consistency and growth.
- [ ] **LinkedIn Sync:** Comparing your online profile to your local resume.
- [ ] **Skill Graphing:** Visualizing your tech stack based on file frequency.

## 🛡️ Privacy

Mr. Dossier is built on the principle of **Zero-Cloud**. No telemetry, no training on your data, no API keys required. It's just you, your code, and the weights running on your GPU.

## ⚖️ License

Distributed under the MIT License. See [LICENSE](/LICENSE) for more information.

---

_Created by Ryan Maxie — Built to turn code into careers._
