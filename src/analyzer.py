import os
from langchain_community.llms import Ollama

class DossierBrain:
    def __init__(self, model="llama3", persona="Technical Forensic Auditor"):
        """
Initialize Mr. Dossier's brain.
Persona defaults to a skeptical auditor for maximum honesty.
"""
        try:
            # Add timeout and base_url for better connection handling
            self.llm = Ollama(
                model=model,
                timeout=30,  # Reduce timeout to 30 seconds
                base_url="http://localhost:11434"  # Default Ollama URL
            )
            self.persona = persona
            print(f"🤖 Connected to Ollama model: {model}")
        except Exception as e:
            print(f"❌ Failed to connect to Ollama: {e}")
            print("Make sure Ollama is running with: ollama serve")
            print(f"And the model is available: ollama pull {model}")
            raise

    def _summarize_codebase(self, code_docs):
        """
Pass 1: Catalog the actual technical evidence found in the files.
"""
        # Much more aggressive limits to prevent timeout
        max_files = 5  # Reduce to just 5 files
        max_chars_per_file = 150  # Very small chunks

        limited_docs = code_docs[:max_files]

        # Create a more concise summary
        file_summaries = []
        for doc in limited_docs:
            source = doc.metadata.get('source', 'unknown')
            filename = source.split('/')[-1] if '/' in source else source
            content_preview = doc.page_content[:max_chars_per_file].replace('\n', ' ')
            file_summaries.append(f"{filename}: {content_preview}")

        evidence_text = "\n".join(file_summaries)

        print(f"📊 Analyzing {len(limited_docs)} files (limited from {len(code_docs)} total)")
        print(f"📏 Total characters being sent: {len(evidence_text)}")

        # Much shorter, more focused prompt
        summary_prompt = f"""Analyze these code files and list:
1. Programming languages used
2. Key frameworks/libraries
3. Project complexity level

Files:
{evidence_text}

Keep response under 200 words."""

        try:
            print("⏳ Sending request to Ollama...")
            response = self.llm.invoke(summary_prompt)
            print("✅ Received response from Ollama")
            return response
        except Exception as e:
            print(f"❌ Error during code analysis: {e}")
            return "Error: Could not analyze codebase. Check Ollama connection."

    def audit(self, resume_text, code_docs):
        """
Pass 2: Compare the resume claims against the code evidence.
"""
        print("🔍 Step 1: Cataloging your code evidence...")
        code_summary = self._summarize_codebase(code_docs)

        if "Error:" in code_summary:
            return code_summary

        print("⚖️  Step 2: Comparing claims to reality...")

        # Make the audit much simpler and shorter
        resume_snippet = resume_text[:400]  # Only first 400 chars of resume
        code_snippet = code_summary[:200] if len(code_summary) > 200 else code_summary  # Limit code summary too

        print(f"📏 Resume chars: {len(resume_snippet)}, Code summary chars: {len(code_snippet)}")

        audit_prompt = f"""Compare resume to code. Rate accuracy 1-10.

RESUME: {resume_snippet}

CODE: {code_snippet}

Give: Rating, one lie, one hidden skill. Max 100 words."""

        try:
            print("⏳ Sending audit request to Ollama...")
            response = self.llm.invoke(audit_prompt)
            print("✅ Received audit response from Ollama")
            return response
        except Exception as e:
            print(f"❌ Error during audit: {e}")
            return f"Error: Could not complete audit. {str(e)}"

    def generate_redacted_report(self, report_text):
        """
Optional: A final pass to ensure no sensitive info like keys leaked into the report.
"""
        redact_prompt = f"Redact any potential API keys, passwords, or private emails from this text:\n\n{report_text}"
        return self.llm.invoke(redact_prompt)
