FROM resin/raspberrypi3-debian:stretch
#Using the stretch distribution that has python 3.5 since iothub_client.so has been compiled with python3.5

RUN [ "cross-build-start" ]

# Install dependencies to run python3
RUN apt-get update && apt-get upgrade && apt-get install -y \
        python3 \
        python3-pip \
        wget \
        build-essential \
        libjpeg-dev \
        python3-dev \
        zlib1g-dev

COPY /build/arm32v7-requirements.txt ./

RUN pip3 install --upgrade pip 
RUN pip install --upgrade setuptools 
RUN pip install -r arm32v7-requirements.txt

#Needed by iothub_client
RUN apt-get install -y libboost-python1.62.0

#Extra dependencies to use sense-hat on this distribution
RUN apt-get update && apt-get install -y \
    libatlas-base-dev \
    libopenjp2-7 \
    libtiff-tools \
    i2c-tools

ADD /app/ .
ADD /build/ .

RUN [ "cross-build-end" ]  

ENTRYPOINT ["python3","-u", "./main.py"]