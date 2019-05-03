import subprocess
import os

def used_memory():
    pum = subprocess.Popen(["redis-cli info memory | grep 'used_memory:' | cut -d ':' -f 2"],
                           stdout=subprocess.PIPE, shell=True)
    um_output, um_error = pum.communicate()
    um_output = str(um_output)
    um_output = um_output.replace("b", "")
    um_output = um_output.replace("n", "")
    um_output = um_output.replace("r", "")
    um_output = um_output.replace("'", "")
    um_output = um_output[:-2]
    return {used_memory.__name__: um_output}


def used_memory_rss():
    pumr = subprocess.Popen(["redis-cli info memory | grep 'used_memory_rss:' | cut -d ':' -f 2"],
                            stdout=subprocess.PIPE, shell=True)
    umr_output, umr_error = pumr.communicate()
    umr_output = str(umr_output)
    umr_output = umr_output.replace("b", "")
    umr_output = umr_output.replace("n", "")
    umr_output = umr_output.replace("r", "")
    umr_output = umr_output.replace("'", "")
    umr_output = umr_output[:-2]
    return {used_memory_rss.__name__: umr_output}


def keyspace_hits():
    pkh = subprocess.Popen(["redis-cli info stats | grep 'keyspace_hits:' | cut -d ':' -f 2"],
                           stdout=subprocess.PIPE, shell=True)
    kh_output, kh_error = pkh.communicate()
    kh_output = str(kh_output)
    kh_output = kh_output.replace("b", "")
    kh_output = kh_output.replace("n", "")
    kh_output = kh_output.replace("r", "")
    kh_output = kh_output.replace("'", "")
    kh_output = kh_output[:-2]
    return {keyspace_hits.__name__: kh_output}


def keyspace_misses():
    pkm = subprocess.Popen(["redis-cli info clients | grep 'connected_clients:' | cut -d ':' -f 2"],
                           stdout=subprocess.PIPE, shell=True)
    km_output, km_error = pkm.communicate()
    km_output = str(km_output)
    km_output = km_output.replace("b", "")
    km_output = km_output.replace("n", "")
    km_output = km_output.replace("r", "")
    km_output = km_output.replace("'", "")
    km_output = km_output[:-2]
    return {keyspace_misses.__name__: km_output}


def connected_clients():
    pcc = subprocess.Popen(["redis-cli info clients | grep 'connected_clients:' | cut -d ':' -f 2"],
                           stdout=subprocess.PIPE, shell=True)
    cc_output, cc_error = pcc.communicate()
    cc_output = str(cc_output)
    cc_output = cc_output.replace("b", "")
    cc_output = cc_output.replace("n", "")
    cc_output = cc_output.replace("r", "")
    cc_output = cc_output.replace("'", "")
    cc_output = cc_output[:-2]
    return {connected_clients.__name__: cc_output}


def blocked_clients():
    pbc = subprocess.Popen(["redis-cli info clients | grep 'blocked_clients:' | cut -d ':' -f 2"],
                           stdout=subprocess.PIPE, shell=True)
    bc_output, bc_error = pbc.communicate()
    bc_output = str(bc_output)
    bc_output = bc_output.replace("b", "")
    bc_output = bc_output.replace("n", "")
    bc_output = bc_output.replace("r", "")
    bc_output = bc_output.replace("'", "")
    bc_output = bc_output[:-2]
    return {blocked_clients.__name__: bc_output}


def expired_keys():
    pexk = subprocess.Popen(["redis-cli info stats | grep 'expired_keys:' | cut -d ':' -f 2"],
                            stdout=subprocess.PIPE, shell=True)
    exk_output, ek_error = pexk.communicate()
    exk_output = str(exk_output)
    exk_output = exk_output.replace("b", "")
    exk_output = exk_output.replace("n", "")
    exk_output = exk_output.replace("r", "")
    exk_output = exk_output.replace("'", "")
    exk_output = exk_output[:-2]
    return {expired_keys.__name__: exk_output}


def evicted_keys():
    pevk = subprocess.Popen(["redis-cli info stats | grep 'evicted_keys:' | cut -d ':' -f 2"],
                            stdout=subprocess.PIPE, shell=True)
    evk_output, evk_error = pevk.communicate()
    evk_output = str(evk_output)
    evk_output = evk_output.replace("b", "")
    evk_output = evk_output.replace("n", "")
    evk_output = evk_output.replace("r", "")
    evk_output = evk_output.replace("'", "")
    evk_output = evk_output[:-2]
    return {evicted_keys.__name__: evk_output}


def connected_slaves():
    pcs = subprocess.Popen(["redis-cli info replication | grep 'connected_slaves:' | cut -d ':' -f 2"],
                           stdout=subprocess.PIPE, shell=True)
    cs_output, cs_error = pcs.communicate()
    cs_output = str(cs_output)
    cs_output = cs_output.replace("b", "")
    cs_output = cs_output.replace("n", "")
    cs_output = cs_output.replace("r", "")
    cs_output = cs_output.replace("'", "")
    cs_output = cs_output[:-2]
    return {connected_slaves.__name__: cs_output}

def host_name():
    f = open('/etc/hostnameDOCKER', 'r')
    file_contents = f.read()
    f.close()
    var_os = os.environ['DOCKERHOST'] = file_contents
    return var_os


def transform_to_zbxsnd_file(def_data, docker_host):
    file = open('redis.txt', 'a')
    for key in def_data.keys():
        met_name = key
        met_value = def_data[key]
        docker_host = docker_host.replace("\n","")
        lld_str = f"""{docker_host} redis.db.info""" """{"data":[{"{#METRICNAME}":"%s"}]} \n""" % met_name
        keys = f"""{docker_host} redis.db.info.key.[{met_name}] {met_value} \n"""
        lld = lld_str + keys
        print(lld)
        file.write(lld)
    file.close()


def load_to_zabbix_server(server_ip):
    popen_command = f"zabbix_sender -z '{server_ip}' -p 10051 -i ./redis.txt -vv"
    print(popen_command)
    send_file = subprocess.Popen([popen_command], shell=True)
    output, errors = send_file.communicate()
    return output, errors


def env_variables():
    p = (subprocess.Popen(['echo $ZABBIX_SERVER'], stdout=subprocess.PIPE, shell=True))
    ip_output, ip_errors = p.communicate()
    ip_output = str(ip_output)
    ip_output = ip_output.replace("b", "")
    ip_output = ip_output.replace("'", "")
    ip_output = ip_output.replace("n", "")
    ip_output = ip_output[:-1]
    print(ip_output)




    return ip_output


if __name__ == '__main__':
    doc_host = host_name()

    f = open('redis.txt', 'w')
    f.close()
    transform_to_zbxsnd_file(used_memory(), docker_host = doc_host)
    transform_to_zbxsnd_file(used_memory_rss(), docker_host = doc_host)
    transform_to_zbxsnd_file(keyspace_hits(), docker_host = doc_host)
    transform_to_zbxsnd_file(keyspace_misses(), docker_host = doc_host)
    transform_to_zbxsnd_file(connected_clients(), docker_host = doc_host)
    transform_to_zbxsnd_file(blocked_clients(), docker_host = doc_host)
    transform_to_zbxsnd_file(expired_keys(), docker_host = doc_host)
    transform_to_zbxsnd_file(evicted_keys(), docker_host = doc_host)
    transform_to_zbxsnd_file(connected_slaves(), docker_host = doc_host)

    ip = env_variables()
    load_to_zabbix_server(server_ip=ip)
