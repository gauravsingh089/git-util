# Quick Start Guide

## Installation

```bash
pip install -e .
```

## Quick Examples

### 1. Simple Commit and Push
```bash
# Add all changes, commit with conventional format, and push
git-util commit -t feat -d "add new feature" --push
```

### 2. Bug Fix with Patch Tag
```bash
# Fix a bug and create a patch version tag
git-util commit -t fix -d "fix validation bug" --tag patch --push
```

### 3. Feature with Minor Version
```bash
# Add a feature and bump minor version
git-util commit -t feat -d "add user authentication" --tag minor --push
```

### 4. Breaking Change
```bash
# Commit breaking change
git-util commit -t feat -d "redesign API" --breaking

# Create major version tag
git-util tag -b major -m "Version 2.0.0" --push
```

## Commit Types Reference

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code formatting
- `refactor` - Code restructuring
- `perf` - Performance improvement
- `test` - Tests
- `build` - Build system
- `ci` - CI/CD
- `chore` - Other changes

## Version Bumping

- `patch` - Bug fixes (0.0.X)
- `minor` - New features (0.X.0)
- `major` - Breaking changes (X.0.0)

## Command Structure

```
git-util <command> [options]

Commands:
  add     - Add files to staging
  commit  - Create conventional commit
  tag     - Create version tag
  push    - Push to remote
```

## Common Workflows

### Daily Development
```bash
# Make changes, add, and commit
git-util commit -t feat -d "description" --push
```

### Release Preparation
```bash
# Commit final changes
git-util commit -t chore -d "prepare for release"

# Create and push release tag
git-util tag -b minor -m "Release v0.2.0" --push
```

### Hotfix
```bash
# Fix critical bug
git-util commit -t fix -d "critical security fix" --tag patch --push
```
