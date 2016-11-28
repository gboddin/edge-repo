FROM centos
MAINTAINER Gregory Boddin

RUN yum install -y spectool mock
RUN useradd mock -g mock

ADD *.cfg /etc/mock/

## Broken see https://github.com/docker/docker/issues/1916

#RUN su mock -c"/usr/bin/mock -r edge-5-x86_64 --init"
#RUN su mock -c"/usr/bin/mock -r edge-6-x86_64 --init"
#RUN su mock -c"/usr/bin/mock -r edge-7-x86_64 --init"
