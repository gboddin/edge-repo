#!/bin/bash
DISTCACHE_VERSION=1.4.5
APR_VERSION=1.5.2
APR_UTIL_VERSION=1.5.4

# Build dist-cache
spectool -g -C SOURCES SPECS/distcache.spec
yum-builddep -y --nogpgcheck SPECS/distcache.spec 
rpmbuild  --quiet --define "rpmrel 24" --define "_topdir `pwd`" -ba SPECS/distcache.spec > ${LOGFILE}
rpm -Uvh RPMS/$(uname -m)/distcache*-${DISTCACHE_VERSION}*.$(uname -m).rpm

# Build apr :
spectool -g -C SOURCES SPECS/apr.spec
yum-builddep -y --nogpgcheck SPECS/apr.spec 
rpmbuild  --quiet --define "rpmrel 1" --define "_topdir `pwd`" -ba SPECS/apr.spec > ${LOGFILE}
rpm -Uvh RPMS/$(uname -m)/apr*-${APR_VERSION}*.$(uname -m).rpm

# Build apr-utils :

spectool -g -C SOURCES SPECS/apr-util.spec
yum-builddep -y --nogpgcheck SPECS/apr-util.spec 
rpmbuild --quiet --define "rpmrel 1" --define "_topdir `pwd`"  -ba  SPECS/apr-util.spec > ${LOGFILE}
rpm -Uvh RPMS/$(uname -m)/apr-util*-${APR_UTIL_VERSION}*.$(uname -m).rpm

# Build httpd :
cat SPECS/httpd.spec.tpl |sed "s/TPL_HTTPD_VERSION/$APACHE_VERSION/g" > SPECS/httpd.spec
spectool -g -C SOURCES SPECS/httpd.spec
yum-builddep -y SPECS/httpd.spec
rpmbuild --quiet --define "rpmrel ${APACHE_RELEASE}" --define "_topdir `pwd`" -ba SPECS/httpd.spec > ${LOGFILE}
