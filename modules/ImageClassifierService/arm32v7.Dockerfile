FROM balenalib/raspberrypi3
# The balena base image for building apps on Raspberry Pi 3.

RUN echo "BUILD MODULE: ImageClassifierService"

RUN [ "cross-build-start" ]

# Install dependencies
RUN install_packages \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libopenjp2-7-dev \
    libtiff5-dev \
    zlib1g-dev \
    libjpeg-dev \
    libatlas-base-dev \
    wget

# Install Python packages
COPY /build/arm32v7-requirements.txt ./
RUN pip3 install --upgrade pip 
RUN pip3 install --upgrade setuptools
RUN pip3 install --index-url=https://www.piwheels.org/simple -r arm32v7-requirements.txt

# Cleanup
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get -y autoremove

RUN [ "cross-build-end" ]

# Add the application
ADD app /app

# Expose the port
EXPOSE 80

# Set the working directory
WORKDIR /app

# Run the flask server for the endpoints
CMD ["python3","app.py"]