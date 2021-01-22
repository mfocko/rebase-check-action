#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

WARNING_MSG_1 = (
    "Your branch is not up to date with upstream/master. "
    "SHA of the last commit of upstream/master: {upstream} "
    "Please, rebase!"
)

WARNING_MSG_2 = (
    "Zuul merged the master, which means your branch is not up to date with upstream/master. "
    "Please, rebase!"
)


def main():
    path = str(Path.cwd().absolute())

    last_commit_subject = subprocess.run(
        ["git", "log", "--format=%s", "-1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=path,
    ).stdout.decode()
    print(f"::group::Last commit subject\n{last_commit_subject.strip()}\n::endgroup::")

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

    print(f"::group::Upstream hash\n{upstream_hash}\n::endgroup::")
    print(f"::group::Local hashes\n{local_hashes[:3]}\n::endgroup::")

    if upstream_hash in local_hashes:
        return 0
    print("::error:: " + WARNING_MSG_1.format(upstream=upstream_hash))
    return 1


if __name__ == "__main__":
    exit(main())
