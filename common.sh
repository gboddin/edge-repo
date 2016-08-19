#!/bin/bash
'Downloading common deps :'
yum install wget git tar -ys
echo Downloading deps :
rpm -ivh ${EPEL} 
