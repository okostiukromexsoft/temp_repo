#!/bin/bash


run_zabbix_sender() {
  exec /usr/sbin/run_zabbix_sender.sh &
}
create_data_dir() {
  mkdir -p ${MYSQL_DATA_DIR}
  chmod -R 0700 ${MYSQL_DATA_DIR}
  chown -R ${MYSQL_USER}:${MYSQL_USER} ${MYSQL_DATA_DIR}
}

create_run_dir() {
  mkdir -p ${MYSQL_RUN_DIR}
  chmod -R 0755 ${MYSQL_RUN_DIR}
  chown -R ${MYSQL_USER}:root ${MYSQL_RUN_DIR}
  rm -rf ${MYSQL_RUN_DIR}/mysqld.sock.lock
}

create_log_dir() {
  mkdir -p ${MYSQL_LOG_DIR}
  chmod -R 0755 ${MYSQL_LOG_DIR}
  chown -R ${MYSQL_USER}:${MYSQL_USER} ${MYSQL_LOG_DIR}
}

listen() {
  sed -e "s/^bind-address\(.*\)=.*/bind-address = $1/" -i /etc/mysql/mysql.conf.d/mysqld.cnf
}

initialize_mysql_database() {
  if [ ! -d ${MYSQL_DATA_DIR}/mysql ]; then
    echo "Installing database..."
    mysqld --initialize-insecure --user=mysql >/dev/null 2>&1

    echo "Starting MySQL server..."
    /usr/bin/mysqld_safe >/dev/null 2>&1 &

    timeout=30
    echo -n "Waiting for database server to accept connections"
    while ! /usr/bin/mysqladmin -u root -p${MYSQL_ROOT_PASSWORD} status >/dev/null 2>&1
    do
      timeout=$(($timeout - 1))
      if [ $timeout -eq 0 ]; then
        echo -e "\nCould not connect to database server. Aborting... In initialize  block"
        exit 1
      fi
      echo -n "."
      sleep 1
    done

    /usr/bin/mysqladmin -uroot -p${MYSQL_ROOT_PASSWORD} shutdown
  fi
}

create_users_and_databases() {
  if [ -n "${DB_USER}" -o -n "${DB_NAME}" ]; then
    /usr/bin/mysqld_safe >/dev/null 2>&1 &

    timeout=30
    while ! /usr/bin/mysqladmin -u root -p${MYSQL_ROOT_PASSWORD} status >/dev/null 2>&1
    do
      timeout=$(($timeout - 1))
      if [ $timeout -eq 0 ]; then
        echo "Could not connect to mysql server. Aborting... In create database block"
        exit 1
      fi
      sleep 2
    done

    if [ -n "${DB_NAME}" ]; then
      for db in $(awk -F',' '{for (i = 1 ; i <= NF ; i++) print $i}' <<< "${DB_NAME}"); do
        echo "Creating database \"$db\"..."
        mysql -uroot -p${MYSQL_ROOT_PASSWORD} \
          -e "CREATE DATABASE IF NOT EXISTS \`$db\` DEFAULT CHARACTER SET \`$MYSQL_CHARSET\` COLLATE \`$MYSQL_COLLATION\`;"
          if [ -n "${DB_USER}" ]; then
            echo "Granting access to database \"$db\" for user \"${DB_USER}\"..."
            mysql -uroot -p${MYSQL_ROOT_PASSWORD} \
            -e "GRANT ALL PRIVILEGES ON \`$db\`.* TO '${DB_USER}' IDENTIFIED BY '${DB_PASS}';"
          fi
        done
    fi
    /usr/bin/mysqladmin -uroot -p${MYSQL_ROOT_PASSWORD} shutdown
  fi
}

create_data_dir
create_run_dir
create_log_dir
run_zabbix_sender

if [[ ${1:0:1} = '-' ]]; then
  EXTRA_ARGS="$@"
  set --
elif [[ ${1} == mysqld_safe || ${1} == $(which mysqld_safe) ]]; then
  EXTRA_ARGS="${@:2}"
  set --
fi
if [[ -z ${1} ]]; then
  listen "127.0.0.1" && \
  initialize_mysql_database && \
  create_users_and_databases && \
  listen "0.0.0.0"
  exec $(which mysqld_safe) $EXTRA_ARGS
else
  exec "$@"
fi
exit 0