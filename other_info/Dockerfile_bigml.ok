FROM debian:jessie
RUN apt-get -y update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN cd /root && \
    git clone https://github.com/bigmlcom/python.git && \
    cd /root/python && \
    python3 setup.py install && \
    cd /root && \
    rm -r python


