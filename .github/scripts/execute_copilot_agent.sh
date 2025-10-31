#!/usr/bin/env bash
# Helper script used by the Copilot agent workflow.
# This script attempts to run a Copilot coding agent container/CLI that consumes
# knowledge-database/claude-prompt.md and knowledge-database/analysis-data.json
# and writes generated files to knowledge-database/concepts/.
# If no official CLI is available, the script falls back to printing instructions
# and exiting non-zero so the workflow fails clearly.

set -euo pipefail

REPO=${REPO:-"$GITHUB_REPOSITORY"}
BRANCH=${BRANCH:-"copilot-kb-synthesis-$(date +%s)"}
COMMIT_METHOD=${COMMIT_METHOD:-"pull_request"}

# Ensure output directory exists
mkdir -p knowledge-database/concepts

# Preferred: run an official Copilot agent container (replace with real image when available)
# Example (this image is a placeholder - replace with the real Copilot agent image if present):
COPILOT_IMAGE="ghcr.io/github/copilot/agent:latest"

# If the copilot-agent CLI or container is available, run it. Otherwise fail with helpful message.
if command -v copilot-agent >/dev/null 2>&1; then
  echo "Running copilot-agent CLI"
  copilot-agent \
    --input-prompt knowledge-database/claude-prompt.md \
    --analysis knowledge-database/analysis-data.json \
    --output-dir knowledge-database/concepts \
    --mode non-interactive

elif docker image inspect "$COPILOT_IMAGE" >/dev/null 2>&1 || docker pull "$COPILOT_IMAGE" >/dev/null 2>&1; then
  echo "Running copilot-agent container $COPILOT_IMAGE"
  docker run --rm \
    -v "$(pwd)":/workspace \
    -w /workspace \
    -e GITHUB_TOKEN="$GITHUB_TOKEN" \
    $COPILOT_IMAGE \
    copilot-agent --input-prompt knowledge-database/claude-prompt.md --analysis knowledge-database/analysis-data.json --output-dir knowledge-database/concepts --mode non-interactive

else
  echo "No copilot-agent CLI or container available in runner." >&2
  echo "Falling back to guidance: please run Claude Code in your editor using these files:" >&2
  echo " - knowledge-database/claude-prompt.md" >&2
  echo " - knowledge-database/analysis-data.json" >&2
  echo "Expect output to be created under knowledge-database/concepts/" >&2
  echo "To enable full automation, install or provide a copilot-agent CLI or container image at $COPILOT_IMAGE" >&2
  exit 2
fi

# If the agent produced files, commit or open a PR depending on COMMIT_METHOD
if [ -n "$(git status --porcelain)" ]; then
  git config user.name "github-actions[bot]"
  git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

  if [ "$COMMIT_METHOD" = "commit" ]; then
    echo "Committing directly to current branch"
    git add knowledge-database/concepts || true
    git commit -m "chore(kb): add Copilot-generated knowledge base" || true
    git push origin HEAD
  else
    echo "Creating new branch and opening a pull request"
    git checkout -b "$BRANCH"
    git add knowledge-database/concepts || true
    git commit -m "feat(kb): add Copilot-generated knowledge base" || true
    git push --set-upstream origin "$BRANCH"

    # Create a PR using gh (GitHub CLI) if available
    if command -v gh >/dev/null 2>&1; then
      gh pr create --title "feat(kb): Copilot-generated knowledge base" --body "Automated Copilot agent run: generated concept files from Claude prompt." --base dev --head "$BRANCH"
    else
      echo "gh CLI not available - cannot create PR automatically. Branch pushed: $BRANCH" >&2
      echo "Please open a PR against dev from branch: $BRANCH" >&2
      exit 0
    fi
  fi
else
  echo "No changes produced by Copilot agent - nothing to commit." >&2
fi
