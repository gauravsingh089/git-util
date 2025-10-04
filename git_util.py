#!/usr/bin/env python3
"""
Git Utility - A Python script to group and execute common git commands
"""

import subprocess
import sys
import argparse
from typing import List, Optional


class GitUtil:
    """Git utility class for executing grouped git commands"""

    @staticmethod
    def run_command(command: List[str]) -> tuple:
        """
        Execute a shell command and return output and return code
        
        Args:
            command: List of command arguments
            
        Returns:
            Tuple of (stdout, stderr, returncode)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1

    def status_info(self) -> None:
        """Display repository status and information"""
        print("=== Repository Status ===")
        commands = [
            (["git", "status", "--short"], "Short status"),
            (["git", "branch", "--show-current"], "Current branch"),
            (["git", "remote", "-v"], "Remote repositories"),
        ]
        
        for cmd, description in commands:
            print(f"\n{description}:")
            stdout, stderr, code = self.run_command(cmd)
            if code == 0:
                print(stdout if stdout else "(no output)")
            else:
                print(f"Error: {stderr}")

    def quick_commit(self, message: str) -> None:
        """Add all changes and commit with a message"""
        print("=== Quick Commit ===")
        
        # Add all changes
        print("\nAdding all changes...")
        stdout, stderr, code = self.run_command(["git", "add", "."])
        if code != 0:
            print(f"Error adding files: {stderr}")
            return
        
        # Commit
        print(f"\nCommitting with message: '{message}'")
        stdout, stderr, code = self.run_command(["git", "commit", "-m", message])
        if code == 0:
            print(stdout)
        else:
            print(f"Error committing: {stderr}")

    def sync(self) -> None:
        """Pull latest changes and push local changes"""
        print("=== Sync Repository ===")
        
        # Pull
        print("\nPulling latest changes...")
        stdout, stderr, code = self.run_command(["git", "pull"])
        if code == 0:
            print(stdout)
        else:
            print(f"Pull error: {stderr}")
            return
        
        # Push
        print("\nPushing local changes...")
        stdout, stderr, code = self.run_command(["git", "push"])
        if code == 0:
            print(stdout if stdout else "Push successful")
        else:
            print(f"Push error: {stderr}")

    def branch_info(self) -> None:
        """Display branch information"""
        print("=== Branch Information ===")
        
        print("\nLocal branches:")
        stdout, stderr, code = self.run_command(["git", "branch", "-v"])
        if code == 0:
            print(stdout)
        else:
            print(f"Error: {stderr}")
        
        print("\nRemote branches:")
        stdout, stderr, code = self.run_command(["git", "branch", "-r"])
        if code == 0:
            print(stdout)
        else:
            print(f"Error: {stderr}")

    def create_branch(self, branch_name: str, checkout: bool = True) -> None:
        """Create and optionally checkout a new branch"""
        print(f"=== Creating Branch: {branch_name} ===")
        
        if checkout:
            stdout, stderr, code = self.run_command(["git", "checkout", "-b", branch_name])
        else:
            stdout, stderr, code = self.run_command(["git", "branch", branch_name])
        
        if code == 0:
            print(f"Branch '{branch_name}' created successfully")
            if stdout:
                print(stdout)
        else:
            print(f"Error: {stderr}")

    def switch_branch(self, branch_name: str) -> None:
        """Switch to a different branch"""
        print(f"=== Switching to Branch: {branch_name} ===")
        
        stdout, stderr, code = self.run_command(["git", "checkout", branch_name])
        if code == 0:
            print(f"Switched to branch '{branch_name}'")
            if stdout:
                print(stdout)
        else:
            print(f"Error: {stderr}")

    def log_history(self, limit: int = 10) -> None:
        """Display commit history"""
        print(f"=== Recent Commits (last {limit}) ===\n")
        
        stdout, stderr, code = self.run_command([
            "git", "log", 
            f"--oneline", 
            f"-{limit}",
            "--decorate"
        ])
        if code == 0:
            print(stdout)
        else:
            print(f"Error: {stderr}")

    def undo_last_commit(self, keep_changes: bool = True) -> None:
        """Undo the last commit"""
        print("=== Undo Last Commit ===")
        
        if keep_changes:
            stdout, stderr, code = self.run_command(["git", "reset", "--soft", "HEAD~1"])
            print("Last commit undone, changes kept in staging area")
        else:
            stdout, stderr, code = self.run_command(["git", "reset", "--hard", "HEAD~1"])
            print("Last commit undone, changes discarded")
        
        if code != 0:
            print(f"Error: {stderr}")

    def discard_changes(self, file_path: Optional[str] = None) -> None:
        """Discard changes in working directory"""
        if file_path:
            print(f"=== Discarding Changes in: {file_path} ===")
            stdout, stderr, code = self.run_command(["git", "checkout", "--", file_path])
        else:
            print("=== Discarding All Changes ===")
            stdout, stderr, code = self.run_command(["git", "checkout", "--", "."])
        
        if code == 0:
            print("Changes discarded successfully")
        else:
            print(f"Error: {stderr}")

    def stash_save(self, message: Optional[str] = None) -> None:
        """Save current changes to stash"""
        print("=== Stashing Changes ===")
        
        if message:
            cmd = ["git", "stash", "push", "-m", message]
        else:
            cmd = ["git", "stash"]
        
        stdout, stderr, code = self.run_command(cmd)
        if code == 0:
            print(stdout if stdout else "Changes stashed successfully")
        else:
            print(f"Error: {stderr}")

    def stash_pop(self) -> None:
        """Apply and remove the most recent stash"""
        print("=== Applying Stash ===")
        
        stdout, stderr, code = self.run_command(["git", "stash", "pop"])
        if code == 0:
            print(stdout if stdout else "Stash applied successfully")
        else:
            print(f"Error: {stderr}")

    def stash_list(self) -> None:
        """List all stashes"""
        print("=== Stash List ===\n")
        
        stdout, stderr, code = self.run_command(["git", "stash", "list"])
        if code == 0:
            print(stdout if stdout else "No stashes found")
        else:
            print(f"Error: {stderr}")


def main():
    """Main entry point for the git utility"""
    parser = argparse.ArgumentParser(
        description="Git Utility - Group and execute common git commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status              # Show repository status and info
  %(prog)s commit "message"    # Quick commit all changes
  %(prog)s sync                # Pull and push changes
  %(prog)s branch              # Show branch information
  %(prog)s create-branch dev   # Create and switch to 'dev' branch
  %(prog)s switch main         # Switch to 'main' branch
  %(prog)s log                 # Show recent commits
  %(prog)s stash-save          # Stash current changes
  %(prog)s stash-pop           # Apply most recent stash
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    subparsers.add_parser("status", help="Display repository status and information")
    
    # Commit command
    commit_parser = subparsers.add_parser("commit", help="Add all changes and commit")
    commit_parser.add_argument("message", help="Commit message")
    
    # Sync command
    subparsers.add_parser("sync", help="Pull latest changes and push local changes")
    
    # Branch command
    subparsers.add_parser("branch", help="Display branch information")
    
    # Create branch command
    create_branch_parser = subparsers.add_parser("create-branch", help="Create a new branch")
    create_branch_parser.add_argument("name", help="Branch name")
    create_branch_parser.add_argument("--no-checkout", action="store_true", 
                                      help="Don't checkout the new branch")
    
    # Switch branch command
    switch_parser = subparsers.add_parser("switch", help="Switch to a different branch")
    switch_parser.add_argument("name", help="Branch name")
    
    # Log command
    log_parser = subparsers.add_parser("log", help="Display commit history")
    log_parser.add_argument("-n", "--number", type=int, default=10, 
                           help="Number of commits to show (default: 10)")
    
    # Undo command
    undo_parser = subparsers.add_parser("undo", help="Undo last commit")
    undo_parser.add_argument("--hard", action="store_true", 
                            help="Discard changes (default: keep changes)")
    
    # Discard command
    discard_parser = subparsers.add_parser("discard", help="Discard changes in working directory")
    discard_parser.add_argument("file", nargs="?", help="Specific file to discard (default: all)")
    
    # Stash commands
    stash_save_parser = subparsers.add_parser("stash-save", help="Save changes to stash")
    stash_save_parser.add_argument("-m", "--message", help="Stash message")
    
    subparsers.add_parser("stash-pop", help="Apply and remove most recent stash")
    subparsers.add_parser("stash-list", help="List all stashes")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    git_util = GitUtil()
    
    # Execute the appropriate command
    if args.command == "status":
        git_util.status_info()
    elif args.command == "commit":
        git_util.quick_commit(args.message)
    elif args.command == "sync":
        git_util.sync()
    elif args.command == "branch":
        git_util.branch_info()
    elif args.command == "create-branch":
        git_util.create_branch(args.name, not args.no_checkout)
    elif args.command == "switch":
        git_util.switch_branch(args.name)
    elif args.command == "log":
        git_util.log_history(args.number)
    elif args.command == "undo":
        git_util.undo_last_commit(not args.hard)
    elif args.command == "discard":
        git_util.discard_changes(args.file)
    elif args.command == "stash-save":
        git_util.stash_save(args.message)
    elif args.command == "stash-pop":
        git_util.stash_pop()
    elif args.command == "stash-list":
        git_util.stash_list()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
