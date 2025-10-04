# git-util
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
