#!/bin/bash
EPEL=`sed "s/${DISTRO}-//"`
[ -z $EPEL ] && rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${EPEL}.noarch.rpm
echo Downloading common deps :
yum install wget git tar -y
echo Downloading deps :
rpm -ivh ${EPEL} 
