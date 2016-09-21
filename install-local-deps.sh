#!/bin/bash

# Quit on fail :
set -e

: ${DISTRO:="$1"} 
[ -z ${DISTRO} ] && echo "Please speecify a distro" && exit 1
: ${PACKAGE:="$2"} 
[ -z ${PACKAGE} ] && echo "Please speecify a package" && exit 1

# Commen env
. common.env

# Install proprietary depedencies :

[ ! -z "${THIRD_PARTY_RPMS}" ] && for RPM in ${THIRD_PARTY_RPMS} ; do
  echo "Checking if $RPM exists ..."
  [ ! -f "$RPM" ] && echo "$RPM not found" && continue
  echo "Installing $RPM"
  $PROOT_CMD yum -y --nogpgcheck install ${RPM}

  # Fix Oracle instant client missing link

  echo $RPM|grep -q "^oracle-instantclient12.1-devel" && ( \
    $PROOT_CMD ln -s /usr/lib/oracle/12.1/client64/lib/libnnz12.so /usr/lib/oracle/12.1/client64/lib/libnnz.so && \
    ln -s /usr/lib/oracle  /usr/lib64/oracle
   ) || /bin/true
done
