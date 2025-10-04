# Git Utility - Usage Examples

This file contains practical examples of using the git utility in common workflows.

## Scenario 1: Starting a New Feature

```bash
# Check current status
python3 git_util.py status

# Create a new feature branch
python3 git_util.py create-branch feature/add-login

# Make your code changes...

# Quick commit all changes
python3 git_util.py commit "Add login functionality"

# Push to remote
python3 git_util.py sync
```

## Scenario 2: Checking Work Status

```bash
# View repository status
python3 git_util.py status

# View recent commits
python3 git_util.py log

# View all branches
python3 git_util.py branch
```

## Scenario 3: Switching Between Features

```bash
# Save current work
python3 git_util.py stash-save -m "Login form in progress"

# Switch to another branch
python3 git_util.py switch feature/bug-fix

# Work on bug fix...

# Return to original feature
python3 git_util.py switch feature/add-login

# Restore your work
python3 git_util.py stash-pop
```

## Scenario 4: Fixing a Commit Mistake

```bash
# Made a commit with typo in message
python3 git_util.py undo

# Re-commit with correct message
python3 git_util.py commit "Fix typo in user authentication"
```

## Scenario 5: Daily Sync Routine

```bash
# Morning: Get latest changes
python3 git_util.py switch main
python3 git_util.py sync

# Create daily work branch
python3 git_util.py create-branch work/daily-tasks

# End of day: Commit and sync
python3 git_util.py commit "Complete daily tasks"
python3 git_util.py sync
```

## Scenario 6: Discard Unwanted Changes

```bash
# Discard all changes
python3 git_util.py discard

# Or discard specific file
python3 git_util.py discard src/config.py
```

## Scenario 7: Review History

```bash
# View last 5 commits
python3 git_util.py log -n 5

# View last 20 commits
python3 git_util.py log -n 20

# View all branches with details
python3 git_util.py branch
```

## Scenario 8: Managing Stashes

```bash
# Save work with description
python3 git_util.py stash-save -m "Experimental feature"

# View all stashes
python3 git_util.py stash-list

# Apply most recent stash
python3 git_util.py stash-pop
```

## Quick Reference

| Task | Command |
|------|---------|
| Check status | `python3 git_util.py status` |
| Quick commit | `python3 git_util.py commit "message"` |
| Sync (pull & push) | `python3 git_util.py sync` |
| New branch | `python3 git_util.py create-branch name` |
| Switch branch | `python3 git_util.py switch name` |
| View log | `python3 git_util.py log` |
| Undo commit | `python3 git_util.py undo` |
| Save stash | `python3 git_util.py stash-save` |
| Apply stash | `python3 git_util.py stash-pop` |
| List stashes | `python3 git_util.py stash-list` |

## Tips

1. **Always check status first**: Before making changes, run `status` to see what's in your working directory
2. **Use meaningful commit messages**: The `commit` command makes it easy to commit with good messages
3. **Stash frequently**: Use stash to save work when you need to switch contexts quickly
4. **Review before sync**: Check your commits with `log` before running `sync`
5. **Create feature branches**: Use `create-branch` for all new features to keep work organized
