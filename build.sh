#!/bin/bash
if [ -z $PACKAGE ] && [ -z $1 ] ; then
  echo "Either need to specify package as argument or set the $PACKAGE environment variable"
  exit 1
fi
[ -z $PACKAGE ] && PACKAGE=$1

# Replaces version tokens if needed :
[ -f SPEC/${PACKAGE}.spec.tpl ] && sed -i 's/TPL_PACKAGE_VERSION/${PACKAGE_VERSION}/g' SPEC/${PACKAGE}.spec.tpl > SPEC/${PACKAGE}.spec

# Install sources :
spectool -g -C SOURCES SPECS/${PACKAGE}.spec

# Install build depedencies :
${CMD_BUILD_DEP} -y --nogpgcheck SPECS/${PACKAGE}.spec 

# Build the package :
rpmbuild  --quiet --define "rpmrel ${RPM_RELEASE}" --define "_topdir `pwd`" -ba SPECS/${PACKAGE}.spec > ${LOGFILE}
