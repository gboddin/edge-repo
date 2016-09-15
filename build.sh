#!/bin/bash
if [ -z $PACKAGE ] && [ -z $1 ] ; then
  echo "Either need to specify package as argument or set the $PACKAGE environment variable"
  exit 1
fi
[ -z $PACKAGE ] && PACKAGE=$1

# If SOURCES dir is not there, create it
[ ! -d `pwd`/SOURCES/${PACKAGE} ] && mkdir -p `pwd`/SOURCES/${PACKAGE}

# Install sources :
spectool -g -C SOURCES/${PACKAGE} SPECS/${PACKAGE}.spec

# Install build depedencies :
${CMD_BUILD_DEP} -y --nogpgcheck SPECS/${PACKAGE}.spec 

# Build the package :
rpmbuild  ${CONFIG_FLAGS} --define "_sourcedir `pwd`/SOURCES/${PACKAGE}" --define "_topdir `pwd`" ${CONFIG_FLAGS} -ba SPECS/${PACKAGE}.spec > ${LOGFILE}
