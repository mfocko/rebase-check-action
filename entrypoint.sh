#!/bin/bash

cd $GITHUB_WORKSPACE;
/check-rebase.py "https://github.com/$GITHUB_REPOSITORY.git"
