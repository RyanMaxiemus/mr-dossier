import argparse
import os
from dotenv import load_dotenv

from loaders import DocumentProcessor
from analyzer import DossierBrain
from utils import clear_screen, resolve_and_validate_path, SecurityError, sanitize_for_prompt
from config import (
    CODE_PATTERN_FULL, CODE_PATTERN_FAST, DEFAULT_PERSONA,
    DEFAULT_MAX_FILES, DEFAULT_MAX_CHARS_PER_FILE,
    CACHE_ENABLED
)

# Load environment variables
load_dotenv()

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
        default=os.getenv("AUDITOR_PERSONA", DEFAULT_PERSONA),
        help="Auditor personality"
    )

    parser.add_argument("--fast",
        action="store_true",
        help="Only scan READMEs to save time")

    parser.add_argument("--redact",
        action="store_true",
        help="Enable additional LLM-based redaction of the final report")
    
    parser.add_argument("--max-files",
        type=int,
        default=int(os.getenv("MAX_FILES", DEFAULT_MAX_FILES)),
        help=f"Maximum number of files to analyze (default: {DEFAULT_MAX_FILES})"
    )
    
    parser.add_argument("--max-chars",
        type=int,
        default=int(os.getenv("MAX_CHARS_PER_FILE", DEFAULT_MAX_CHARS_PER_FILE)),
        help=f"Maximum characters per file to analyze (default: {DEFAULT_MAX_CHARS_PER_FILE})"
    )
    
    parser.add_argument("--no-cache",
        action="store_true",
        help="Disable file caching (enabled by default)"
    )
    
    parser.add_argument("--clear-cache",
        action="store_true",
        help="Clear the cache before running")

    args = parser.parse_args()

    clear_screen()
    print(f"🕵️‍♂️  Mr. Dossier is initiating investigation...")
    print(f"📂  Target Codebase: {args.code}")
    print(f"📄  Target Resume:   {args.resume}")
    print("-" * 50)

    # 2. Initialize Components
    # Handle cache clearing first
    if args.clear_cache:
        from cache import FileCache
        temp_cache = FileCache()
        temp_cache.clear()
    
    processor = DocumentProcessor(cache_enabled=not args.no_cache)
    brain = DossierBrain(
        model=args.model,
        persona=args.persona,
        max_files=args.max_files,
        max_chars_per_file=args.max_chars
    )

    # Enable verbose mode if set in environment
    verbose = os.getenv("VERBOSE_MODE", "False").lower() == "true"
    if verbose:
        print(f"🔧 Debug: Using model '{args.model}' with persona '{args.persona}'")

    # 3. Load and Parse Data
    try:
        print("🛠️  Parsing files (this might take a second if your code is a mess)...")

        # Determine glob pattern based on --fast flag
        code_pattern = CODE_PATTERN_FAST if args.fast else CODE_PATTERN_FULL

        # Load resume and code - path validation happens inside these methods
        resume_text = processor.load_resume(args.resume)
        code_docs = processor.load_code(args.code, pattern=code_pattern)

        if not code_docs:
            print("❌ Error: No code files found in the specified directory.")
            print(f"   Tried pattern: {code_pattern}")
            return

        # 4. Run the Audit
        print(f"🧠 Consulting {args.model}...")
        report = brain.audit(resume_text, code_docs)
        
        # Optional: Apply additional redaction if requested
        if args.redact:
            print("🔒 Applying additional redaction to report...")
            report = brain.generate_redacted_report(report)

        # 5. Output the Results
        print("\n" + "═" * 60)
        print("               THE DOSSIER FINAL REPORT")
        print("═" * 60)
        print(report)
        print("═" * 60)
        print("\n✅ Audit complete. Don't take it personally.")
        
        # Print cache stats in verbose mode
        if verbose:
            cache_stats = processor.cache.get_stats()
            print(f"\n📦 Cache: {cache_stats['entries']} entries, {cache_stats['size_bytes'] / 1024:.1f} KB")

    except FileNotFoundError as e:
        print(f"💥 File Error: {str(e)}")
    except NotADirectoryError as e:
        print(f"💥 Directory Error: {str(e)}")
    except SecurityError as e:
        print(f"🚫 Security Error: {str(e)}")
        print("   This operation was blocked for security reasons.")
    except Exception as e:
        print(f"💥 Incident Report: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        print("Check if Ollama is running (`ollama serve`) and the model is pulled.")

if __name__ == "__main__":
    main()
