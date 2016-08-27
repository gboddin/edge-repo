#!/bin/bash
ORIGIN=$1
[ -z $1 ] && ORIGIN=dev
echo "Syncing branches ..."
ls SPECS/|sed 's/.spec$//g' |grep -v edge-repo|while read soft; do
  git checkout $soft && git merge master && git push $ORIGIN
  git checkout master && git merge $soft
done
git push $ORIGIN
