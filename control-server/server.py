from flask import Flask, request
from functools import wraps
from bcrypt import hashpw
from haproxy_controls import *
app = Flask(__name__)

with open('.pass') as passfile:
    hashpass = passfile.readline()

with open('default_servers') as servers:
    server_cfg = servers.readline()

haproxy_cfg = '/etc/haproxy/haproxy.cfg'

def verify_password(password):
    return hashpw(password, hashpass) == hashpass

def auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        password = request.get_json().get('password').encode('utf-8')
        if not verify_password(password):
            return 'Incorrect password', 400
        return f(*args, **kwargs)
    return decorated

@app.route("/addServers", methods=['POST'])
@auth
def add_servers():
    body = request.get_json()
    servers = body.get('servers')
    force = body.get('force')
    reload_server_flag = body.get('reload_server')
    for server in servers:
        if force or not server_exists(server):
            add_server(server, False)
    if reload_server_flag:
        reload_server()
    return 'Added servers succesfully'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
