#!/bin/bash
echo Downloading deps :
[ ! -z ${EPEL} ] && rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${EPEL}.noarch.rpm
echo Downloading common deps :
yum install wget git tar rpm-build rpmdevtools make -y
[ ! -z ${ORACLE_OCI_RPM} ] && yum -y --nogpgcheck install ${ORACLE_OCI_RPM}
