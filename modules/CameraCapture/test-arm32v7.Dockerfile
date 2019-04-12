FROM balenalib/raspberrypi3
# The balena base image for building apps on Raspberry Pi 3.

RUN echo "BUILD MODULE: CameraCapture"

# Enforces cross-compilation through Quemu
RUN [ "cross-build-start" ]

# Update package index and install dependencies
RUN install_packages \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libopenjp2-7-dev \
    zlib1g-dev \
    libatlas-base-dev \
    wget \
    libboost-python1.62.0 \
    curl \
    libcurl4-openssl-dev

# Required for OpenCV
RUN install_packages \
    # Hierarchical Data Format
    libhdf5-dev libhdf5-serial-dev \
    # for image files
    libjpeg-dev libtiff5-dev libjasper-dev libpng-dev \
    # for video files
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    # for GUI
    libqt4-test libqtgui4 libqtwebkit4 libgtk2.0-dev \
    # high def image processing
    libilmbase-dev libopenexr-dev

# Install Python packages
COPY /build/arm32v7-requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --index-url=https://www.piwheels.org/simple -r arm32v7-requirements.txt

# Cleanup
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get -y autoremove

RUN [ "cross-build-end" ]

ADD /app/ .
ADD /test/ .

# Expose the port
EXPOSE 5012

ENTRYPOINT [ "python3", "-u", "./main.py" ]