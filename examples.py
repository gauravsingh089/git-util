"""Example usage of git-util library."""

from git_util import GitUtil
from git_util.git_operations import CommitType, VersionBump


def example_basic_workflow():
    """Example: Basic workflow with add, commit, and push."""
    git = GitUtil()
    
    # Add all files
    success, message = git.add_files()
    print(f"Add: {message}")
    
    # Create a conventional commit
    success, message = git.create_conventional_commit(
        commit_type=CommitType.FEAT,
        description="add new dashboard feature",
        scope="ui"
    )
    print(f"Commit: {message}")
    
    # Push to remote
    success, message = git.push_changes(remote="origin")
    print(f"Push: {message}")


def example_with_tagging():
    """Example: Workflow with version tagging."""
    git = GitUtil()
    
    # Add and commit
    git.add_files()
    git.create_conventional_commit(
        commit_type=CommitType.FIX,
        description="fix validation bug",
        body="Fixed an issue with email validation"
    )
    
    # Create tag and push
    success, message = git.auto_tag_and_push(
        bump_type=VersionBump.PATCH,
        remote="origin",
        tag_message="Bug fix release"
    )
    print(f"Tag and Push: {message}")


def example_breaking_change():
    """Example: Breaking change commit."""
    git = GitUtil()
    
    git.add_files()
    success, message = git.create_conventional_commit(
        commit_type=CommitType.FEAT,
        description="redesign authentication API",
        breaking=True,
        body="Complete redesign of the authentication system",
        footer="BREAKING CHANGE: Old API endpoints are no longer supported"
    )
    print(f"Commit: {message}")


def example_version_management():
    """Example: Manual version management."""
    git = GitUtil()
    
    # Get current version
    latest_tag = git.get_latest_tag()
    print(f"Latest tag: {latest_tag}")
    
    if latest_tag:
        version = git.parse_version(latest_tag)
        print(f"Current version: {version}")
        
        # Bump to next minor version
        new_version = git.bump_version(version, VersionBump.MINOR)
        print(f"New version: {new_version}")
        
        # Create tag
        success, message = git.create_tag(
            version=new_version,
            message="Release with new features"
        )
        print(f"Tag: {message}")


if __name__ == "__main__":
    print("Git-Util Examples")
    print("=" * 50)
    print("\nNote: These examples show how to use the library.")
    print("Uncomment the examples you want to run.\n")
    
    # Uncomment to run examples:
    # example_basic_workflow()
    # example_with_tagging()
    # example_breaking_change()
    # example_version_management()
