from shutil import copyfile

with open('control-server/default_servers') as servers:
    lines = servers.readlines()

lines = [line.strip() for line in lines]

server_opts, servers = lines[0], lines[1:]

copyfile('config/haproxy.cfg.sample', 'haproxy.cfg')

with open('haproxy.cfg', 'a') as hapcfg:
    for idx, server in enumerate(servers):
        hapcfg.write('\tserver server{} {} {}\n'.format(idx, server, server_opts))
