#!/bin/bash

# Stop on error :
set -e

: ${DISTRO:="$1"} 
[ -z ${DISTRO} ] && echo "Please speecify a distro" && exit 1

# Common env
. common.env

# Prepare proot environment

if [ ! -d ${DISTRO} ] ; then 
  wget -c "https://github.com/gboddin/upsalter/releases/download/0.6.0-alpha1/${DISTRO}-rootfs-buildenv.tar.bz2" 
  mkdir -p ${DISTRO}
  tar -C ${DISTRO} -xjf ${DISTRO}-rootfs-buildenv.tar.bz2 || exit 1
fi

echo "Enabling third-party repos :"
${CMD_PROOT} rpm -ivh http://repo.siwhine.net/${DISTRO}/edge-repo-latest.rpm
echo installed > ${DISTRO}/rootfs-installed 
