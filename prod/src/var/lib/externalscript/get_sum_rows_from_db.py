import mysql.connector
import subprocess
import os


def export_db(host1, user1, passwd1):
    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        passwd=passwd1
    )

    curr = conn.cursor()
    curr.execute("SHOW DATABASES;")
    db_fetch = curr.fetchall()
    db_list = []
    db_count = {}

    for db in db_fetch:
        db_list.append(db[0])

    for db in db_list:
        curr.execute(f"USE {db};")
        curr.execute("SHOW TABLE STATUS;")
        rows = curr.fetchall()

        row_count = 0
        for row in rows:
            if row[4] is None:
                pass
            else:
                row_count = row_count + row[4]
            db_count[db] = row_count

    return db_count


def host_name():
    f = open('/etc/hostnameDOCKER', 'r')
    file_contents = f.read()
    f.close()
    var_os = os.environ['DOCKERHOST'] = file_contents
    return var_os


def transform_to_zbxsnd_file(import_db, docker_host):
    file = open('text.txt', 'w')
    for db in import_db.keys():
        db_name = db
        db_rows = import_db[db]
        docker_host = docker_host.replace("\n", "")
        lld_str = f"""{docker_host} mysql.db.sum.rows""" """{"data":[{"{#DBNAME}":"%s"}]} \n""" % db_name
        keys = f"""{docker_host} mysql.db.sum.rows.sum.[{db_name}] {db_rows} \n"""
        lld = lld_str + keys
        print(lld)
        file.write(lld)
    file.close()



def env_variables():
    p = (subprocess.Popen(['echo $ZABBIX_SERVER'], stdout=subprocess.PIPE, shell=True))
    ip_output, ip_errors = p.communicate()
    ip_output = str(ip_output)
    ip_output = ip_output.replace("b", "")
    ip_output = ip_output.replace("'", "")
    ip_output = ip_output.replace("n", "")
    ip_output = ip_output[:-1]

    ho = (subprocess.Popen(['echo $HOSTNAME'], stdout=subprocess.PIPE, shell=True))
    host_output, host_errors = ho.communicate()
    host_output = str(host_output)
    host_output = host_output.replace("b", "")
    host_output = host_output.replace("'", "")
    host_output = host_output.replace("n", "")
    host_output = host_output[:-1]

    us = (subprocess.Popen(['echo $DB_USER'], stdout=subprocess.PIPE, shell=True))
    user_output, user_errors = us.communicate()
    user_output = str(user_output)
    user_output = user_output.replace("b", "")
    user_output = user_output.replace("'", "")
    user_output = user_output.replace("n", "")
    user_output = user_output[:-1]

    pa = (subprocess.Popen(['echo $DB_PASS'], stdout=subprocess.PIPE, shell=True))
    passwd_output, passwd_errors = pa.communicate()
    passwd_output = str(passwd_output)
    passwd_output = passwd_output.replace("b", "")
    passwd_output = passwd_output.replace("'", "")
    passwd_output = passwd_output.replace("n", "")
    passwd_output = passwd_output[:-1]

    return ip_output, host_output, user_output, passwd_output


def load_to_zabbix_server(server_ip):
    popen_command = f"zabbix_sender -z '{server_ip}' -p 10051 -i ./text.txt -vv"
    print(popen_command)
    send_file = subprocess.Popen([popen_command], shell=True)
    output, errors = send_file.communicate()
    return output, errors


if __name__ == "__main__":
    ip = env_variables()[0]
    host = env_variables()[1]
    user = env_variables()[2]
    pas = env_variables()[3]

    doc_host = host_name()

    transform_to_zbxsnd_file(export_db(host1=host, user1=user, passwd1=pas), docker_host = doc_host)


    load_to_zabbix_server(server_ip=ip)
