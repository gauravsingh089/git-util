#!/usr/bin/env python3
"""
Simple tests for git_util.py
"""

import unittest
import subprocess
import sys
import os


class TestGitUtil(unittest.TestCase):
    """Test cases for git utility"""
    
    def setUp(self):
        """Set up test environment"""
        self.script_path = os.path.join(os.path.dirname(__file__), "git_util.py")
    
    def run_git_util(self, args):
        """Helper method to run git_util.py with arguments"""
        cmd = [sys.executable, self.script_path] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        return result
    
    def test_help_command(self):
        """Test that help command works"""
        result = self.run_git_util(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Git Utility", result.stdout)
        self.assertIn("Available commands", result.stdout)
    
    def test_status_command(self):
        """Test that status command executes"""
        result = self.run_git_util(["status"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Repository Status", result.stdout)
    
    def test_branch_command(self):
        """Test that branch command executes"""
        result = self.run_git_util(["branch"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Branch Information", result.stdout)
    
    def test_log_command(self):
        """Test that log command executes"""
        result = self.run_git_util(["log"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Recent Commits", result.stdout)
    
    def test_log_command_with_number(self):
        """Test log command with custom number of commits"""
        result = self.run_git_util(["log", "-n", "5"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Recent Commits (last 5)", result.stdout)
    
    def test_stash_list_command(self):
        """Test that stash-list command executes"""
        result = self.run_git_util(["stash-list"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Stash List", result.stdout)
    
    def test_commit_help(self):
        """Test commit subcommand help"""
        result = self.run_git_util(["commit", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("commit", result.stdout)
        self.assertIn("message", result.stdout)
    
    def test_no_command(self):
        """Test that running with no command shows help"""
        result = self.run_git_util([])
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
