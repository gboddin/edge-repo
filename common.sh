#!/bin/bash
echo Downloading common deps :
yum install wget git tar -i
echo Downloading deps :
rpm -ivh ${EPEL} 
