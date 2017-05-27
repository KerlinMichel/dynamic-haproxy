from flask import Flask, request
from functools import wraps
from bcrypt import hashpw

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
def add_server():
    body = request.get_json()
    servers = body.get('servers')
    print(servers)
    print(type(servers))
    return 'Not fully implemented'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
