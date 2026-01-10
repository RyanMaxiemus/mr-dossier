import os
from langchain_community.llms import Ollama

class DossierBrain:
    def __init__(self, model="llama3", persona="Technical Forensic Auditor"):
        """
Initialize Mr. Dossier's brain.
Persona defaults to a skeptical auditor for maximum honesty.
"""
        self.llm = Ollama(model=model)
        self.persona = persona

    def _summarize_codebase(self, code_docs):
        """
Pass 1: Catalog the actual technical evidence found in the files.
"""
        evidence_text = "\n".join([doc.page_content[:500] for doc in code_docs]) # Limit per file

        summary_prompt = f"""
Analyze the following code snippets and READMEs.
Create a 'Technical Evidence Report' listing:
1. Languages and Frameworks actually used.
2. Complexity of implementations (e.g., 'Simple CRUD' vs 'Distributed Systems').
3. Recurrent patterns or bad habits.

CODE DATA:
{evidence_text}
"""
        return self.llm.invoke(summary_prompt)

    def audit(self, resume_text, code_docs):
        """
Pass 2: Compare the resume claims against the code evidence.
"""
        print("🔍 Step 1: Cataloging your code evidence...")
        code_summary = self._summarize_codebase(code_docs)

        print("⚖️  Step 2: Comparing claims to reality...")

        audit_prompt = f"""
SYSTEM: You are {self.persona}. You are brutally honest, analytical, and encouraging
but won't tolerate exaggeration.

CONTEXT:
You have a candidate's RESUME and a SUMMARY OF THEIR ACTUAL CODE.

RESUME:
{resume_text}

ACTUAL CODE EVIDENCE:
{code_summary}

TASK:
1. Assign a 'BULLSHIT RATING' (1-10).
    - 1: Extremely humble/Under-sold.
    - 5: Perfectly accurate.
    - 10: Complete hallucination/Total fraud.
2. Identify 'THE BIGGEST LIE': The claim with the least evidence in the code.
3. Identify 'THE HIDDEN GEM': A high-value skill found in code but missing from the resume.
4. SUGGESTED UPDATES: Provide 3 rewritten bullet points in 'Action-Context-Result' format.

OUTPUT FORMAT: Return as Markdown.
"""

        return self.llm.invoke(audit_prompt)

    def generate_redacted_report(self, report_text):
        """
Optional: A final pass to ensure no sensitive info like keys leaked into the report.
"""
        redact_prompt = f"Redact any potential API keys, passwords, or private emails from this text:\n\n{report_text}"
        return self.llm.invoke(redact_prompt)
