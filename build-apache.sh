#!/bin/bash
DISTCACHE_VERSION=1.4.5-23
APR_VERSION=1.5.2
APR_UTIL_VERSION=1.5.4

# Get packages 
wget -c https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/18/Fedora/source/SRPMS/d/distcache-${DISTCACHE_VERSION}.src.rpm -O SRPMS/distcache-${DISTCACHE_VERSION}.src.rpm 

# Build dist-cache
yum-builddep -y --nogpgcheck SRPMS/distcache-${DISTCACHE_VERSION}.src.rpm
rpmbuild --quiet --rebuild  --define "_topdir `pwd`"  SRPMS/distcache-${DISTCACHE_VERSION}.src.rpm > ${LOGFILE}
rpm -Uvh RPMS/$(uname -m)/distcache*-${DISTCACHE_VERSION}.$(uname -m).rpm

# Build apr :
spectool -g -C SOURCES SPECS/apr.spec
yum-builddep -y --nogpgcheck SPECS/apr.spec 
rpmbuild  --quiet --define "_topdir `pwd`" -ba SPECS/apr.spec > ${LOGFILE}
rpm -Uvh RPMS/$(uname -m)/apr*-${APR_VERSION}*.$(uname -m).rpm

# Build apr-utils :

spectool -g -C SOURCES SPECS/apr-util.spec
yum-builddep -y --nogpgcheck SPECS/apr-util.spec 
rpmbuild --quiet --define "_topdir `pwd`"  -ba  SPECS/apr-util.spec > ${LOGFILE}
rpm -Uvh RPMS/$(uname -m)/apr-util*-${APR_UTIL_VERSION}*.$(uname -m).rpm

# Build httpd :
cat SPECS/httpd.spec.tpl |sed "s/TPL_HTTPD_VERSION/$APACHE_VERSION/g" > SPECS/httpd.spec
spectool -g -C SOURCES SPECS/httpd.spec
yum-builddep -y SPECS/httpd.spec
rpmbuild --quiet --define "_topdir `pwd`" -ba SPECS/httpd.spec > ${LOGFILE}
