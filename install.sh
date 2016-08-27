#!/bin/bash

# Enable 3rd party repos

echo Enabling third-party repos :
[ ! -z ${EPEL} ] && rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${EPEL}.noarch.rpm
rpm -ivh http://repo.siwhine.net/${DISTRO}/edge-repo-latest.rpm || exit 1

# Install proprietary depedencies :

[ ! -z "${THIRD_PARTY_RPMS}" ] && for RPM in ${THIRD_PARTY_RPMS} ; do
  yum -y --nogpgcheck install ${RPM} || exit 1

  # Fix Oracle instant client missing link

  echo $RPM|grep -q "^oracle-instantclient12.1-devel" && ( \
    ln -s /usr/lib/oracle/12.1/client64/lib/libnnz12.so /usr/lib/oracle/12.1/client64/lib/libnnz.so && \
    ln -s /usr/lib/oracle  /usr/lib64/oracle
   ) || /bin/true

done

exit 0
