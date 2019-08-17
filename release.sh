#!/bin/bash

cd index || exit
git init
git checkout -b gh-pages
git add .
git commit -m "Release $(date --rfc-3339=sec)"
git remote add origin https://github.com/otamachan/rospy3.git
git push -f origin gh-pages
rm .git -rf
