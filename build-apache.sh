#!/bin/bash
APACHE_VERSION=2.4.23
DISTCACHE_VERSION=1.4.5-23
APR_VERSION=1.5.2
APR_UTIL_VERSION=1.5.4

echo Downloading deps :
rpm -ivh  http://dl.fedoraproject.org/pub/epel/6/$(uname -m)/epel-release-6-8.noarch.rpm
yum install tar expat-devel freetds-devel db4-devel rpm-build postgresql-devel mysql-devel sqlite-devel wget unixODBC-devel nss-devel doxygen automake libtool autoconf zlib-devel libselinux-devel libuuid-devel pcre-devel openldap-devel lua-devel libxml2-devel  openssl-devel -y
wget -c https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/18/Fedora/source/SRPMS/d/distcache-${DISTCACHE_VERSION}.src.rpm -O SRPMS/distcache-${DISTCACHE_VERSION}.src.rpm 
wget -c http://www.apache.si/apr/apr-${APR_VERSION}.tar.bz2 -O SOURCES/apr-${APR_VERSION}.tar.bz2
wget -c  http://www.apache.si/apr/apr-util-${APR_UTIL_VERSION}.tar.bz2 -O SOURCES/apr-util-${APR_UTIL_VERSION}.tar.bz2
rpmbuild --rebuild  --define "_topdir `pwd`"  SRPMS/distcache-${DISTCACHE_VERSION}.src.rpm
rpm -Uvh RPMS/$(uname -m)/distcache*-${DISTCACHE_VERSION}.$(uname -m).rpm
rpmbuild  --define "_topdir `pwd`" -tb SOURCES/apr-${APR_VERSION}.tar.bz2
rpm -Uvh RPMS/$(uname -m)/apr*-${APR_VERSION}*.$(uname -m).rpm
rpmbuild --define "_topdir `pwd`"  -tb  SOURCES/apr-util-${APR_UTIL_VERSION}.tar.bz2
rpm -Uvh RPMS/$(uname -m)/apr-util*-${APR_UTIL_VERSION}*.$(uname -m).rpm
wget -c "https://www.apache.org/dist/httpd/httpd-${APACHE_VERSION}.tar.bz2" -O SOURCES/httpd-${APACHE_VERSION}.tar.bz2 
cat SPECS/httpd.spec.tpl |sed "s/TPL_HTTPD_VERSION/$APACHE_VERSION/g" > SPECS/httpd.spec
rpmbuild --define "_topdir `pwd`" -bb SPECS/httpd.spec
