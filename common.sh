#!/bin/bash
echo Downloading common deps :
yum install wget git tar -y
echo Downloading deps :
rpm -ivh ${EPEL} 
