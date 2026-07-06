#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

def run_command(command):
    """Runs a system command and returns stdout, or raises an error on failure."""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}")
        print(f"Exit code: {e.returncode}")
        print(f"Error output:\n{e.stderr.strip()}")
        sys.exit(1)

def main():
    # 1. Check if git is installed and if this is a git repository
    try:
        run_command(["git", "rev-parse", "--is-inside-work-tree"])
    except SystemExit:
        print("Error: The current directory is not a Git repository.")
        sys.exit(1)

    # 2. Check if there are any changes (tracked or untracked)
    status = run_command(["git", "status", "--porcelain"])
    if not status:
        print("No changes to commit. Everything is up-to-date!")
        sys.exit(0)

    print("Found the following changes:")
    print(status)
    print("-" * 40)

    # 3. Determine the commit message
    if len(sys.argv) > 1:
        commit_message = " ".join(sys.argv[1:])
    else:
        # Prompt user or generate an automatic message
        user_input = input("Enter commit message (press Enter for default): ").strip()
        if user_input:
            commit_message = user_input
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Auto-commit: updates as of {timestamp}"

    print(f"Using commit message: '{commit_message}'")

    # 4. Stage all changes
    print("Staging all changes...")
    run_command(["git", "add", "."])

    # 5. Commit changes
    print("Committing changes...")
    run_command(["git", "commit", "-m", commit_message])

    # 6. Push to main branch
    # Note: We push to 'main'. If the remote tracking branch is set or default is origin main:
    print("Pushing to remote repository (branch: main)...")
    run_command(["git", "push", "origin", "main"])

    print("Successfully completed: git add, commit, and push!")

if __name__ == "__main__":
    main()
