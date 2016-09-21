#!/bin/bash

# Stop on error :
set -e

# Parse arguments :

: ${DISTRO:="$1"} 
[ -z ${DISTRO} ] && echo "Please speecify a distro" && exit 1
: ${PACKAGE:="$2"} 
[ -z ${PACKAGE} ] && echo "Please speecify a package" && exit 1


# Common env
. common.env

# If SOURCES dir is not there, create it
[ ! -d ${DISTRO}/SOURCES/${PACKAGE} ] && mkdir -p ${DISTRO}/SOURCES/${PACKAGE}

# Install sources :
echo "Downloading sources for ${PACKAGE}..."
${CMD_PROOT} spectool -g -C SOURCES/${PACKAGE} SPECS/${PACKAGE}.spec

# Install build depedencies :
echo "Install build depedencies for ${PACKAGE}..."
${CMD_PROOT} ${CMD_BUILD_DEP} -y --nogpgcheck SPECS/${PACKAGE}.spec 

# Build the package :
echo "Building ${PACKAGE} RPM..."
${CMD_PROOT} rpmbuild  ${CONFIG_FLAGS} --define "_sourcedir /root/build/SOURCES/${PACKAGE}" --define "_topdir /root/build" ${CONFIG_FLAGS} -ba SPECS/${PACKAGE}.spec > ${LOGFILE}
