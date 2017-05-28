from subprocess import Popen, PIPE
from re import search

with open('../haproxy.cfg') as hapcfg:
    lines = hapcfg.readlines()

with open('default_servers') as servers:
    server_opts = servers.readline().strip()

haproxy_cfg = {}

for line in lines:
    if not line.strip():
        continue
    if line[0].isspace():
        if key not in haproxy_cfg:
            haproxy_cfg[key] = []
        haproxy_cfg[key].append(line.strip())
    else:
        key = line.strip()

num_servers = 0
for server in haproxy_cfg['listen servers']:
    if server[0:6] == 'server':
        num_servers = num_servers + 1

def server_exists(ip):
    for server in haproxy_cfg['listen servers']:
        if server[0:6] == 'server' and ip in server:
            return True
    return False

def reload_server():
    process = Popen(['service', 'haproxy', 'reload'], stdout=PIPE)
    out, err = process.communicate()

def add_server(server, reload_server):
    server_name = haproxy_cfg['listen servers'][-1]
    idx = int(search(r'(server)(\d+)', server_name).group(2))
    with open('../haproxy.cfg', 'a') as hap_cfg:
        hap_cfg.write('\tserver server{} {} {}\n'.format(idx+1, server, server_opts))
    if reload_server:
        reload_server()

def remove_server(server, reload_server):
    with open('../haproxy.cfg', 'r+') as hapcfg:
        lines = hapcfg.readlines()
        hapcfg.seek(0)
        for line in lines:
            if server not in line:
                hapcfg.write(line)
        hapcfg.truncate()
    if reload_server:
         reload_server()
