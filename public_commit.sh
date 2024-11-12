#!/bin/bash

# Hardcoded variables
BRANCH_NAME="public-share"
REMOTE_NAME="public"
REMOTE_URL="https://github.com/mdeacey/profile_rewriter.git"

# Function to run a command and handle errors
run_command() {
    if ! "$@"; then
        echo "Error while running command: $*" >&2
        exit 1
    fi
}

# Check if the remote exists
if ! git remote | grep -q "^${REMOTE_NAME}$"; then
    echo "Adding remote '${REMOTE_NAME}'..."
    run_command git remote add ${REMOTE_NAME} ${REMOTE_URL}
else
    echo "Remote '${REMOTE_NAME}' already exists."
fi

# Detach from the current branch if it's public-share
current_branch=$(git branch --show-current)
if [[ "$current_branch" == "$BRANCH_NAME" ]]; then
    echo "Detaching from the current branch '${BRANCH_NAME}'..."
    run_command git checkout main
fi

# Remove the local public-share branch if it exists
if git branch --list | grep -q "${BRANCH_NAME}"; then
    echo "Removing existing local branch '${BRANCH_NAME}'..."
    run_command git branch -D ${BRANCH_NAME}
fi

# Remove the remote public-share branch if it exists
if git ls-remote --heads ${REMOTE_NAME} | grep -q "refs/heads/${BRANCH_NAME}"; then
    echo "Removing existing remote branch '${BRANCH_NAME}'..."
    run_command git push ${REMOTE_NAME} --delete ${BRANCH_NAME}
fi

# Create and switch to an orphan branch
echo "Creating orphan branch '${BRANCH_NAME}'..."
run_command git checkout --orphan ${BRANCH_NAME}

# Stage all files
echo "Adding files to the new branch..."
run_command git add .

# Commit files
echo "Committing files..."
run_command git commit -m "Initial commit for public share"

# Force push to remote
echo "Force pushing '${BRANCH_NAME}' to '${REMOTE_NAME}:main'..."
run_command git push ${REMOTE_NAME} ${BRANCH_NAME}:main --force

echo "Branch '${BRANCH_NAME}' successfully pushed to '${REMOTE_NAME}:main'."
