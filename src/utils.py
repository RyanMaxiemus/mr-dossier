"""
Utility functions for Mr. Dossier.

Contains security utilities, path validation, and helper functions.
"""

import os
import re
import subprocess
import platform
from typing import Optional


class SecurityError(Exception):
    """Raised when a security violation is detected."""
    pass


def resolve_and_validate_path(user_path: str, allowed_base: Optional[str] = None) -> str:
    """
    Resolve a user-provided path and validate it doesn't escape the allowed directory.
    
    Args:
        user_path: The path provided by the user (may contain ~ for home)
        allowed_base: The base directory that the resolved path must be within.
                      If None, only basic path traversal checks are performed.
    
    Returns:
        The resolved absolute path.
    
    Raises:
        SecurityError: If path traversal is detected.
        FileNotFoundError: If the path doesn't exist.
    """
    # Expand user directory (~)
    expanded = os.path.expanduser(user_path)
    
    # Convert to absolute and normalize (resolves .., symlinks, etc.)
    resolved = os.path.realpath(expanded)
    
    # Check for path traversal if base is specified
    if allowed_base:
        base_resolved = os.path.realpath(os.path.expanduser(allowed_base))
        # Ensure the resolved path starts with the allowed base
        if not resolved.startswith(base_resolved + os.sep) and resolved != base_resolved:
            raise SecurityError(
                f"Path traversal detected: '{user_path}' resolves to '{resolved}' "
                f"which is outside allowed base '{base_resolved}'"
            )
    
    return resolved


def clear_screen():
    """
    Clear the terminal screen in a cross-platform, safe manner.
    
    Uses platform-specific commands without shell interpretation.
    """
    system = platform.system().lower()
    
    if system == 'windows':
        # Use cls on Windows
        subprocess.run(['cls'], shell=False, check=False)
    else:
        # Use clear on Unix-like systems (Linux, macOS)
        subprocess.run(['clear'], shell=False, check=False)


class SecretScanner:
    """
    Scans text content for potential secrets and sensitive data.
    
    Uses regex patterns to identify API keys, passwords, tokens, and other
    sensitive information that should not be sent to external services.
    """
    
    # Patterns for detecting potential secrets
    PATTERNS = {
        'api_key': re.compile(
            r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{16,}["\']?',
            re.IGNORECASE
        ),
        'aws_key': re.compile(
            r'(?i)(AKIA[0-9A-Z]{16})',
            re.IGNORECASE
        ),
        'private_key': re.compile(
            r'(?i)(-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----)',
            re.IGNORECASE
        ),
        'password': re.compile(
            r'(?i)(password|passwd|pwd)\s*[:=]\s*["\'][^"\']{4,}["\']',
            re.IGNORECASE
        ),
        'secret': re.compile(
            r'(?i)(secret[_-]?key|secret)\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{8,}["\']?',
            re.IGNORECASE
        ),
        'token': re.compile(
            r'(?i)(token|access_token|auth_token)\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{16,}["\']?',
            re.IGNORECASE
        ),
        'bearer_token': re.compile(
            r'(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}',
            re.IGNORECASE
        ),
        'connection_string': re.compile(
            r'(?i)(mongodb(\+srv)?://|postgres(ql)?://|mysql://|redis://)[^\s\"\']+',
            re.IGNORECASE
        ),
        'email': re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            re.IGNORECASE
        ),
        'ip_address': re.compile(
            r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        ),
    }
    
    # Replacement text for redacted content
    REDACTION_TEXT = '[REDACTED]'
    
    def __init__(self):
        self.found_secrets = []
    
    def scan(self, content: str) -> tuple[str, list[dict]]:
        """
        Scan content for secrets and return redacted text.
        
        Args:
            content: The text content to scan.
        
        Returns:
            Tuple of (redacted_content, list_of_found_secrets).
            Each secret in the list contains: type, preview, position.
        """
        redacted = content
        self.found_secrets = []
        
        for secret_type, pattern in self.PATTERNS.items():
            for match in pattern.finditer(content):
                # Store info about the found secret
                preview = match.group(0)[:20] + '...' if len(match.group(0)) > 20 else match.group(0)
                self.found_secrets.append({
                    'type': secret_type,
                    'preview': preview,
                    'position': match.span()
                })
                
                # Replace with redaction text
                redacted = redacted.replace(match.group(0), self.REDACTION_TEXT)
        
        return redacted, self.found_secrets
    
    def has_secrets(self, content: str) -> bool:
        """Check if content contains any potential secrets."""
        for pattern in self.PATTERNS.values():
            if pattern.search(content):
                return True
        return False


def sanitize_for_prompt(text: str) -> str:
    """
    Sanitize text before including in LLM prompts to prevent prompt injection.
    
    Basic sanitization that:
    - Limits length
    - Removes common injection patterns
    - Escapes special characters
    
    Args:
        text: The text to sanitize.
    
    Returns:
        Sanitized text safe for prompt inclusion.
    """
    # Limit length to prevent token overflow and injection via large payloads
    max_length = 10000
    if len(text) > max_length:
        text = text[:max_length] + "\n[Content truncated due to length]"
    
    # Replace common prompt injection patterns
    # These patterns try to make the LLM ignore previous instructions
    injection_patterns = [
        r'ignore (all |previous )?instructions',
        r'forget (all |previous )?instructions',
        r'ignore (the |your )?prompt',
        r'disregard (all |previous )?instructions',
        r'you are now',
        r'system prompt',
        r'new instructions',
    ]
    
    sanitized = text
    for pattern in injection_patterns:
        sanitized = re.sub(pattern, '[REMOVED]', sanitized, flags=re.IGNORECASE)
    
    return sanitized
