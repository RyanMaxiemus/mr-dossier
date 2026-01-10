import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader

class DocumentProcessor:
    def __init__(self):
        # List of folders we definitely want to ignore
        self.exclude_dirs = [
            'node_modules', '.git', '__pycache__', 'venv',
            'env', 'dist', 'build', '.vscode', 'target'
        ]

    def load_resume(self, file_path):
        """
        Extracts text from a PDF resume.
        """
        path = os.path.expanduser(file_path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Resume not found at {path}")

        loader = PyPDFLoader(path)
        pages = loader.load()
        # Combine all pages into one string for the auditor
        full_text = "\n".join([page.page_content for page in pages])
        return full_text

    def load_code(self, dir_path, pattern="**/*.py"):
        """
        Crawls a directory and loads code files while skipping the junk.
        """
        path = os.path.expanduser(dir_path)
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Code directory not found at {path}")

        print(f"📂 Filtering out noise ({', '.join(self.exclude_dirs)})...")

        # We use a custom loader logic to ensure we don't crash on binary files
        loader = DirectoryLoader(
            path,
            glob=pattern,
            recursive=True,
            show_progress=True,
            exclude=self.exclude_dirs,
            loader_cls=TextLoader,
            loader_kwargs={'autodetect_encoding': True}
        )

        try:
            docs = loader.load()
            return docs
        except Exception as e:
            print(f"⚠️ Warning: Some files couldn't be read: {e}")
            return []
