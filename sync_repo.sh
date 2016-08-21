#!/bin/bash
rsync --ignore-existing -arvce "ssh -i deploy.key -o StrictHostKeyChecking=no" RPMS/ ${RSYNC_REPO}:/var/www/html/repo/${DISTRO}/RPMS/
rsync --ignore-existing -arvce "ssh -i deploy.key -o StrictHostKeyChecking=no" SRPMS/ ${RSYNC_REPO}:/var/www/html/repo/${DISTRO}/SRPMS/
