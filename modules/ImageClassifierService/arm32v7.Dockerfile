FROM resin/rpi-raspbian:stretch

RUN [ "cross-build-start" ]

# Install dependencies
RUN apt-get update &&  apt-get install -y \
        python3 \
        python3-pip \
        build-essential \
        python3-dev \
        libopenjp2-7-dev \
        libtiff5-dev \
        zlib1g-dev \
        libjpeg-dev \
        libatlas-base-dev \
        wget

COPY /build/arm32v7-requirements.txt arm32v7-requirements.txt

RUN pip3 install --upgrade pip 
RUN pip3 install --upgrade setuptools 
RUN pip3 install -r arm32v7-requirements.txt

ADD app /app

# Expose the port
EXPOSE 80

# Set the working directory
WORKDIR /app

RUN [ "cross-build-end" ]

# Run the flask server for the endpoints
CMD ["python3","app.py"]