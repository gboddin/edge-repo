#!/bin/bash
GD_VERSION=2.2.3

wget "http://fr2.php.net/get/php-${PHP_VERSION}.tar.bz2/from/this/mirror" -cO SOURCES/php-${PHP_VERSION}.tar.bz2

## TODO : investigate :
[ ! -f SOURCES/php-${PHP_VERSION}-strip.tar.xz ] && cd SOURCES && ./strip.sh ${PHP_VERSION} && cd ..

cat SPECS/php56.spec.tpl |sed "s/TPL_PHP_VERSION/$PHP_VERSION/g" > SPECS/php56.spec
echo $PHP_CONFIG_FLAGS|grep -q libgd && yum-builddep -y SPECS/gd.spec
echo $PHP_CONFIG_FLAGS|grep -q libgd && wget "https://github.com/libgd/libgd/releases/download/gd-${GD_VERSION}/libgd-${GD_VERSION}.tar.xz" -cO SOURCES/libgd-${GD_VERSION}.tar.xz
echo $PHP_CONFIG_FLAGS|grep -q libgd && rpmbuild --define "rpmrel 1" --define "_topdir `pwd`"  -ba SPECS/gd.spec > ${LOGFILE}
echo $PHP_CONFIG_FLAGS|grep -q libgd && rpm -ivh RPMS/$(uname -m)/gd-last-{,devel-}${GD_VERSION}-1.el6.$(uname -m).rpm 

yum-builddep -y SPECS/php56.spec
rpmbuild --define "rpmrel ${PHP_RELEASE}" --define "_topdir `pwd`" ${PHP_CONFIG_FLAGS} -ba SPECS/php56.spec > ${LOGFILE}
