import os
from langchain_community.llms import Ollama
from config import (
    DEFAULT_MAX_FILES,
    DEFAULT_MAX_CHARS_PER_FILE,
    DEFAULT_RESUME_SNIPPET_LENGTH,
    DEFAULT_CODE_SNIPPET_LENGTH,
    DEFAULT_TIMEOUT,
    DEFAULT_OLLAMA_URL,
)

class DossierBrain:
    def __init__(
        self,
        model="llama3",
        persona="Technical Forensic Auditor",
        max_files: int = DEFAULT_MAX_FILES,
        max_chars_per_file: int = DEFAULT_MAX_CHARS_PER_FILE
    ):
        """
        Initialize Mr. Dossier's brain.
        Persona defaults to a skeptical auditor for maximum honesty.
        
        Args:
            model: Ollama model name to use.
            persona: Auditor personality/persona.
            max_files: Maximum number of files to analyze.
            max_chars_per_file: Maximum characters per file to analyze.
        """
        try:
            # Add timeout and base_url for better connection handling
            self.llm = Ollama(
                model=model,
                timeout=DEFAULT_TIMEOUT,
                base_url=DEFAULT_OLLAMA_URL
            )
            self.persona = persona
            self.max_files = max_files
            self.max_chars_per_file = max_chars_per_file
            print(f"🤖 Connected to Ollama model: {model}")
            print(f"🎭 Using persona: {persona}")
            print(f"📊 Analysis limits: {max_files} files, {max_chars_per_file} chars/file")
        except Exception as e:
            print(f"❌ Failed to connect to Ollama: {e}")
            print("Make sure Ollama is running with: ollama serve")
            print(f"And the model is available: ollama pull {model}")
            raise

    def _summarize_codebase(self, code_docs):
        """
        Pass 1: Catalog the actual technical evidence found in the files.
        """
        # Import here to avoid circular imports
        from utils import sanitize_for_prompt
        
        # Use instance limits (configurable via CLI)
        max_files = self.max_files
        max_chars_per_file = self.max_chars_per_file

        limited_docs = code_docs[:max_files]

        # Create a more concise summary
        file_summaries = []
        for doc in limited_docs:
            source = doc.metadata.get('source', 'unknown')
            filename = source.split('/')[-1] if '/' in source else source
            content_preview = doc.page_content[:max_chars_per_file].replace('\n', ' ')
            file_summaries.append(f"{filename}: {content_preview}")

        evidence_text = "\n".join(file_summaries)
        
        # Sanitize before including in prompt
        evidence_text = sanitize_for_prompt(evidence_text)

        print(f"📊 Analyzing {len(limited_docs)} files (limited from {len(code_docs)} total)")
        print(f"📏 Total characters being sent: {len(evidence_text)}")

        # Much shorter, more focused prompt
        summary_prompt = f"""As a {self.persona}, analyze these code files and list:
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
        # Import here to avoid circular imports
        from utils import sanitize_for_prompt
        
        print("🔍 Step 1: Cataloging your code evidence...")
        code_summary = self._summarize_codebase(code_docs)

        if "Error:" in code_summary:
            return code_summary

        print("⚖️  Step 2: Comparing claims to reality...")

        # Make the audit much simpler and shorter
        # Sanitize inputs before including in prompt
        resume_snippet = sanitize_for_prompt(resume_text[:DEFAULT_RESUME_SNIPPET_LENGTH])
        code_snippet = sanitize_for_prompt(code_summary[:DEFAULT_CODE_SNIPPET_LENGTH]) if len(code_summary) > DEFAULT_CODE_SNIPPET_LENGTH else sanitize_for_prompt(code_summary)

        print(f"📏 Resume chars: {len(resume_snippet)}, Code summary chars: {len(code_snippet)}")

        audit_prompt = f"""As a {self.persona}, compare resume to code. Rate accuracy 1-10.

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
        Uses a lightweight local check first before calling LLM.
        """
        from utils import SecretScanner
        
        # First, use local secret scanner
        scanner = SecretScanner()
        redacted_local, found = scanner.scan(report_text)
        
        # If secrets were found, also use LLM for additional redaction
        if found:
            print(f"   🛡️  Redacting {len(found)} potential secrets from report...")
            redact_prompt = f"""As a {self.persona}, review this report and redact any potential API keys, passwords, private emails, or other sensitive information:

{report_text}

Return only the redacted report."""
            try:
                return self.llm.invoke(redact_prompt)
            except Exception as e:
                print(f"   ⚠️  LLM redaction failed, using local redaction: {e}")
                return redacted_local
        
        return report_text
