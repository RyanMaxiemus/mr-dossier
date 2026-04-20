import os
from langchain_core.documents import Document
from utils import resolve_and_validate_path, SecurityError, SecretScanner
from config import VALID_EXTENSIONS, EXCLUDE_DIRS, CACHE_ENABLED
from cache import FileCache

class DocumentProcessor:
    def __init__(self, cache_enabled: bool = CACHE_ENABLED):
        # The "Blacklist" - We do NOT want to scan these
        self.exclude_dirs = EXCLUDE_DIRS
        # The "Whitelist" - Extensions we actually care about
        self.valid_extensions = VALID_EXTENSIONS
        # Initialize file cache
        self.cache = FileCache(enabled=cache_enabled)

    def load_resume(self, file_path):
        """
        Extracts text from a PDF resume.
        
        Args:
            file_path: Path to the PDF resume file.
            
        Returns:
            str: The extracted text content from the PDF.
            
        Raises:
            FileNotFoundError: If the resume file doesn't exist.
            SecurityError: If path traversal is detected.
        """
        # Validate path - don't allow traversal outside intended directories
        path = resolve_and_validate_path(file_path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Resume not found at {path}")
        
        if not os.path.isfile(path):
            raise ValueError(f"Resume path is not a file: {path}")

        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(path)
        pages = loader.load()
        # Combine all pages into one string for the auditor
        full_text = "\n".join([page.page_content for page in pages])
        return full_text

    def load_code(self, root_dir, pattern=None, scan_secrets=True):
        """
        A deep, recursive scanner that walks through every subfolder.
        Supports different patterns for fast vs full scans.
        
        Args:
            root_dir: Root directory to scan for code files.
            pattern: Glob pattern for file matching. If None, uses CODE_PATTERN_FULL.
                     Use CODE_PATTERN_FAST for README-only scanning.
            scan_secrets: If True, scan and redact potential secrets from file content.
            
        Returns:
            list: List of Document objects containing the scanned code.
            
        Raises:
            SecurityError: If path traversal is detected.
            NotADirectoryError: If the path is not a directory.
        """
        from config import CODE_PATTERN_FULL, CODE_PATTERN_FAST
        
        # Use default pattern if none specified
        if pattern is None:
            pattern = CODE_PATTERN_FULL
        
        root_path = resolve_and_validate_path(root_dir)
        
        if not os.path.isdir(root_path):
            raise NotADirectoryError(f"Code directory not found or is not a directory: {root_path}")
        
        documents = []
        secret_scanner = SecretScanner() if scan_secrets else None

        print(f"🚀 Deep Scanning: {root_path}")
        print(f"📋 Using pattern: {pattern}")
        print(f"🚫 Excluding directories: {', '.join(sorted(self.exclude_dirs))}")

        # Determine which extensions to scan based on pattern
        # Check if pattern indicates fast mode (README only)
        is_fast_mode = pattern == CODE_PATTERN_FAST or pattern.lower().endswith('readme.md')
        
        if is_fast_mode:
            # Fast mode - only README files
            target_files = {"readme.md", "readme", "readme.txt"}
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
                    
                    # Check cache first
                    cached = self.cache.get(file_path)
                    if cached:
                        content = cached['content']
                        print(f"   📦 Using cached: {file_path}")
                    else:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                # Scan for and redact secrets before caching and adding to documents
                                if secret_scanner and content.strip():
                                    content, found_secrets = secret_scanner.scan(content)
                                    if found_secrets:
                                        print(f"   ⚠️  Found {len(found_secrets)} potential secrets in {file_path}, redacting...")
                                
                                # Cache the processed content
                                self.cache.set(file_path, content)
                        except Exception as e:
                            # Skip files that can't be read (binaries, etc.)
                            continue
                    
                    # We wrap it in a LangChain Document object
                    if content.strip():
                        doc = Document(
                            page_content=content,
                            metadata={"source": file_path}
                        )
                        documents.append(doc)

        print(f"✅ Found {len(documents)} relevant files across your projects.")
        print(f"📊 Scanned {scanned_dirs} directories, skipped {skipped_dirs} excluded directories")
        return documents
