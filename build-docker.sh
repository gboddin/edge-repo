#!/bin/bash
set -e

[ -z $1 ] && echo "Please specify a distory (5/6/7)"
[ -z $2 ] && echo "Please specify a package"

EL=$1
DIST=el${EL}
PACKAGE=$2
CONTAINER=${PACKAGE}_${EL}_centos_build

# reset log files :
cat /dev/null > RPMS/build.log
cat /dev/null > RPMS/root.log
cat /dev/null > RPMS/trace.log
cat /dev/null > SRPMS/build.log
cat /dev/null > SRPMS/root.log
cat /dev/null > SRPMS/trace.log

# Reset container if running :
if [ ! -z $(docker ps -qaf name=${CONTAINER}) ] ; then
  echo "Found previous build instance, killing ..."
  docker rm ${CONTAINER} -f
fi

# Build the image if missing :
if [ -z $(docker images -q el7-mock) ]; then
  echo "Building base mock image"
  docker build -t el7-mock conf/ 
fi

echo "Building ${PACKAGE}..."

docker create --privileged=true --name ${CONTAINER} -v $(pwd):/mock/build el7-mock bash -c 'tail -f /mock/build/{S,}RPMS/*.log'
docker start ${CONTAINER} && sleep 1 
docker exec ${CONTAINER} spectool -g -C /mock/build/SOURCES/${PACKAGE} /mock/build/SPECS/${PACKAGE}.spec
docker exec -u ${UID} ${CONTAINER}  /usr/bin/mock -r edge-${EL}-x86_64 --spec=/mock/build/SPECS/${PACKAGE}.spec --sources=/mock/build/SOURCES/${PACKAGE} --resultdir=/mock/build/SRPMS --buildsrpm
docker exec -u ${UID} ${CONTAINER} /usr/bin/mock --clean -r edge-${EL}-x86_64  -D "dist .${DIST}" --resultdir=/mock/build/RPMS --rebuild /mock/build/SRPMS/$(ls -1utr SRPMS/|grep ^${PACKAGE}-.*src\.rpm$|head -1)
docker rm ${CONTAINER} -f
