---
title: Git Worktrees for AI Development
source: https://www.kdnuggets.com/git-worktrees-for-ai-development?shem=dsdf%2Csharefoc%2Cagadiscoversdl%2C%2Csh%2Fx%2Fdiscover%2Fm1%2F4
captured: 2026-07-22T10:01:46+01:00 2026-07-22T10:01:46+01:00
status: processing
tags:
- input
type: head
permalink: llmeon/20-thinking/21-workbench/head-git-worktrees-for-ai-development
---

## Raw Output / Content
## \# Introduction

You are running **[Claude Code](https://github.com/anthropics/claude-code)** on a feature branch. The agent has been working for twenty minutes, it has read your codebase, built up context, and started making real progress on the authentication rewrite. Then a Slack message appears: production is down, someone needs a hotfix on `main`, and they need it now.

In the old workflow, you stash your changes, switch branches, lose everything your AI agent built up, fix the bug, push, switch back, and spend ten minutes getting the agent re-oriented to what it was doing. If you were running two agents simultaneously on the same directory, the situation is worse — both agents touching `package.json`, both generating edits to the same files, and the second writes silently, overwriting the first. No warning. No error. Just corrupted work you discover an hour later when tests fail in a way that makes no sense.

**[Git worktrees](https://git-scm.com/docs/git-worktree)** eliminate this entire class of problems. They are not a new invention — the feature has been in Git since version 2.5, released in 2015 — but the AI coding wave of 2025–2026 made them essential infrastructure. One **.git** directory, multiple working directories, each on its own branch, each invisible to the others. Each AI agent gets its own isolated workspace. The hotfix gets its own workspace. Nothing collides.

[51% of professional developers now use AI tools daily, but only 17% of developers using AI agents say those tools have improved team collaboration](https://blog.appxlab.io/2026/03/31/multi-agent-ai-coding-workflow-git-worktrees/). The gap between those two numbers is not a tooling problem. It is an infrastructure problem. Teams adopted AI agents without the workflow layer underneath. This guide is that workflow layer.

By the end, you will know what worktrees are, how to set them up, how to run parallel AI agents inside them without chaos, and how to maintain them over the life of a project.

<iframe frameborder="0" src="https://22feb83616c7e88bc2d40c5e3fdba8f8.safeframe.googlesyndication.com/safeframe/1-0-45/html/container.html" title="3rd party ad content" width="360" height="300" allow="private-state-token-redemption;attribution-reporting" aria-label="Advertisement"></iframe>

## \# What Git Worktrees Actually Are

A standard Git repository has one working directory — the folder where your files live and where you edit code. To work on a different branch, you switch to it, which changes all the files in that directory to match the branch. If you have uncommitted work, you stash it first. If your AI agent is mid-task, you interrupt it.

Git worktrees break this constraint. A worktree is a separate directory checked out from the same repository. You can have as many as you need, each on its own branch, all coexisting simultaneously on your filesystem.

```
my-project/                    ← main worktree  (branch: main)
my-project-feat-auth/          ← linked worktree (branch: feat/auth)
my-project-feat-api/           ← linked worktree (branch: feat/api)
my-project-hotfix-login/       ← linked worktree (branch: hotfix/login)
```

All four directories share the same **.git** folder. They share history, objects, and commits. But each has its own checked-out files, its own index, and its own working state. An agent editing files in `my-project-feat-auth/` cannot see or touch anything in `my-project-feat-api/`. They are physically separate directories that happen to share a git backend.

![A diagram showing one .git folder at the center with four directory boxes branching out from it](https://www.kdnuggets.com/wp-content/uploads/KDN-Shittu-A-diagram-showing-one-git-folder-at-the-center-with-four-directory-boxes-branching-out-from-it-b.png)

**Why does this beat multiple clones?** The naive alternative to worktrees is cloning the repository twice and working in different clone directories. This works, but it has real costs: you duplicate the entire repository on disk, git history is not shared between clones, commits in one clone are not immediately visible in another, and there is no coordination between them at the git layer. With worktrees, you clone once. Every additional worktree adds only the cost of the checked-out files, not another copy of the full history.

The seven commands that cover everything you need to manage worktrees:

| **Command** | **What It Does** |
| --- | --- |
| `git worktree add <path> -b <branch>` | Create a new worktree on a new branch |
| `git worktree add <path> <existing-branch>` | Check out an existing branch into a new worktree |
| `git worktree list` | Show all active worktrees with their branches and commit hashes |
| `git worktree lock <path>` | Prevent a worktree from being pruned (useful while an agent is running) |
| `git worktree unlock <path>` | Release the lock |
| `git worktree remove <path>` | Delete a worktree cleanly (branch is preserved) |
| `git worktree prune` | Clean up metadata for worktrees that were manually deleted |

That is the full surface area. Everything else in this article is a workflow built on top of these seven commands.

<iframe frameborder="0" src="https://22feb83616c7e88bc2d40c5e3fdba8f8.safeframe.googlesyndication.com/safeframe/1-0-45/html/container.html" title="3rd party ad content" width="1" height="1" allow="private-state-token-redemption;attribution-reporting" aria-label="Advertisement"></iframe>

## \# Setting Up

Prerequisites: Git 2.5 or higher. Run `git --version` to check. Any modern system (macOS, Linux, Windows with WSL or Git Bash) ships with a version above 2.5.

#### // Step 1: Starting From a Clean Repository

Worktrees work best when your main branch is clean. Commit or stash any in-progress work before creating your first worktree.

```
# Verify you have a clean working tree
git status

# If there is uncommitted work, commit it
git add . && git commit -m "checkpoint: work in progress"
```

#### // Step 2: Creating Your First Worktree

```
# Create a new worktree at ../myapp-feat-auth on a new branch feat/auth
# Replace "myapp" with your project name and "feat/auth" with your branch name
git worktree add -b feat/auth ../myapp-feat-auth main

# Verify it was created
git worktree list
```

You should see output like this:

```
/home/user/myapp            abc1234 [main]
/home/user/myapp-feat-auth  abc1234 [feat/auth]
```

Both directories exist. Both contain the same files from the `main` branch. From this point, any changes you make in `myapp-feat-auth/` stay on `feat/auth` and are completely isolated from `main`.

#### // Step 3: Setting Up the Environment in the New Worktree

This is the step most tutorials skip. A worktree is a new working directory. It does not automatically have your `.env` file, your installed `node_modules`, or your Python virtual environment. You need to set those up explicitly.

```
cd ../myapp-feat-auth

# Copy environment files that are gitignored
# .env, .env.local, and similar files are not tracked in git --
# they will not appear in the new worktree automatically
cp ../myapp/.env .env
cp ../myapp/.env.local .env.local 2>/dev/null || true

# Node.js project: install dependencies
# Each worktree is an independent working directory --
# node_modules from the parent does not carry over
npm install

# Python project: create and activate a virtual environment
# python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

#### // Step 4: Verifying the Worktree Is Isolated

```
# From inside the new worktree
git branch
# Should show: * feat/auth

# Make a test change
echo "// test" >> test-isolation.js
git status
# Only shows the change in this worktree

# Switch to the main directory and verify it is unaffected
cd ../myapp
git status
# Clean -- the test-isolation.js change is invisible here
ls test-isolation.js 2>/dev/null || echo "Not here -- isolation confirmed"
```

That is all you need to get started. The worktree is live. Any agent you open in that directory operates only on **feat/auth**.

<iframe frameborder="0" src="https://22feb83616c7e88bc2d40c5e3fdba8f8.safeframe.googlesyndication.com/safeframe/1-0-45/html/container.html" title="3rd party ad content" width="360" height="300" allow="private-state-token-redemption;attribution-reporting" aria-label="Advertisement"></iframe>

## \# A Real-World Case Study

The clearest documented example of git worktrees used for AI-driven parallel development comes from the [Microsoft Global Hackathon 2025](https://www.tamirdresher.com/blog/2025/10/20/scaling-your-ai-development-team-with-git-worktrees/).

Tamir Dresher, an engineering lead, faced a problem that everyone building with AI agents eventually hits: too many features, too little time, and no way to work on more than one thing at once without constant context-switching. Creating multiple clones of the repository was cumbersome. Switching branches destroyed the AI agent's context. Something had to change.

The solution was to use git worktrees to create what Dresher described as a virtual AI development team. Each feature got its own worktree. Each worktree got its own VS Code window. Each window ran its own AI agent. Dresher's role shifted from developer to tech lead: scoping tasks, reviewing output, guiding agents that got stuck, and merging finished work.

The setup looked like this:

```
myapp/                       ← main window: coordination and reviews
myapp-feat-authentication/   ← Agent 1: implementing OAuth2 flow
myapp-feat-api-endpoints/    ← Agent 2: building REST endpoints
myapp-bugfix-login-crash/    ← Agent 3: fixing production bug
```

Each VS Code window was completely independent. Language servers, linters, and test runners run per window. The agents never touched each other's files. When Agent 1 finished, Dresher reviewed the diff, approved it, and opened a pull request (PR) from that branch — the same workflow as reviewing a PR from a human engineer.

Three concrete advantages Dresher documented from the hackathon:

1. **No context loss.** Each AI agent maintained full context of its specific task. Switching between features meant switching VS Code windows, not branches, not stashes, not agent restarts. The agent's understanding of what it was building stayed intact.
2. **Different tools for different jobs.** Because each window was independent, Dresher ran **[Roo](https://roocode.com/)** in one window for rapid feature development and **[GitHub Copilot](https://github.com/features/copilot)** with Visual Studio in another for debugging complex issues. Mixing tools across tasks was trivial.
3. **Clean branch management.** If a feature needed to be abandoned, closing the window and deleting the worktree took ten seconds. The other agents were unaffected.

![A flowchart showing the hackathon setup](https://www.kdnuggets.com/wp-content/uploads/KDN-Shittu-A-flowchart-showing-the-hackathon-setup-b.png)

The pattern that emerged from this hackathon is now a documented best practice across the AI coding community.

<iframe frameborder="0" src="https://22feb83616c7e88bc2d40c5e3fdba8f8.safeframe.googlesyndication.com/safeframe/1-0-45/html/container.html" title="3rd party ad content" width="360" height="300" allow="private-state-token-redemption;attribution-reporting" aria-label="Advertisement"></iframe>

## \# Running Parallel AI Agents With Worktrees

The mechanics of the full parallel workflow have four stages: set up the worktrees, give each agent its context, run the agents, and checkpoint regularly.

#### // Stage 1: Scripting the Worktree Creation

Do not create worktrees manually each time. A script ensures every worktree gets the same setup — environment files, dependency installation, and a clean starting point.

Prerequisites: Git 2.5+, Bash (macOS/Linux/WSL)

How to run: Save as `create-worktree.sh` in your project root, run `chmod +x create-worktree.sh`, then `./create-worktree.sh feat/auth-redesign main`.

```
#!/usr/bin/env bash
# create-worktree.sh
# Creates an isolated worktree for one AI agent task
# Usage: ./create-worktree.sh  [base-branch]
# Example: ./create-worktree.sh feat/auth-redesign main

set -euo pipefail

BRANCH="${1:?Usage: $0  [base-branch]}"
BASE="${2:-main}"
REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_ROOT")"

# Replace slashes in branch name with dashes for directory naming
# feat/auth-redesign becomes feat-auth-redesign in the path
WORKTREE_PATH="${REPO_ROOT}/../${REPO_NAME}-${BRANCH//\//-}"

echo "Creating worktree for branch: $BRANCH"
echo "Base branch: $BASE"
echo "Worktree path: $WORKTREE_PATH"

# Fetch latest so the new branch starts from the current remote state
git fetch origin 2>/dev/null || echo "(no remote -- skipping fetch)"

# Create the worktree on a new branch from the base branch
# Falls back to checking out an existing branch if -b fails
git worktree add -b "$BRANCH" "$WORKTREE_PATH" "$BASE" 2>/dev/null || \
  git worktree add "$WORKTREE_PATH" "$BRANCH"

# Copy non-tracked environment files into the worktree
# These are gitignored, so they do not carry over automatically
for f in .env .env.local .env.development .env.test; do
  if [ -f "$REPO_ROOT/$f" ]; then
    cp "$REPO_ROOT/$f" "$WORKTREE_PATH/$f"
    echo "Copied $f"
  fi
done

# Node.js: install dependencies in the new working directory
if [ -f "$WORKTREE_PATH/package.json" ]; then
  echo "Installing Node dependencies..."
  (cd "$WORKTREE_PATH" && npm install --silent 2>/dev/null || \
   echo "(npm install skipped -- run it manually in the worktree)")
fi

# Python: remind the developer to set up their environment
if [ -f "$WORKTREE_PATH/requirements.txt" ] || [ -f "$WORKTREE_PATH/pyproject.toml" ]; then
  echo "Python project detected."
  echo "Run in the new worktree:"
  echo "  python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
fi

echo ""
echo "Worktree ready. Open it in your IDE and start your agent:"
echo "  cd $WORKTREE_PATH"
```

What this does: The script creates the worktree, copies gitignored environment files across (the most common setup failure), and runs dependency installation in the new directory. The `${BRANCH//\//-}` substitution safely converts branch names like `feat/auth` into filesystem-friendly directory names like `feat-auth`. The fallback on line 23 handles the case where the branch already exists remotely.

#### // Stage 2: Setting Up the AGENTS.md Context File

The single most important thing you can do to improve agent output is give each agent a clear, written context file. [Peer-reviewed research at ICSE 2026](https://conf.researchr.org/details/icse-2026/designing-2026-papers/2/Improving-LLM-assisted-code-generation-through-the-use-of-architectural-documents-and) confirmed that incorporating architectural documentation into agent context produces measurable gains in functional correctness, architectural conformance, and code modularity. The `AGENTS.md` file is how you deliver that context reliably, at scale, across every session.

Create this file in your project root and commit it. Every agent reads it on session start. Different tools read different filenames — `AGENTS.md` (OpenAI Codex), `CLAUDE.md` (Claude Code), `AGENTS.md` (generic) — but the content matters more than the name.

```
# AGENTS.md
# Project context for AI coding agents
# Commit this to your repository root.
# Every agent that opens this project reads it first.

## Project Overview
Node.js/TypeScript REST API with a React frontend.
Stack: Node 20, Express 5, Prisma ORM, PostgreSQL, React 18, Vite.

## Build and Test Commands
npm run dev          # start dev server on port 3000
npm run build        # production build to dist/
npm run test         # run all tests (Vitest)
npm run test:watch   # watch mode
npm run lint         # ESLint and Prettier check
npm run db:migrate   # run pending Prisma migrations
npm run db:seed      # seed development data

## Architecture
- API routes:        src/routes/        one file per resource
- Business logic:    src/services/      never in route handlers
- Database access:   src/repositories/  never call Prisma directly from services
- Shared types:      src/types/index.ts

## Conventions
- All exported functions require JSDoc comments
- No console.log in committed code -- use src/utils/logger.ts
- Error handling: throw typed errors from services, catch in route handlers
- Branch naming: feat/, fix/, refactor/

## Prohibited Zones -- Do NOT modify unless explicitly told to
- src/auth/              (security team ownership, separate review process)
- prisma/migrations/     (only modify via npm run db:migrate)
- .env files             (never commit, never read outside config/)

## Current Worktree Task
Task:                 [FILL IN before starting the agent]
Branch:               [FILL IN]
Acceptance criteria:  [FILL IN]
```

The bottom section is what makes this file work per-worktree. Every time you create a new worktree, open `AGENTS.md` and fill in those three lines before starting the agent. This scopes the agent's work precisely and prevents it from wandering into areas it should not touch.

For Claude Code specifically, the native `-w` flag handles worktree creation and session start in one command:

```
# Create a worktree and start a Claude Code session inside it
claude --worktree feat/auth-redesign

# Short form
claude -w feat/auth-redesign

# With tmux panes for split-screen visibility
claude -w feat/auth-redesign --tmux
```

[`claude --worktree`](https://code.claude.com/docs/en/worktrees#start-claude-in-a-worktree) creates `.claude/worktrees/feat-auth-redesign/` on a branch called `worktree-feat-auth-redesign`, then starts the session inside it. The `.worktreeinclude` file (gitignore syntax) controls which gitignored files are automatically copied into new worktrees:

```
# .worktreeinclude -- place in your repo root
# Files to copy into every new worktree on creation
.env
.env.local
.env.development
```

#### // Stage 3: Running Multiple Agents at Once

When you need three or four agents running simultaneously, scripting the entire setup saves time and ensures consistency.

How to run: Save as `parallel-setup.sh`, run `chmod +x parallel-setup.sh`, then `./parallel-setup.sh feat/auth feat/api feat/dashboard`.

```
#!/usr/bin/env bash
# parallel-setup.sh
# Creates N worktrees for N parallel AI agents in one command
# Usage: ./parallel-setup.sh   ... 
# Example: ./parallel-setup.sh feat/auth feat/api feat/dashboard

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0   ... "
  echo "Example: $0 feat/auth feat/api feat/dashboard"
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_ROOT")"
MAIN_BRANCH="main"

echo "Setting up ${#@} parallel worktrees..."
git fetch origin 2>/dev/null || echo "(no remote -- skipping fetch)"

for BRANCH in "$@"; do
  SAFE="${BRANCH//\//-}"
  WT_PATH="${REPO_ROOT}/../${REPO_NAME}-${SAFE}"

  if [ -d "$WT_PATH" ]; then
    echo "Already exists: $WT_PATH (skipping)"
    continue
  fi

  # Create worktree on a new branch from main
  git worktree add -b "$BRANCH" "$WT_PATH" "$MAIN_BRANCH" 2>/dev/null || \
    git worktree add "$WT_PATH" "$BRANCH"

  # Copy environment files
  for f in .env .env.local; do
    [ -f "$REPO_ROOT/$f" ] && cp "$REPO_ROOT/$f" "$WT_PATH/$f"
  done

  echo "Created: $WT_PATH  (branch: $BRANCH)"
done

echo ""
echo "All worktrees:"
git worktree list
echo ""
echo "Open each path in a separate terminal or IDE window and start your agent."
echo "Remember to fill in the Task section of AGENTS.md in each worktree."
```

What this does: One command produces all the worktrees with environment files copied. Running `./parallel-setup.sh feat/auth feat/api feat/dashboard` gives you three isolated working directories in under five seconds. Open each in its own terminal tab, fill in `AGENTS.md`, and start the agents.

<iframe frameborder="0" src="https://22feb83616c7e88bc2d40c5e3fdba8f8.safeframe.googlesyndication.com/safeframe/1-0-45/html/container.html" title="3rd party ad content" width="360" height="300" allow="private-state-token-redemption;attribution-reporting" aria-label="Advertisement"></iframe>

## \# Keeping Worktrees From Drifting

The biggest long-term failure mode is not conflicts at creation time — it is drift. A worktree that runs for three days without syncing to **main** accumulates divergence that makes merging a project in itself.

Practitioners using Claude Code with worktrees in production are clear on this: after completing a checkpoint, pull and merge updates from the main branch — this prevents the worktree from drifting too far, which would result in massive, hard-to-resolve conflicts. The recommendation is to sync at the end of every significant agent session, not just before the PR.

The right strategy is rebase, not merge. Rebasing writes your branch's commits on top of the latest main, which keeps the history linear and makes the PR diff clean.

How to run: Save as `sync-worktree.sh`, run `chmod +x sync-worktree.sh`, then run `./sync-worktree.sh` from inside any worktree directory.

```
#!/usr/bin/env bash
# sync-worktree.sh
# Rebases the current worktree branch onto the latest main
# Run at checkpoints to prevent branch drift
# Usage (from inside the worktree): ./sync-worktree.sh [main-branch-name]
# Example: ./sync-worktree.sh main

set -euo pipefail

MAIN_BRANCH="${1:-main}"
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [ "$CURRENT_BRANCH" = "$MAIN_BRANCH" ]; then
  echo "Already on $MAIN_BRANCH -- nothing to sync."
  exit 0
fi

echo "Syncing '$CURRENT_BRANCH' onto '$MAIN_BRANCH'..."

# Reject if there is uncommitted work -- rebase requires a clean state
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "ERROR: Uncommitted changes detected."
  echo "Commit your progress first:"
  echo "  git add . && git commit -m 'checkpoint: agent progress'"
  exit 1
fi

# Fetch the latest remote state
git fetch origin

# Rebase this branch onto the latest main
# --autostash handles minor working tree differences automatically
git rebase "origin/$MAIN_BRANCH" --autostash

echo ""
echo "Done. '$CURRENT_BRANCH' is up to date with origin/$MAIN_BRANCH."
echo ""
echo "When ready to push:"
echo "  git push --force-with-lease"
echo ""
echo "Note: --force-with-lease is safer than --force."
echo "It refuses to push if someone else pushed to this branch since your last fetch."
```

What this does: The uncommitted-changes check before the rebase is an important safety measure. A rebase on a dirty tree produces a confusing state. `--autostash` handles minor differences. `--force-with-lease` on push is safer than `--force` because it refuses to overwrite remote work you have not seen yet.

The full merge lifecycle from agent completion to merged PR:

```
# Inside the worktree, after the agent finishes its task

# 1. Commit the agent's work
git add .
git commit -m "feat: implement OAuth2 + PKCE auth flow"

# 2. Sync with main before opening a PR
./sync-worktree.sh

# 3. Run tests to verify nothing broke in the sync
npm run test

# 4. Push the branch
git push --force-with-lease origin feat/auth-redesign

# 5. Open a PR via GitHub CLI or the web interface
gh pr create \
  --title "feat: OAuth2 + PKCE authentication" \
  --body "Implements OAuth2 per docs/auth-spec.md. All tests pass."

# 6. After the PR merges, clean up
cd ../myapp
./cleanup-worktree.sh feat/auth-redesign
```

<iframe frameborder="0" src="https://22feb83616c7e88bc2d40c5e3fdba8f8.safeframe.googlesyndication.com/safeframe/1-0-45/html/container.html" title="3rd party ad content" width="360" height="300" allow="private-state-token-redemption;attribution-reporting" aria-label="Advertisement"></iframe>

## \# The Complete Command Reference

Every git worktree command with real examples. Keep this section open while building your first workflow.

#### // Creating Worktrees

```
# Create a worktree on a new branch from main
git worktree add -b feat/payments ../myapp-payments main

# Check out an existing branch into a new worktree
git worktree add ../myapp-feat-auth feat/auth

# Detached HEAD -- useful for reproducing a bug at a specific commit
git worktree add --detach ../myapp-debug abc1234

# Track a remote branch directly
git worktree add ../myapp-hotfix origin/hotfix/login-crash
```

#### // Inspecting and Managing

```
# Show all worktrees with path, commit hash, and branch name
git worktree list

# Machine-readable output for use in scripts
git worktree list --porcelain

# Lock a worktree so prune does not remove it
# Use while an agent is running to protect against accidental cleanup
git worktree lock ../myapp-feat-auth --reason "agent-running"

# Release the lock
git worktree unlock ../myapp-feat-auth

# Move a worktree directory (close any open editors first)
git worktree move ../myapp-feat-auth ../worktrees/auth-redesign
```

#### // Cleanup

```
# Remove a worktree cleanly -- the branch is preserved in git
git worktree remove ../myapp-feat-auth

# Force remove even with uncommitted changes
# Only use this when you are certain the work can be discarded
git worktree remove --force ../myapp-feat-auth

# Clean up metadata for worktrees manually deleted with rm -rf
git worktree prune

# Preview what would be pruned without actually pruning
git worktree prune --dry-run

# Fix worktree references after moving the .git directory
git worktree repair
```

<iframe frameborder="0" src="https://22feb83616c7e88bc2d40c5e3fdba8f8.safeframe.googlesyndication.com/safeframe/1-0-45/html/container.html" title="3rd party ad content" width="360" height="300" allow="private-state-token-redemption;attribution-reporting" aria-label="Advertisement"></iframe>

## \# Common Errors and Fixes

| **Error Message** | **Cause** | **Fix** |
| --- | --- | --- |
| `fatal: 'feat/auth' is already checked out` | Branch in use by another worktree | Use a different branch, or remove the existing worktree first |
| `fatal: <path> already exists` | Target directory exists | Delete it or choose a different path |
| `error: '...' is a main worktree` | Tried to remove the main checkout | Only linked worktrees can be removed |
| `error: worktree has modified files` | Uncommitted changes present | Commit the work, or use `--force` to discard |
| Worktree appears in `git worktree list` after `rm -rf` | Metadata not cleaned up | Run `git worktree prune` |

## \# Conclusion

Git worktrees are not advanced Git arcana. They are a core infrastructure primitive that became essential the moment AI coding agents started running in parallel on the same codebases.

The workflow in this article is not theoretical. It is what Tamir Dresher's team ran at the Microsoft Global Hackathon. It is what practitioners with Claude Code, **[Cursor](https://www.cursor.com/)**, and **[Codex](https://openai.com/codex)** are documenting across GitHub and Medium right now. It is the pattern the [agentic coding community](https://www.mindstudio.ai/blog/git-worktrees-parallel-ai-coding-agents) has converged on for one reason: it is the simplest thing that reliably solves the problem it was built to solve.

The setup cost is low. The four scripts in this article cover the full lifecycle — create, sync, and clean up — in about 120 lines of bash. The conceptual model is simple: one task, one branch, one worktree, one agent. The payoff is that you can run multiple agents in parallel without spending your afternoon untangling conflicts that neither agent created intentionally.

If you are already using AI coding tools and not using worktrees, set them up on your next project. The `create-worktree.sh` script is a ten-second start. If you are building a team workflow around AI agents, `AGENTS.md` and the parallel setup script move you from ad-hoc sessions to a repeatable process that scales.

The model writes the code. Your job is to create the conditions where it can do that cleanly, in parallel, without getting in its own way.  

****[Shittu Olumide](https://www.linkedin.com/in/olumide-shittu/)**** is a software engineer and technical writer passionate about leveraging cutting-edge technologies to craft compelling narratives, with a keen eye for detail and a knack for simplifying complex concepts. You can also find Shittu on [Twitter](https://twitter.com/Shittu_Olumide_).