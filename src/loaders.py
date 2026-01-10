import os
from langchain_core.documents import Document

class DocumentProcessor:
    def __init__(self):
        # The "Blacklist" - We do NOT want to scan these
        self.exclude_dirs = {
            'node_modules', '.git', '__pycache__', 'venv', 'env', 'virtualenv',
            'dist', 'build', '.vscode', 'target', '.idea', 'coverage',
            '.pytest_cache', '.mypy_cache', '.tox', 'htmlcov', 'site-packages',
            'lib', 'lib64', 'include', 'bin', 'Scripts', 'pyvenv.cfg',
            '.venv', 'node_modules', 'bower_components', 'vendor'
        }
        # The "Whitelist" - Extensions we actually care about
        self.valid_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.go',
            '.cpp', '.rs', '.java', '.md'
        }

    def load_resume(self, file_path):
        """
        Extracts text from a PDF resume.
        """
        path = os.path.expanduser(file_path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Resume not found at {path}")

        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(path)
        pages = loader.load()
        # Combine all pages into one string for the auditor
        full_text = "\n".join([page.page_content for page in pages])
        return full_text

    def load_code(self, root_dir, pattern="**/*.{py,js,ts,jsx,tsx,go,cpp,rs,java,md}"):
        """
        A deep, recursive scanner that walks through every subfolder.
        Supports different patterns for fast vs full scans.
        """
        root_path = os.path.expanduser(root_dir)
        documents = []

        print(f"🚀 Deep Scanning: {root_path}")
        print(f"📋 Using pattern: {pattern}")
        print(f"🚫 Excluding directories: {', '.join(sorted(self.exclude_dirs))}")

        # Determine which extensions to scan based on pattern
        if "README.md" in pattern:
            # Fast mode - only README files
            target_files = {"readme.md"}
            scan_all_code = False
            print("⚡ Fast mode: Only scanning README files")
        else:
            # Full mode - all code files
            target_files = set()
            scan_all_code = True
            print(f"🔍 Full mode: Scanning extensions: {', '.join(sorted(self.valid_extensions))}")

        scanned_dirs = 0
        skipped_dirs = 0

        for root, dirs, files in os.walk(root_path):
            # 1. Prune excluded directories in-place so os.walk doesn't enter them
            # This is the critical fix - we need to modify dirs in-place
            original_dirs = dirs[:]
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs and not d.startswith('.')]

            excluded_this_level = set(original_dirs) - set(dirs)
            if excluded_this_level:
                skipped_dirs += len(excluded_this_level)

            # Additional check: skip if current directory path contains excluded dirs
            current_path = os.path.relpath(root, root_path)
            path_parts = current_path.split(os.sep)
            if any(part in self.exclude_dirs or part.startswith('.') for part in path_parts if part != '.'):
                continue

            scanned_dirs += 1

            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    continue

                file_lower = file.lower()
                ext = os.path.splitext(file)[1].lower()

                # 2. Check if we should process this file
                should_process = False
                if scan_all_code and ext in self.valid_extensions:
                    should_process = True
                elif not scan_all_code and file_lower in target_files:
                    should_process = True

                if should_process:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            # We wrap it in a LangChain Document object
                            if content.strip():
                                doc = Document(
                                    page_content=content,
                                    metadata={"source": file_path}
                                )
                                documents.append(doc)
                    except Exception as e:
                        # Skip files that can't be read (binaries, etc.)
                        continue

        print(f"✅ Found {len(documents)} relevant files across your projects.")
        print(f"📊 Scanned {scanned_dirs} directories, skipped {skipped_dirs} excluded directories")
        return documents
