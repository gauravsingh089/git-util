"""Command-line interface for git-util."""

import argparse
import sys
from .git_operations import GitUtil, CommitType, VersionBump


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Git utility for conventional commits and semantic versioning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add all files, commit with conventional message, and push
  git-util commit -t feat -d "add new feature" --push
  
  # Add specific files and commit
  git-util commit -t fix -d "fix bug" -f file1.py file2.py
  
  # Commit with scope and body
  git-util commit -t feat -d "add login" -s auth -b "Detailed description"
  
  # Create a tag and push
  git-util tag -b minor -m "Release v0.2.0"
  
  # Full workflow: add, commit, tag, and push
  git-util commit -t feat -d "new feature" --push --tag minor
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add files to staging area")
    add_parser.add_argument(
        "files",
        nargs="*",
        help="Files to add (default: all files)"
    )
    
    # Commit command
    commit_parser = subparsers.add_parser(
        "commit",
        help="Create a conventional commit"
    )
    commit_parser.add_argument(
        "-t", "--type",
        required=True,
        choices=[ct.value for ct in CommitType],
        help="Commit type"
    )
    commit_parser.add_argument(
        "-d", "--description",
        required=True,
        help="Short description of changes"
    )
    commit_parser.add_argument(
        "-s", "--scope",
        help="Scope of changes"
    )
    commit_parser.add_argument(
        "-b", "--body",
        help="Detailed description"
    )
    commit_parser.add_argument(
        "--breaking",
        action="store_true",
        help="Mark as breaking change"
    )
    commit_parser.add_argument(
        "--footer",
        help="Footer (e.g., issue references)"
    )
    commit_parser.add_argument(
        "-f", "--files",
        nargs="*",
        help="Files to add before committing (default: all files)"
    )
    commit_parser.add_argument(
        "--push",
        action="store_true",
        help="Push after committing"
    )
    commit_parser.add_argument(
        "--tag",
        choices=[vb.value for vb in VersionBump],
        help="Create and push tag with version bump"
    )
    commit_parser.add_argument(
        "--remote",
        default="origin",
        help="Remote name (default: origin)"
    )
    commit_parser.add_argument(
        "--branch",
        help="Branch name (default: current branch)"
    )
    
    # Tag command
    tag_parser = subparsers.add_parser(
        "tag",
        help="Create a semantic version tag"
    )
    tag_parser.add_argument(
        "-b", "--bump",
        required=True,
        choices=[vb.value for vb in VersionBump],
        help="Version bump type"
    )
    tag_parser.add_argument(
        "-m", "--message",
        help="Tag message"
    )
    tag_parser.add_argument(
        "--push",
        action="store_true",
        help="Push tag after creating"
    )
    tag_parser.add_argument(
        "--remote",
        default="origin",
        help="Remote name (default: origin)"
    )
    
    # Push command
    push_parser = subparsers.add_parser(
        "push",
        help="Push changes to remote"
    )
    push_parser.add_argument(
        "--remote",
        default="origin",
        help="Remote name (default: origin)"
    )
    push_parser.add_argument(
        "--branch",
        help="Branch name (default: current branch)"
    )
    push_parser.add_argument(
        "--tags",
        action="store_true",
        help="Push tags"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    git_util = GitUtil()
    
    try:
        if args.command == "add":
            files = args.files if args.files else None
            success, message = git_util.add_files(files)
            print(message)
            sys.exit(0 if success else 1)
            
        elif args.command == "commit":
            # Add files if specified
            files = args.files if hasattr(args, 'files') and args.files else None
            if files is not None or (hasattr(args, 'files') and args.files is not None):
                success, message = git_util.add_files(files)
                if not success:
                    print(f"Error: {message}", file=sys.stderr)
                    sys.exit(1)
                print(message)
            
            # Create commit
            commit_type = CommitType(args.type)
            success, message = git_util.create_conventional_commit(
                commit_type=commit_type,
                description=args.description,
                scope=args.scope,
                body=args.body,
                breaking=args.breaking,
                footer=args.footer
            )
            
            if not success:
                print(f"Error: {message}", file=sys.stderr)
                sys.exit(1)
            print(message)
            
            # Create tag if requested
            if args.tag:
                bump_type = VersionBump(args.tag)
                success, message = git_util.auto_tag_and_push(
                    bump_type=bump_type,
                    remote=args.remote,
                    branch=args.branch,
                    tag_message=args.description
                )
                if not success:
                    print(f"Error: {message}", file=sys.stderr)
                    sys.exit(1)
                print(message)
            elif args.push:
                # Push without tag
                success, message = git_util.push_changes(
                    remote=args.remote,
                    branch=args.branch,
                    push_tags=False
                )
                if not success:
                    print(f"Error: {message}", file=sys.stderr)
                    sys.exit(1)
                print(message)
                
        elif args.command == "tag":
            bump_type = VersionBump(args.bump)
            
            # Get latest tag and bump version
            latest_tag = git_util.get_latest_tag()
            if latest_tag:
                version = git_util.parse_version(latest_tag)
                if not version:
                    print(f"Error: Failed to parse version from tag: {latest_tag}", file=sys.stderr)
                    sys.exit(1)
            else:
                version = (0, 0, 0)
            
            new_version = git_util.bump_version(version, bump_type)
            success, message = git_util.create_tag(new_version, args.message)
            
            if not success:
                print(f"Error: {message}", file=sys.stderr)
                sys.exit(1)
            print(message)
            
            if args.push:
                success, message = git_util.push_changes(
                    remote=args.remote,
                    push_tags=True
                )
                if not success:
                    print(f"Error: {message}", file=sys.stderr)
                    sys.exit(1)
                print(message)
                
        elif args.command == "push":
            success, message = git_util.push_changes(
                remote=args.remote,
                branch=args.branch,
                push_tags=args.tags
            )
            
            if not success:
                print(f"Error: {message}", file=sys.stderr)
                sys.exit(1)
            print(message)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
