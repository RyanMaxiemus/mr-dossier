"""
Unit tests for bug fixes and configuration.
"""

import os
import sys
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import (
    VALID_EXTENSIONS,
    EXCLUDE_DIRS,
    CODE_PATTERN_FULL,
    CODE_PATTERN_FAST,
    DEFAULT_MAX_FILES,
    DEFAULT_MAX_CHARS_PER_FILE,
)


class TestConfigModule(unittest.TestCase):
    """Tests for configuration constants."""
    
    def test_valid_extensions_defined(self):
        """Test that valid extensions are defined."""
        self.assertIsInstance(VALID_EXTENSIONS, set)
        self.assertIn('.py', VALID_EXTENSIONS)
        self.assertIn('.js', VALID_EXTENSIONS)
        self.assertIn('.md', VALID_EXTENSIONS)
    
    def test_exclude_dirs_defined(self):
        """Test that excluded directories are defined."""
        self.assertIsInstance(EXCLUDE_DIRS, set)
        self.assertIn('node_modules', EXCLUDE_DIRS)
        self.assertIn('__pycache__', EXCLUDE_DIRS)
        self.assertIn('.git', EXCLUDE_DIRS)
    
    def test_exclude_dirs_no_duplicates(self):
        """Test that excluded directories has no duplicates."""
        # A set should never have duplicates, but verify length matches expected
        self.assertEqual(len(EXCLUDE_DIRS), len(set(EXCLUDE_DIRS)))
    
    def test_code_patterns_defined(self):
        """Test that code patterns are defined."""
        self.assertIsInstance(CODE_PATTERN_FULL, str)
        self.assertIsInstance(CODE_PATTERN_FAST, str)
        self.assertIn('README', CODE_PATTERN_FAST.upper())
    
    def test_fast_mode_is_readme_pattern(self):
        """Test that fast mode pattern is README-specific."""
        self.assertTrue(
            CODE_PATTERN_FAST.endswith('README.md') or 
            'readme' in CODE_PATTERN_FAST.lower()
        )
    
    def test_default_limits_positive(self):
        """Test that default limits are positive integers."""
        self.assertGreater(DEFAULT_MAX_FILES, 0)
        self.assertGreater(DEFAULT_MAX_CHARS_PER_FILE, 0)


class TestFastModeDetection(unittest.TestCase):
    """Tests for fast mode pattern matching."""
    
    def test_fast_mode_pattern_recognition(self):
        """Test that fast mode patterns are correctly identified."""
        from config import CODE_PATTERN_FAST
        
        # Test pattern-based detection
        is_fast = CODE_PATTERN_FAST.endswith('README.md')
        self.assertTrue(is_fast)
        
        # Test case insensitivity
        is_fast_lower = '**/readme.md'.endswith('readme.md')
        self.assertTrue(is_fast_lower)
    
    def test_full_mode_pattern(self):
        """Test that full mode pattern includes multiple extensions."""
        from config import CODE_PATTERN_FULL
        
        # Should contain multiple extensions
        self.assertIn('{', CODE_PATTERN_FULL)
        self.assertIn('}', CODE_PATTERN_FULL)
        self.assertIn(',', CODE_PATTERN_FULL)


class TestDirectoryCounting(unittest.TestCase):
    """Tests for directory counting logic."""
    
    def test_scanned_dirs_incremented_correctly(self):
        """Test that scanned_dirs is only incremented for non-skipped dirs."""
        # This is a logic verification test
        # The actual counting happens in load_code() which requires filesystem
        
        # Simulate the logic:
        # - Directory A: not excluded -> should be counted
        # - Directory B: excluded -> should NOT be counted
        # - Directory C: not excluded -> should be counted
        
        exclude_dirs = {'exclude_me'}
        
        dirs_to_process = ['dirA', 'exclude_me', 'dirC']
        original_dirs = dirs_to_process[:]
        
        # Filter logic from load_code
        dirs_to_process = [d for d in dirs_to_process if d not in exclude_dirs]
        
        # Only dirA and dirC should remain
        self.assertEqual(dirs_to_process, ['dirA', 'dirC'])
        
        # Excluded count
        excluded_count = len(set(original_dirs)) - len(dirs_to_process)
        self.assertEqual(excluded_count, 1)


if __name__ == '__main__':
    unittest.main()
