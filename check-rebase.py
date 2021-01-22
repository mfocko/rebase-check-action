#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

WARNING_MSG_1 = (
    "Your branch is not up to date with upstream's main branch. "
    "SHA of the last commit on main branch: {upstream} "
    "Please, rebase!"
)

WARNING_MSG_2 = (
    "Zuul merged the main branch, which means your branch is not up to date with the main branch. "
    "Please, rebase!"
)


def wrap_in_group(group_name, text):
    return f"::group::{group_name}\n{text}\n::endgroup::\n"


def main():
    path = str(Path.cwd().absolute())

    last_commit_subject = subprocess.run(
        ["git", "log", "--format=%s", "-1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=path,
    ).stdout.decode()
    print(wrap_in_group("Last commit subject", last_commit_subject.strip()))

    if "Merge commit" in last_commit_subject:
        print("::error " + WARNING_MSG_2)
        return 2

    local_hashes = (
        subprocess.run(
            ["git", "log", "--max-count=100", "--format=%H"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=path,
        )
        .stdout.decode()
        .split()
    )

    upstream_hash = (
        subprocess.run(
            ["git", "ls-remote", str(sys.argv[1]), "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=path,
        )
        .stdout.decode()
        .split()[0]
    )

    print(wrap_in_group("Upstream hash", upstream_hash))
    print(wrap_in_group("Local hashes", local_hashes[:3]))

    if upstream_hash in local_hashes:
        return 0
    print("::error:: " + WARNING_MSG_1.format(upstream=upstream_hash))
    return 1


if __name__ == "__main__":
    exit(main())
