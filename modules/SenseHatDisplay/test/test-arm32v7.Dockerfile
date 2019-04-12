FROM balenalib/raspberrypi3
# The balena base image for building apps on Raspberry Pi 3.

RUN echo "BUILD MODULE: SenseHatDisplay"

RUN [ "cross-build-start" ]

# Update package index and install python
RUN install_packages \
    python3 \
    python3-pip \
    python3-dev

# Install Python packages
COPY /build/arm32v7-requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --index-url=https://www.piwheels.org/simple -r arm32v7-requirements.txt

# Needed by iothub_client
RUN install_packages \
    libboost-python1.62.0 \
    curl \
    libcurl4-openssl-dev

# Extra dependencies to use sense-hat on this distribution
RUN install_packages \
    libatlas-base-dev \
    libopenjp2-7 \
    libtiff-tools \
    i2c-tools

# Cleanup
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get -y autoremove

RUN [ "cross-build-end" ]

ADD /app/ .
ADD /build/ .
ADD /test/ .

#Manually run the IntegrationTests.py or test other functions
ENTRYPOINT ["bash"]