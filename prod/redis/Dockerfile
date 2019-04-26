FROM ubuntu:bionic-20181204

ARG ZABBIX_SERVER

ENV REDIS_VERSION=4.0.9 \
    REDIS_USER=redis \
    REDIS_DATA_DIR=/var/lib/redis \
    REDIS_LOG_DIR=/var/log/redis \
    ZABBIX_SERVER=${ZABBIX_SERVER}


RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y redis-server=5:${REDIS_VERSION}* \
 && sed 's/^bind /# bind /' -i /etc/redis/redis.conf \
 && sed 's/^logfile /# logfile /' -i /etc/redis/redis.conf \
 && sed 's/^daemonize yes/daemonize no/' -i /etc/redis/redis.conf \
 && sed 's/^protected-mode yes/protected-mode no/' -i /etc/redis/redis.conf \
 && sed 's/^# unixsocket /unixsocket /' -i /etc/redis/redis.conf \
 && sed 's/^# unixsocketperm 700/unixsocketperm 777/' -i /etc/redis/redis.conf \
 && rm -rf /var/lib/apt/lists/*

RUN apt -y update \
 && apt -y install software-properties-common \
 && apt -y install python3 \
 && apt -y install python3 python3-pip \
 && apt -y install wget curl sudo

RUN cd /tmp && wget https://repo.zabbix.com/zabbix/4.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_4.0-2+bionic_all.deb
RUN cd /tmp && dpkg -i zabbix-release_4.0-2+bionic_all.deb

RUN apt update && apt -y upgrade \
 && apt -y install zabbix-sender \
 && apt -y install nano

RUN mkdir /run_py
COPY externalscript/get_info_from_redis.py /run_py
COPY externalscript/requirements.txt /run_py
RUN pip3 install -r /run_py/requirements.txt

COPY externalscript/run_sender.sh /usr/sbin
RUN  chmod +x /usr/sbin/run_sender.sh

COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

EXPOSE 6379/tcp
ENTRYPOINT ["/sbin/entrypoint.sh"]