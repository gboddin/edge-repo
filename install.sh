#!/bin/bash
EPEL=`echo ${DISTRO} | sed "s/centos-//"`
echo Downloading deps :
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${EPEL}.noarch.rpm
echo Downloading common deps :
yum install /etc/mime.types wget git tar rpm-build make -y
