import argparse
import os
import sys
from loaders import DocumentProcessor
from analyzer import DossierBrain

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # 1. Setup CLI Arguments
    parser = argparse.ArgumentParser(
        description="🕵️‍♂️ Mr. Dossier: The Local-First Code-to-Resume Auditor",
        epilog="Remember: The code doesn't lie, but your resume might."
    )

    parser.add_argument("--resume", required=True, help="Path to your PDF resume (e.g., ~/docs/resume.pdf)")
    parser.add_argument("--code", required=True, help="Path to your project directory (e.g., ~/dev/projects)")
    parser.add_argument("--model", default="llama3", help="Ollama model to use (default: llama3)")
    parser.add_argument("--persona", default="Technical Forensic Auditor", help="Auditor personality")
    parser.add_argument("--fast", action="store_true", help="Only scan READMEs to save time")

    args = parser.parse_args()

    clear_screen()
    print(f"🕵️‍♂️  Mr. Dossier is initiating investigation...")
    print(f"📂  Target Codebase: {args.code}")
    print(f"📄  Target Resume:   {args.resume}")
    print("-" * 50)

    # 2. Initialize Components
    # Note: Ensure you've created loaders.py with a DocumentProcessor class
    processor = DocumentProcessor()
    brain = DossierBrain(model=args.model, persona=args.persona)

    # 3. Load and Parse Data
    try:
        print("🛠️  Parsing files (this might take a second if your code is a mess)...")

        # Determine glob pattern based on --fast flag
        code_pattern = "**/README.md" if args.fast else "**/*.{py,js,ts,go,cpp,java,rs}"

        resume_text = processor.load_resume(args.resume)
        code_docs = processor.load_code(args.code, pattern=code_pattern)

        if not code_docs:
            print("❌ Error: No code files found in the specified directory.")
            return

        # 4. Run the Audit
        print(f"🧠 Consulting {args.model}...")
        report = brain.audit(resume_text, code_docs)

        # 5. Output the Results
        print("\n" + "═" * 60)
        print("               THE DOSSIER FINAL REPORT")
        print("═" * 60)
        print(report)
        print("═" * 60)
        print("\n✅ Audit complete. Don't take it personally.")

    except Exception as e:
        print(f"💥 Incident Report: {str(e)}")
        print("Check if Ollama is running (`ollama serve`) and the model is pulled.")

if __name__ == "__main__":
    main()
