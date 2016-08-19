#!/bin/bash
DISTCACHE_VERSION=1.4.5-23
APR_VERSION=1.5.2
APR_UTIL_VERSION=1.5.4

# Get packages 
wget -c https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/18/Fedora/source/SRPMS/d/distcache-${DISTCACHE_VERSION}.src.rpm -O SRPMS/distcache-${DISTCACHE_VERSION}.src.rpm 
wget -c http://www.apache.si/apr/apr-${APR_VERSION}.tar.bz2 -O SOURCES/apr-${APR_VERSION}.tar.bz2
wget -c  http://www.apache.si/apr/apr-util-${APR_UTIL_VERSION}.tar.bz2 -O SOURCES/apr-util-${APR_UTIL_VERSION}.tar.bz2

# Build dist-cache
yum-builddep -y --nogpgcheck SRPMS/distcache-${DISTCACHE_VERSION}.src.rpm
rpmbuild --rebuild  --define "_topdir `pwd`"  SRPMS/distcache-${DISTCACHE_VERSION}.src.rpm
rpm -Uvh RPMS/$(uname -m)/distcache*-${DISTCACHE_VERSION}.$(uname -m).rpm

# Build apr :
rpmbuild  --define "_topdir `pwd`" -ts SOURCES/apr-${APR_VERSION}.tar.bz2
yum-builddep --nogpgcheck -y SRPMS/apr-util*-${APR_UTIL_VERSION}*.$(uname -m).src.rpm
rpmbuild  --define "_topdir `pwd`" -tb SOURCES/apr-${APR_VERSION}.tar.bz2
rpm -Uvh RPMS/$(uname -m)/apr*-${APR_VERSION}*.$(uname -m).rpm

# Build apr-utils :

rpmbuild --define "_topdir `pwd`"  -ts  SOURCES/apr-util-${APR_UTIL_VERSION}.tar.bz2
yum-builddep -y --nogpgcheck SRPMS/$(uname -m)/apr-util*-${APR_UTIL_VERSION}*.$(uname -m).src.rpm
rpmbuild --define "_topdir `pwd`"  -tb  SOURCES/apr-util-${APR_UTIL_VERSION}.tar.bz2
rpm -Uvh RPMS/$(uname -m)/apr-util*-${APR_UTIL_VERSION}*.$(uname -m).rpm

wget -c "https://www.apache.org/dist/httpd/httpd-${APACHE_VERSION}.tar.bz2" -O SOURCES/httpd-${APACHE_VERSION}.tar.bz2 
cat SPECS/httpd.spec.tpl |sed "s/TPL_HTTPD_VERSION/$APACHE_VERSION/g" > SPECS/httpd.spec
rpmbuild --define "_topdir `pwd`" -bs SPECS/httpd.spec
yum-builddep -y SPECS/httpd.spec
rpmbuild --define "_topdir `pwd`" -bb SPECS/httpd.spec
