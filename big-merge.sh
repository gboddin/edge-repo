#!/bin/bash
echo "Syncing branches ..."
ls SPECS/|sed 's/.spec$//g' |grep -v edge-repo|while read soft; do
  git checkout $soft && git merge --squash master 
  git checkout master && git merge --squash $soft
done
