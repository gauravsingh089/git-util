"""Core git operations with conventional commits and semantic versioning."""

import subprocess
import re
from typing import Optional, List, Tuple
from enum import Enum


class CommitType(Enum):
    """Conventional commit types."""
    FEAT = "feat"  # New feature
    FIX = "fix"  # Bug fix
    DOCS = "docs"  # Documentation changes
    STYLE = "style"  # Code style changes (formatting, etc.)
    REFACTOR = "refactor"  # Code refactoring
    PERF = "perf"  # Performance improvements
    TEST = "test"  # Adding or updating tests
    BUILD = "build"  # Build system or dependencies
    CI = "ci"  # CI/CD changes
    CHORE = "chore"  # Other changes


class VersionBump(Enum):
    """Semantic versioning bump types."""
    MAJOR = "major"  # Breaking changes (X.0.0)
    MINOR = "minor"  # New features (0.X.0)
    PATCH = "patch"  # Bug fixes (0.0.X)


class GitUtil:
    """Git utility for conventional commits and semantic versioning."""

    def __init__(self, repo_path: str = "."):
        """
        Initialize GitUtil.
        
        Args:
            repo_path: Path to git repository (default: current directory)
        """
        self.repo_path = repo_path

    def _run_git_command(self, args: List[str]) -> Tuple[bool, str, str]:
        """
        Run a git command.
        
        Args:
            args: Git command arguments
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            success = result.returncode == 0
            return success, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)

    def add_files(self, files: Optional[List[str]] = None) -> Tuple[bool, str]:
        """
        Add files to git staging area.
        
        Args:
            files: List of files to add (None means add all)
            
        Returns:
            Tuple of (success, message)
        """
        if files is None:
            args = ["add", "."]
        else:
            args = ["add"] + files
            
        success, stdout, stderr = self._run_git_command(args)
        
        if success:
            return True, f"Successfully added files to staging area"
        else:
            return False, f"Failed to add files: {stderr}"

    def create_conventional_commit(
        self,
        commit_type: CommitType,
        description: str,
        scope: Optional[str] = None,
        body: Optional[str] = None,
        breaking: bool = False,
        footer: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Create a conventional commit.
        
        Args:
            commit_type: Type of commit (feat, fix, etc.)
            description: Short description of changes
            scope: Optional scope of changes
            body: Optional detailed description
            breaking: Whether this is a breaking change
            footer: Optional footer (e.g., issue references)
            
        Returns:
            Tuple of (success, message)
        """
        # Build commit message
        type_str = commit_type.value
        scope_str = f"({scope})" if scope else ""
        breaking_str = "!" if breaking else ""
        
        commit_msg = f"{type_str}{scope_str}{breaking_str}: {description}"
        
        if body:
            commit_msg += f"\n\n{body}"
            
        if breaking and not body:
            commit_msg += "\n\nBREAKING CHANGE: This commit contains breaking changes"
            
        if footer:
            commit_msg += f"\n\n{footer}"
            
        # Create commit
        success, stdout, stderr = self._run_git_command(["commit", "-m", commit_msg])
        
        if success:
            return True, f"Successfully created commit: {commit_msg.split(chr(10))[0]}"
        else:
            return False, f"Failed to create commit: {stderr}"

    def get_latest_tag(self) -> Optional[str]:
        """
        Get the latest semantic version tag.
        
        Returns:
            Latest tag or None if no tags exist
        """
        success, stdout, stderr = self._run_git_command(
            ["describe", "--tags", "--abbrev=0"]
        )
        
        if success and stdout.strip():
            return stdout.strip()
        return None

    def parse_version(self, tag: str) -> Optional[Tuple[int, int, int]]:
        """
        Parse semantic version from tag.
        
        Args:
            tag: Version tag (e.g., "v1.2.3" or "1.2.3")
            
        Returns:
            Tuple of (major, minor, patch) or None if invalid
        """
        # Remove 'v' prefix if present
        version_str = tag.lstrip("v")
        
        # Parse version
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version_str)
        if match:
            return int(match.group(1)), int(match.group(2)), int(match.group(3))
        return None

    def bump_version(
        self,
        current_version: Tuple[int, int, int],
        bump_type: VersionBump
    ) -> Tuple[int, int, int]:
        """
        Bump semantic version.
        
        Args:
            current_version: Current version (major, minor, patch)
            bump_type: Type of version bump
            
        Returns:
            New version (major, minor, patch)
        """
        major, minor, patch = current_version
        
        if bump_type == VersionBump.MAJOR:
            return major + 1, 0, 0
        elif bump_type == VersionBump.MINOR:
            return major, minor + 1, 0
        else:  # PATCH
            return major, minor, patch + 1

    def create_tag(
        self,
        version: Tuple[int, int, int],
        message: Optional[str] = None,
        prefix: str = "v"
    ) -> Tuple[bool, str]:
        """
        Create a git tag with semantic version.
        
        Args:
            version: Version tuple (major, minor, patch)
            message: Optional tag message
            prefix: Tag prefix (default: "v")
            
        Returns:
            Tuple of (success, message)
        """
        tag_name = f"{prefix}{version[0]}.{version[1]}.{version[2]}"
        
        if message:
            args = ["tag", "-a", tag_name, "-m", message]
        else:
            args = ["tag", tag_name]
            
        success, stdout, stderr = self._run_git_command(args)
        
        if success:
            return True, f"Successfully created tag: {tag_name}"
        else:
            return False, f"Failed to create tag: {stderr}"

    def push_changes(
        self,
        remote: str = "origin",
        branch: Optional[str] = None,
        push_tags: bool = False
    ) -> Tuple[bool, str]:
        """
        Push changes to remote repository.
        
        Args:
            remote: Remote name (default: "origin")
            branch: Branch name (None means current branch)
            push_tags: Whether to push tags
            
        Returns:
            Tuple of (success, message)
        """
        if branch:
            args = ["push", remote, branch]
        else:
            args = ["push", remote]
            
        success, stdout, stderr = self._run_git_command(args)
        
        if not success:
            return False, f"Failed to push changes: {stderr}"
            
        message = f"Successfully pushed changes to {remote}"
        
        if push_tags:
            success, stdout, stderr = self._run_git_command(["push", remote, "--tags"])
            if success:
                message += " (including tags)"
            else:
                return False, f"Failed to push tags: {stderr}"
                
        return True, message

    def auto_tag_and_push(
        self,
        bump_type: VersionBump,
        remote: str = "origin",
        branch: Optional[str] = None,
        tag_message: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Automatically create a tag based on version bump and push.
        
        Args:
            bump_type: Type of version bump
            remote: Remote name
            branch: Branch name
            tag_message: Optional tag message
            
        Returns:
            Tuple of (success, message)
        """
        # Get latest tag
        latest_tag = self.get_latest_tag()
        
        if latest_tag:
            version = self.parse_version(latest_tag)
            if not version:
                return False, f"Failed to parse version from tag: {latest_tag}"
        else:
            # Start with 0.1.0 if no tags exist
            version = (0, 0, 0)
            
        # Bump version
        new_version = self.bump_version(version, bump_type)
        
        # Create tag
        success, msg = self.create_tag(new_version, tag_message)
        if not success:
            return False, msg
            
        # Push changes with tags
        success, msg = self.push_changes(remote, branch, push_tags=True)
        
        tag_name = f"v{new_version[0]}.{new_version[1]}.{new_version[2]}"
        if success:
            return True, f"Successfully created tag {tag_name} and pushed to {remote}"
        else:
            return False, msg
