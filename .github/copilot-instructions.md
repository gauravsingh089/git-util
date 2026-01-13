# AI Coding Agent Guide

This repo contains two Git-related tools: a packaged CLI (`git-util`) with conventional commit + semantic versioning support, and a standalone helper script (`git_util.py`) for grouped Git operations. Both use the Python standard library and shell out to `git`.

## Architecture & Key Files
- [git-util package CLI](git-util/git_util/cli.py): Parses commands and maps to core ops.
- [core operations](git-util/git_util/git_operations.py): Implements `CommitType`, `VersionBump`, commit message construction, tag creation, pushing.
- [package init](git-util/git_util/__init__.py): Exposes `GitUtil`.
- [pyproject entrypoint](git-util/pyproject.toml#L22-L24): Defines `git-util = "git_util.cli:main"`.
- [standalone script](git-util/git_util.py): Separate class and CLI for general Git workflows (status/branch/log/stash).
- [tests](git-util/test_git_util.py): Basic `unittest` for the standalone script only.

## Developer Workflows
- Install (dev):
  - `pip install -e .`
- Run packaged CLI:
  - `git-util add`
  - `git-util commit -t feat -d "add login" -s auth --push`
  - `git-util tag -b minor -m "Release v0.2.0" --push`
- Run standalone script (repo must be a Git repo):
  - `python3 git_util.py status | branch | log | stash-save -m "msg" | sync`
- Tests (standalone script):
  - `python3 -m unittest test_git_util.py`

## Project-Specific Conventions
- Conventional commits are constructed in `GitUtil.create_conventional_commit()`:
  - Format: `type(scope)!: description` + optional body/footer; `!` when `--breaking`.
  - If `--breaking` is set and no body is provided, a default "BREAKING CHANGE" body is added.
- Semantic versioning tags use a `v` prefix:
  - Tag names: `vX.Y.Z` (see `create_tag()`; default `prefix="v"`).
  - Latest tag discovered via `git describe --tags --abbrev=0`; if none, starts from `(0,0,0)`.
- Auto flow behavior:
  - `commit --tag <patch|minor|major>` triggers `auto_tag_and_push()` (creates tag, pushes changes + tags).
  - `commit --push` pushes changes without creating a tag.
- No external Python dependencies; keep changes within stdlib + `git` CLI.

## Integration Notes
- Requires `git` available on PATH and a valid repository in the working directory.
- Remote defaults to `origin`; branch defaults to current when not specified.
- `push_changes()` pushes tags only when `push_tags=True` or via `auto_tag_and_push()`.

## Examples
- Feature commit + minor bump and push:
  - `git-util commit -t feat -d "add user dashboard" -s ui --tag minor --push`
- Standalone daily routine:
  - `python3 git_util.py status && python3 git_util.py log -n 5 && python3 git_util.py sync`

## Maintenance Tips
- Tests currently exercise `git_util.py` only; if editing packaged CLI behavior, add parallel tests or keep both CLIs aligned.
- When parsing tags, ensure they follow `vX.Y.Z` to be recognized by `parse_version()`.