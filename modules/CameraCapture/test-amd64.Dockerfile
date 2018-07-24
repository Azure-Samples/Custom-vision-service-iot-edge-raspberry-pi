FROM ubuntu:xenial

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libcurl4-openssl-dev python-pip libboost-python-dev && \
    rm -rf /var/lib/apt/lists/* 

COPY /build/amd64-requirements.txt ./
RUN pip install -r amd64-requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgtk2.0-dev && \
    rm -rf /var/lib/apt/lists/*

ADD /app/ .
ADD /test/ .


#Manually run the main.py or test other functions
#ENTRYPOINT ["bash"]
ENTRYPOINT [ "python", "-u", "./main.py" ]