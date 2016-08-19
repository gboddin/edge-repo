#!/bin/bash
GD_VERSION=2.2.3
yum install fontconfig-devel libjpeg-devel libX11-devel libXpm-devel httpd-devel libvpx-devel gettext-devel libtiff-devel libwebp-devel perl-generators enchant-devel libicu-devel recode-devel  aspell-devel libtidy-devel libmcrypt-devel tokyocabinet-devel  gdbm-devel gmp-devel t1lib-devel libxslt-devel net-snmp-devel firebird-devel libc-client-devel libacl-devel systemtap-sdt-devel libtool-ltdl-devel gcc-c++ libedit-devel smtpdaemon libstdc++-devel pam-devel curl-devel bzip2-devel libpng-devel expat-devel freetds-devel db4-devel rpm-build postgresql-devel mysql-devel sqlite-devel unixODBC-devel nss-devel doxygen automake libtool autoconf zlib-devel libselinux-devel libuuid-devel pcre-devel openldap-devel lua-devel libxml2-devel  openssl-devel  freetype-devel  -y
wget "http://fr2.php.net/get/php-${PHP_VERSION}.tar.bz2/from/this/mirror" -cO SOURCES/php-${PHP_VERSION}.tar.bz2
[ ! -f SOURCES/php-${PHP_VERSION}-strip.tar.xz ] && cd SOURCES && ./strip.sh ${PHP_VERSION} && cd ..
cat SPECS/php56.spec.tpl |sed "s/TPL_PHP_VERSION/$PHP_VERSION/g" > SPECS/php56.spec
echo $PHP_CONFIG_FLAGS|grep -q libgd && wget "https://github.com/libgd/libgd/releases/download/gd-${GD_VERSION}/libgd-${GD_VERSION}.tar.xz" -cO SOURCES/libgd-${GD_VERSION}.tar.xz
echo $PHP_CONFIG_FLAGS|grep -q libgd && rpmbuild --define "_topdir `pwd`"  -bb SPECS/gd.spec
echo $PHP_CONFIG_FLAGS|grep -q libgd && rpm -ivh RPMS/$(uname -m)/gd-last-{,devel-}${GD_VERSION}-1.el6.$(uname -m).rpm 
rpmbuild --define "_topdir `pwd`" ${PHP_CONFIG_FLAGS} -bb SPECS/php56.spec
