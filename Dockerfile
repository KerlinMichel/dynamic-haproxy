FROM haproxy:1.7

COPY . /usr/local/etc/haproxy/

RUN groupadd haproxy && useradd -g haproxy haproxy

RUN mkdir /var/lib/haproxy

RUN apt-get update && apt-get install -y libffi-dev \
                                         python python-pip python-dev python-setuptools

RUN pip install --upgrade cffi
RUN pip install flask bcrypt
