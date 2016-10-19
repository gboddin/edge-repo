#!/bin/bash
set -e
EL=$1
DIST=el${EL}
PACKAGE=$2
CONTAINER=${PACKAGE}_${EL}_centos_build
docker build -t el7-mock conf/ 
docker create --privileged=true --name ${CONTAINER} -v $(pwd):/mock/build el7-mock bash -c 'while /bin/true ; do sleep 10 ; done'
docker start ${CONTAINER} && sleep 1 
docker exec ${CONTAINER} spectool -g -C /mock/build/SOURCES/${PACKAGE} /mock/build/SPECS/${PACKAGE}.spec
docker exec -u ${UID} ${CONTAINER}  /usr/bin/mock -r edge-${EL}-x86_64 --spec=/mock/build/SPECS/${PACKAGE}.spec --sources=/mock/build/SOURCES/${PACKAGE} --resultdir=/mock/build/SRPMS --buildsrpm
docker exec -u ${UID} ${CONTAINER} /usr/bin/mock --clean -r edge-${EL}-x86_64  -D "dist .${DIST}" --resultdir=/mock/build/RPMS --rebuild /mock/build/SRPMS/$(ls -1utr SRPMS/|grep ^${PACKAGE}-*src\.rpm$|head -1)
docker rm ${CONTAINER} -f
