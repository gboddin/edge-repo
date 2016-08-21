#!/bin/bash
[ ! -z ${ORACLE_OCI_RPM} ] && rpm -ivh ${ORACLE_OCI_RPM}
EPEL=`echo ${DISTRO} | sed "s/centos-//"`
echo Downloading deps :
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${EPEL}.noarch.rpm
echo Downloading common deps :
yum install /sbin/service /etc/mime.types libdb wget git tar rpm-build rpmdevtools make -y
