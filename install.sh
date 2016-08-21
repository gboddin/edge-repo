#!/bin/bash
EPEL=`echo ${DISTRO} | sed "s/centos-//"`
echo Downloading deps :
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${EPEL}.noarch.rpm
echo Downloading common deps :
yum install wget git tar rpm-build rpmdevtools make -y
[ ! -z ${ORACLE_OCI_RPM} ] && yum -y --nogpgcheck localinstall ${ORACLE_OCI_RPM}
