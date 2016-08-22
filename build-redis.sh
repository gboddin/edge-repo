#!/bin/bash
wget "http://download.redis.io/releases/redis-${REDIS_VERSION}.tar.gz" -cO SOURCES/redis-${REDIS_VERSION}.tar.gz
cat SPECS/redis.spec.tpl | sed "s/TPL_REDIS_VERSION/$REDIS_VERSION/g" > SPECS/redis.spec
${CMD_BUILD_DEP} -y SPECS/redis.spec
rpmbuild --define "rpmrel ${REDIS_RELEASE}" --define "_topdir `pwd`" -ba SPECS/redis.spec > ${LOGFILE}
