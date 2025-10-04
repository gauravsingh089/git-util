# git-util

A Python utility for streamlined Git operations with conventional commits and semantic versioning.

## Features

- 🚀 **Conventional Commits**: Automatically format commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification
- 🏷️ **Semantic Versioning**: Automatic version tagging following [Semantic Versioning](https://semver.org/) (SemVer)
- 📦 **Simple CLI**: Easy-to-use command-line interface
- 🔄 **Automated Workflow**: Add, commit, tag, and push in a single command

## Installation

```bash
# Clone the repository
git clone https://github.com/gauravsingh089/git-util.git
cd git-util

# Install in development mode
pip install -e .
```

## Usage

### Basic Commands

#### Add Files
```bash
# Add all files
git-util add

# Add specific files
git-util add file1.py file2.py
```

#### Commit with Conventional Commit Format
```bash
# Basic commit
git-util commit -t feat -d "add new authentication module"

# Commit with scope
git-util commit -t fix -d "resolve login issue" -s auth

# Commit with detailed body
git-util commit -t feat -d "add user profile" -b "Added comprehensive user profile with avatar support"

# Breaking change commit
git-util commit -t feat -d "redesign API" --breaking

# Commit with footer (e.g., issue reference)
git-util commit -t fix -d "fix memory leak" --footer "Fixes #123"
```

#### Create Semantic Version Tags
```bash
# Create a patch version tag (0.0.X)
git-util tag -b patch -m "Bug fixes"

# Create a minor version tag (0.X.0)
git-util tag -b minor -m "New features"

# Create a major version tag (X.0.0)
git-util tag -b major -m "Breaking changes"

# Create and push tag
git-util tag -b minor --push
```

#### Push Changes
```bash
# Push to origin
git-util push

# Push to specific remote and branch
git-util push --remote origin --branch main

# Push with tags
git-util push --tags
```

### Combined Workflows

#### Add, Commit, and Push
```bash
git-util commit -t feat -d "add new feature" -f file1.py file2.py --push
```

#### Add, Commit, Tag, and Push
```bash
git-util commit -t feat -d "add authentication" --tag minor --push
```

## Conventional Commit Types

The utility supports the following conventional commit types:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, whitespace, etc.)
- **refactor**: Code refactoring without functionality changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system or dependency changes
- **ci**: CI/CD configuration changes
- **chore**: Other changes that don't modify src or test files

## Semantic Versioning

The utility follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes (breaking changes)
- **MINOR**: New functionality in a backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

### Version Bump Rules
- Use `--tag patch` for bug fixes and minor changes
- Use `--tag minor` for new features
- Use `--tag major` for breaking changes

## Examples

### Example 1: Feature Development Workflow
```bash
# Make changes to your code
# ...

# Add, commit, and push a new feature
git-util commit -t feat -d "add user dashboard" -s ui --push
```

### Example 2: Bug Fix with Tagging
```bash
# Fix a bug
# ...

# Add, commit, create patch tag, and push
git-util commit -t fix -d "fix validation error" --tag patch --push
```

### Example 3: Breaking Change Release
```bash
# Make breaking changes
# ...

# Commit with breaking change flag
git-util commit -t feat -d "redesign authentication API" --breaking

# Create major version tag and push
git-util tag -b major -m "Version 2.0.0 - New authentication API" --push
```

### Example 4: Documentation Update
```bash
# Update documentation
# ...

# Commit documentation changes (no need to tag)
git-util commit -t docs -d "update installation guide" --push
```

## API Usage

You can also use git-util as a Python library:

```python
from git_util import GitUtil
from git_util.git_operations import CommitType, VersionBump

# Initialize
git = GitUtil()

# Add files
git.add_files(["file1.py", "file2.py"])

# Create conventional commit
git.create_conventional_commit(
    commit_type=CommitType.FEAT,
    description="add new feature",
    scope="api",
    body="Detailed description of the feature"
)

# Create tag and push
git.auto_tag_and_push(
    bump_type=VersionBump.MINOR,
    remote="origin",
    tag_message="Release v0.2.0"
)
```

## Requirements

- Python 3.7+
- Git installed and configured

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Python utility script for grouping required git commands

## Overview

`git_util.py` is a Python utility that groups and simplifies common git operations. Instead of typing multiple git commands, you can execute grouped operations with a single command.

## Features

- **Status & Info**: View repository status, current branch, and remotes at once
- **Quick Commit**: Add all changes and commit with one command
- **Sync**: Pull and push changes in one operation
- **Branch Management**: Easy branch creation, switching, and viewing
- **Commit History**: View formatted commit logs
- **Undo Operations**: Safely undo commits or discard changes
- **Stash Management**: Save, apply, and list stashes

## Requirements

- Python 3.6 or higher
- Git installed and accessible from command line

## Usage

Make the script executable:
```bash
chmod +x git_util.py
```

### Available Commands

#### Repository Status
Display comprehensive repository information including status, current branch, and remotes:
```bash
python3 git_util.py status
```

#### Quick Commit
Add all changes and commit with a message in one command:
```bash
python3 git_util.py commit "Your commit message"
```

#### Sync Repository
Pull latest changes and push local commits:
```bash
python3 git_util.py sync
```

#### Branch Information
View all local and remote branches with details:
```bash
python3 git_util.py branch
```

#### Create Branch
Create a new branch and switch to it:
```bash
python3 git_util.py create-branch feature-branch
```

Create without switching:
```bash
python3 git_util.py create-branch feature-branch --no-checkout
```

#### Switch Branch
Switch to an existing branch:
```bash
python3 git_util.py switch main
```

#### View Commit History
Show recent commits (default: 10):
```bash
python3 git_util.py log
```

Show specific number of commits:
```bash
python3 git_util.py log -n 20
```

#### Undo Last Commit
Undo last commit but keep changes in staging area:
```bash
python3 git_util.py undo
```

Undo last commit and discard changes:
```bash
python3 git_util.py undo --hard
```

#### Discard Changes
Discard all changes in working directory:
```bash
python3 git_util.py discard
```

Discard changes in specific file:
```bash
python3 git_util.py discard path/to/file.txt
```

#### Stash Operations
Save current changes to stash:
```bash
python3 git_util.py stash-save
```

Save with a message:
```bash
python3 git_util.py stash-save -m "Work in progress"
```

Apply and remove most recent stash:
```bash
python3 git_util.py stash-pop
```

List all stashes:
```bash
python3 git_util.py stash-list
```

## Help

View all available commands and options:
```bash
python3 git_util.py --help
```

View help for specific command:
```bash
python3 git_util.py commit --help
```

## Examples

### Daily Workflow
```bash
# Check what's changed
python3 git_util.py status

# Create a feature branch
python3 git_util.py create-branch new-feature

# Make changes to files...

# Quick commit
python3 git_util.py commit "Add new feature"

# Sync with remote
python3 git_util.py sync
```

### Working with Stashes
```bash
# Save current work
python3 git_util.py stash-save -m "Partial implementation"

# Switch to another branch
python3 git_util.py switch hotfix

# Do some work...

# Switch back and restore work
python3 git_util.py switch feature-branch
python3 git_util.py stash-pop
```

## License

MIT License
