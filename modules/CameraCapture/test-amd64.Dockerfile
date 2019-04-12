FROM ubuntu:xenial

RUN echo "BUILD MODULE: CameraCapture"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        libcurl4-openssl-dev \
        libboost-python-dev \
        libgtk2.0-dev

# Install Python packages
COPY /build/amd64-requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools 
RUN pip3 install -r amd64-requirements.txt

# Cleanup
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get -y autoremove

ADD /app/ .
ADD /test/ .

# Expose the port
EXPOSE 5012

#Manually run the main.py or test other functions
ENTRYPOINT [ "python3", "-u", "./main.py" ]