#!/bin/bash
echo Enabling third-party repos :
[ ! -z ${EPEL} ] && rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${EPEL}.noarch.rpm
rpm -ivh http://repo.siwhine.net/${DISTRO}/edge-repo-latest.rpm

echo Downloading common deps :
yum install wget git tar rpm-build rpmdevtools make -y
[ ! -z "${THIRD_PARTY_RPMS}" ] && for RPM in ${THIRD_PARTY_RPMS} ; do
  yum -y --nogpgcheck install ${RPM}
done
