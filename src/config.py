"""
Configuration module for Mr. Dossier.

Centralizes all configuration constants, file extensions, and settings.
"""

# File extensions that are considered valid source code
VALID_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.go',
    '.cpp', '.rs', '.java', '.md'
}

# File patterns for different scan modes
CODE_PATTERN_FULL = "**/*.{py,js,ts,jsx,tsx,go,cpp,rs,java,md}"
CODE_PATTERN_FAST = "**/README.md"

# Directories to exclude from scanning
EXCLUDE_DIRS = {
    'node_modules', '.git', '__pycache__', 'venv', 'env', 'virtualenv',
    'dist', 'build', '.vscode', 'target', '.idea', 'coverage',
    '.pytest_cache', '.mypy_cache', '.tox', 'htmlcov', 'site-packages',
    'lib', 'lib64', 'include', 'bin', 'Scripts', 'pyvenv.cfg',
    '.venv', 'bower_components', 'vendor'
}

# LLM analysis limits
DEFAULT_MAX_FILES = 5
DEFAULT_MAX_CHARS_PER_FILE = 150
DEFAULT_RESUME_SNIPPET_LENGTH = 400
DEFAULT_CODE_SNIPPET_LENGTH = 200
DEFAULT_MAX_PROMPT_LENGTH = 10000

# Ollama configuration
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_TIMEOUT = 30

# UI/Output configuration
DEFAULT_PERSONA = "Technical Forensic Auditor"

# Cache configuration
CACHE_DIR = ".cache"
CACHE_ENABLED = True
CACHE_FORMAT = "json"  # or "jsonl"

# Batch processing configuration
DEFAULT_BATCH_SIZE = 100  # Process files in batches of this size
