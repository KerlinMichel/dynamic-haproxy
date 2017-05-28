FROM buildpack-deps:jessie

COPY . /etc/haproxy/

RUN apt-get update && apt-get install -y libffi-dev \
                                         python python-pip python-dev python-setuptools \
                                         haproxy

RUN pip install --upgrade cffi
RUN pip install flask bcrypt

WORKDIR /etc/haproxy/control-server

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
