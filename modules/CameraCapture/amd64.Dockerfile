FROM ubuntu:xenial

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libcurl4-openssl-dev python-pip libboost-python-dev && \
    rm -rf /var/lib/apt/lists/* 

COPY /build/amd64-requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools && pip install -r amd64-requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgtk2.0-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install trollius tornado

ADD /app/ .

# Expose the port
EXPOSE 5012

ENTRYPOINT [ "python", "-u", "./main.py" ]