FROM mohaseeb/raspberrypi3-python-opencv:latest
#This image is base on the resin image which is based on armv7 debian jessie, which has libboost-python1.55.0.
#This image include a pre-compiled version of OpenCV. It is based on python 2.7.

#Enforces cross-compilation through Quemu
RUN [ "cross-build-start" ]

#update list of packages available
RUN apt-get update

#Needed to use iothub_client.so. iothub_client is manually compiled until an ARM version can be installed through pip install
RUN apt-get install -y \
        libboost-python1.55.0

#Install python packages        
COPY /build/arm32v7-requirements.txt ./
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools 
RUN pip install -r arm32v7-requirements.txt

RUN [ "cross-build-end" ]  

ADD /app/ .
ADD /build/ . 

CMD [ "python", "-u", "./main.py" ]