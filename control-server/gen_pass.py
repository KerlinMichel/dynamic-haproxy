from getpass import getpass
from bcrypt import hashpw, gensalt

password = getpass('Enter your password for the control-server:')

with open('.pass', 'w') as passfile:
    passfile.write(hashpw(password, gensalt(14)))
