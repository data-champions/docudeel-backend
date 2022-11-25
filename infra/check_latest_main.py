#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A script raising error if latest version of main branch is not used.
"""
import subprocess
import sys


def run_bash(command: str) -> None:
    process = subprocess.run(command, shell=True,
                             check=True,
                             capture_output=True)
    out = process.stdout.decode('utf-8').strip()
    return out


def warn_if_changes_not_staged() -> None:
    if "Changes not staged" in run_bash("git status"):
        print_red_and_exit("Commit not staged changes")


def print_red_and_exit(message: str) -> None:
    # ref how-do-i-print-colored-text-to-the-terminal-in-python
    CRED = "\033[91m"
    CEND = "\033[0m"
    print(CRED + message + CEND)
    # -1 exits script with error
    sys.exit(-1)


def check_latest_version_of_main_is_used() -> None:
    warn_if_changes_not_staged()
    get_latest_main = """git checkout main --quiet && \
                         git log -n 1 --pretty=format:"%H" && \
                         git checkout - --quiet"""
    latest_commit = run_bash(get_latest_main).splitlines()[-1]
    get_br_with_latest = f"git branch --contains {latest_commit}"
    updated_branches = run_bash(get_br_with_latest).splitlines()
    current_branch = run_bash("git rev-parse --abbrev-ref HEAD")
    branches = [
        update_branch
        for update_branch in updated_branches
        if current_branch in update_branch
    ]
    if not branches:
        print_red_and_exit("Merge latest version of main before xxproceeding!")


if __name__ == "__main__":
    check_latest_version_of_main_is_used()
