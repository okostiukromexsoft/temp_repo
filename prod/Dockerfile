FROM ubuntu:16.04
MAINTAINER tst

ARG    MYSQL_DATA_DIR
ARG    MYSQL_RUN_DIR
ARG    MYSQL_LOG_DIR
ARG    MYSQL_ROOT_PASSWORD
ARG    MYSQL_CHARSET
ARG    DB_USER
ARG    DB_NAME
ARG    DB_PASS
ARG    MYSQL_USER
ARG    MYSQL_COLLATION
ARG    ZABBIX_SERVER


ENV    DEBIAN_FRONTEND noninteractive
ENV    MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV    MYSQL_DATA_DIR=${MYSQL_DATA_DIR}
ENV    MYSQL_RUN_DIR=${MYSQL_RUN_DIR}
ENV    MYSQL_LOG_DIR=${MYSQL_LOG_DIR}
ENV    DB_USER=${DB_USER}
ENV    DB_NAME=${DB_NAME}
ENV    DB_PASS=${DB_PASS}
ENV    MYSQL_CHARSET=${MYSQL_CHARSET}
ENV    MYSQL_USER=${MYSQL_USER}
ENV    MYSQL_COLLATION=${MYSQL_COLLATION}
ENV    ZABBIX_SERVER=${ZABBIX_SERVER}


RUN set -xe \
	&& echo '#!/bin/sh' > /usr/sbin/policy-rc.d \
	&& echo 'exit 101' >> /usr/sbin/policy-rc.d \
	&& chmod +x /usr/sbin/policy-rc.d \
	&& dpkg-divert --local --rename --add /sbin/initctl \
	&& cp -a /usr/sbin/policy-rc.d /sbin/initctl \
	&& sed -i 's/^exit.*/exit 0/' /sbin/initctl \
	&& echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/docker-apt-speedup \
	&& echo 'DPkg::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' > /etc/apt/apt.conf.d/docker-clean \
	&& echo 'APT::Update::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' >> /etc/apt/apt.conf.d/docker-clean \
	&& echo 'Dir::Cache::pkgcache ""; Dir::Cache::srcpkgcache "";' >> /etc/apt/apt.conf.d/docker-clean \
	&& echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/docker-no-languages \
	&& echo 'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/docker-gzip-indexes \
	&& echo 'Apt::AutoRemove::SuggestsImportant "false";' > /etc/apt/apt.conf.d/docker-autoremove-suggests \
	&& apt update \
	&& apt -y install software-properties-common \
	&& add-apt-repository ppa:jonathonf/python-3.6 \
	&& apt -y install wget curl sudo

RUN cd /tmp && wget https://repo.zabbix.com/zabbix/4.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_4.0-2+xenial_all.deb
RUN cd /tmp && dpkg -i zabbix-release_4.0-2+xenial_all.deb

RUN sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list
RUN mkdir -p /run/systemd && echo 'docker' > /run/systemd/container


COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

RUN  apt update && apt -y upgrade \
    && echo "mysql-server mysql-server/root_password password $MYSQL_ROOT_PASSWORD" | debconf-set-selections \
    && echo "mysql-server mysql-server/root_password_again password $MYSQL_ROOT_PASSWORD" | debconf-set-selections \
    && apt -y install apt-utils nano \
    && apt -y install mysql-server \
    && apt -y install zabbix-sender \
    && apt -y install python3.6

RUN rm -rf /var/lib/apt/lists/*
RUN mkdir /app
COPY src/var/lib/externalscript/get_sum_rows_from_db.py /app
COPY src/var/lib/externalscript/requirements.txt /app
RUN curl https://bootstrap.pypa.io/get-pip.py | sudo -H python3.6
RUN pip3 install -r /app/requirements.txt
COPY src/var/lib/externalscript/run_zabbix_sender.sh /usr/sbin
RUN  chmod +x /usr/sbin/run_zabbix_sender.sh

EXPOSE 3306/tcp
VOLUME ["${MYSQL_DATA_DIR}", "${MYSQL_RUN_DIR}"]

ENTRYPOINT ["/sbin/entrypoint.sh"]

