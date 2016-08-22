#!/bin/bash
# Build rhel rpm repo helper
[ -z ${EPEL} ] && exit 0
spectool -g -C SOURCES SPECS/edge-repo-${EPEL}.spec
yum-builddep -y --nogpgcheck SPECS/edge-repo-${EPEL}.spec 
rpmbuild  --quiet --define "rpmrel 3" --define "_topdir `pwd`" -ba SPECS/edge-repo-${EPEL}.spec > ${LOGFILE}
