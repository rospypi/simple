#!/bin/bash

cd index || exit
BRANCH="$(uname -s)"
git init
git checkout -b "$BRANCH"
git add .
git commit -m "Release $(date --rfc-3339=sec)"
git remote add origin https://github.com/otamachan/rospy3.git
git push -f origin "$BRANCH"
rm -rf .git
