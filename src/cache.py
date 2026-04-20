"""
Caching module for Mr. Dossier.

Provides file-based caching to avoid re-parsing unchanged files.
Uses SHA256 hashes of file content for cache keys.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from config import CACHE_DIR, CACHE_FORMAT, CACHE_ENABLED


class FileCache:
    """
    Simple file-based cache for storing parsed file metadata and content.
    
    Uses file hashes to detect changes and invalidate cache entries.
    """
    
    def __init__(self, cache_dir: Optional[str] = None, enabled: bool = True):
        """
        Initialize the file cache.
        
        Args:
            cache_dir: Directory to store cache files. Defaults to CACHE_DIR.
            enabled: Whether caching is enabled.
        """
        self.enabled = enabled and CACHE_ENABLED
        self.cache_dir = Path(cache_dir or CACHE_DIR)
        
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_hash(self, file_path: str) -> str:
        """
        Calculate SHA256 hash of file content.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            Hex digest of file hash.
        """
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""
    
    def _get_cache_path(self, file_hash: str) -> Path:
        """
        Get the cache file path for a given file hash.
        
        Args:
            file_hash: The file content hash.
            
        Returns:
            Path to cache file.
        """
        # Use first 2 chars of hash as subdirectory to avoid too many files in one dir
        subdir = self.cache_dir / file_hash[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        return subdir / f"{file_hash}.json"
    
    def get(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached data for a file if it exists and is valid.
        
        Args:
            file_path: Path to the source file.
            
        Returns:
            Cached data dict or None if not found/valid.
        """
        if not self.enabled:
            return None
        
        file_hash = self._get_file_hash(file_path)
        if not file_hash:
            return None
        
        cache_path = self._get_cache_path(file_hash)
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Verify the cached file hash matches current file
            if cached_data.get('file_hash') == file_hash:
                return cached_data
        except (json.JSONDecodeError, KeyError, IOError):
            # Invalid cache entry, remove it
            try:
                cache_path.unlink()
            except OSError:
                pass
        
        return None
    
    def set(self, file_path: str, content: str, metadata: Optional[Dict] = None):
        """
        Cache file content and metadata.
        
        Args:
            file_path: Path to the source file.
            content: The file content (already redacted if needed).
            metadata: Additional metadata to cache.
        """
        if not self.enabled:
            return
        
        file_hash = self._get_file_hash(file_path)
        if not file_hash:
            return
        
        cache_data = {
            'file_hash': file_hash,
            'file_path': file_path,
            'content': content,
            'metadata': metadata or {},
        }
        
        cache_path = self._get_cache_path(file_hash)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"   ⚠️  Failed to cache {file_path}: {e}")
    
    def clear(self):
        """Clear all cached entries."""
        if not self.cache_dir.exists():
            return
        
        import shutil
        try:
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            print("🗑️  Cache cleared successfully")
        except Exception as e:
            print(f"   ⚠️  Failed to clear cache: {e}")
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.
        
        Returns:
            Dict with 'entries' and 'size_bytes' keys.
        """
        if not self.cache_dir.exists():
            return {'entries': 0, 'size_bytes': 0}
        
        total_size = 0
        entry_count = 0
        
        for subdir in self.cache_dir.iterdir():
            if subdir.is_dir():
                for cache_file in subdir.glob('*.json'):
                    total_size += cache_file.stat().st_size
                    entry_count += 1
        
        return {'entries': entry_count, 'size_bytes': total_size}
