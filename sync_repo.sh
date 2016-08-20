#!/bin/bash
rsync -arvce "ssh -i deploy.key -o StrictHostKeyChecking=no" RPMS/$(uname -m)/ ${RSYNC_REPO}:/var/www/html/repo/${DISTRO}/RPMS/$(uname -m)/
rsync -arvce "ssh -i deploy.key -o StrictHostKeyChecking=no" SRPMS/ ${RSYNC_REPO}:/var/www/html/repo/${DISTRO}/SRPMS/
