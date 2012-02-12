#!/bin/bash          
# Github Syncro Script

git pull
git add --all
git commit -m "Auto-Git-Backup $(date "+%d.%m.%Y %H:%M "|sed -e ' s/\"/\\\"/g' )"
git push -u origin master
