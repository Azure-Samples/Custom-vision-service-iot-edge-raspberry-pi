FROM resin/rpi-raspbian:jessie

# Install dependencies
RUN apt-get update &&  apt-get install -y \
        python3 \
        python3-pip \
        build-essential \
        python3-dev \
        zlib1g-dev \
        libjpeg-dev \
        wget

COPY /build/arm32v7-requirements.txt arm32v7-requirements.txt

RUN pip3 install --upgrade pip 
RUN pip install --upgrade setuptools 
RUN pip install -r arm32v7-requirements.txt

#TensorFlow 1.5.0
RUN pip install http://ci.tensorflow.org/view/Nightly/job/nightly-pi-python3/122/artifact/output-artifacts/tensorflow-1.5.0-cp34-none-any.whl

ADD app /app

# Expose the port
EXPOSE 80

# Set the working directory
WORKDIR /app

# Run the flask server for the endpoints
CMD ["python3","app.py"]