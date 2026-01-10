import argparse
import os
import sys
from loaders import DocumentProcessor
from analyzer import DossierBrain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def clear_screen():
    """Clear the terminal screen in a cross-platform way."""
    os.system('clear' if os.name != 'nt' else 'cls')

def main():
    # 1. Setup CLI Arguments
    parser = argparse.ArgumentParser(
        description="🕵️‍♂️ Mr. Dossier: The Local-First Code-to-Resume Auditor",
        epilog="Remember: The code doesn't lie, but your resume might."
    )

    parser.add_argument("--resume",
        required=True,
        help="Path to your PDF resume (e.g., ~/docs/resume.pdf)")

    parser.add_argument("--code",
        required=True,
        help="Path to your project directory (e.g., ~/dev/projects)")

    parser.add_argument(
        "--model",
        default=os.getenv("DEFAULT_MODEL", "llama3"),
        help="Ollama model to use"
    )

    parser.add_argument(
        "--persona",
        default=os.getenv("AUDITOR_PERSONA", "Forensic Auditor"),
        help="Auditor personality"
    )

    parser.add_argument("--fast",
        action="store_true",
        help="Only scan READMEs to save time")

    args = parser.parse_args()

    clear_screen()
    print(f"🕵️‍♂️  Mr. Dossier is initiating investigation...")
    print(f"📂  Target Codebase: {args.code}")
    print(f"📄  Target Resume:   {args.resume}")
    print("-" * 50)

    # 2. Initialize Components
    processor = DocumentProcessor()
    brain = DossierBrain(model=args.model, persona=args.persona)

    # Enable verbose mode if set in environment
    verbose = os.getenv("VERBOSE_MODE", "False").lower() == "true"
    if verbose:
        print(f"🔧 Debug: Using model '{args.model}' with persona '{args.persona}'")

    # 3. Load and Parse Data
    try:
        # Validate paths exist before processing
        if not os.path.exists(os.path.expanduser(args.resume)):
            print(f"❌ Error: Resume file not found at {args.resume}")
            return

        if not os.path.isdir(os.path.expanduser(args.code)):
            print(f"❌ Error: Code directory not found at {args.code}")
            return

        print("🛠️  Parsing files (this might take a second if your code is a mess)...")

        # Determine glob pattern based on --fast flag
        code_pattern = "**/README.md" if args.fast else "**/*.{py,js,ts,go,cpp,java,rs}"

        resume_text = processor.load_resume(args.resume)
        code_docs = processor.load_code(args.code, pattern=code_pattern)

        if not code_docs:
            print("❌ Error: No code files found in the specified directory.")
            print(f"   Tried pattern: {code_pattern}")
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

    except FileNotFoundError as e:
        print(f"💥 File Error: {str(e)}")
    except NotADirectoryError as e:
        print(f"💥 Directory Error: {str(e)}")
    except Exception as e:
        print(f"💥 Incident Report: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        print("Check if Ollama is running (`ollama serve`) and the model is pulled.")

if __name__ == "__main__":
    main()
