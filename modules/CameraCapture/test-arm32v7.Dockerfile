FROM resin/raspberrypi3-python:2.7
#This image is base on the resin image for building Python apps on Raspberry Pi 3.

#Enforces cross-compilation through Quemu
RUN [ "cross-build-start" ]

#update list of packages available
RUN apt-get update

#Needed by iothub_client
RUN apt-get install -y libboost-python1.55.0

#Install python packages        
COPY /build/arm32v7-requirements.txt ./
RUN pip install --upgrade pip  && pip install --upgrade setuptools && pip install -r arm32v7-requirements.txt

# Install build modules for openCV
# Based on the work at https://github.com/mohaseeb/raspberrypi3-opencv-docker
RUN sudo apt-get install -y --no-install-recommends \
    # to build and install opencv
    unzip \
    build-essential cmake pkg-config \
    # to work with image files
    libjpeg-dev libtiff5-dev libjasper-dev libpng-dev \
    # to work with video files
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    # to display GUI
    libgtk2.0-dev pkg-config \
    && sudo rm -rf /var/lib/apt/lists/* \
    && sudo apt-get -y autoremove

RUN  OPENCV_VERSION=3.4.2 \
  && WS_DIR=`pwd` \
  && mkdir opencv \
  && cd opencv \
  # download OpenCV and opencv_contrib
  && wget -O opencv.zip https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip \
  && unzip opencv.zip \
  && sudo rm -rf opencv.zip \
  && OPENCV_SRC_DIR=`pwd`/opencv-$OPENCV_VERSION \
  # build and install without gpu dependency
  && cd $OPENCV_SRC_DIR \
  && mkdir build && cd build \
  && cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D ENABLE_FAST_MATH=1 \
    -D CUDA_FAST_MATH=1 \
    -D WITH_OPENCL=off -D WITH_OPENCL_SVM=off \
    -D WITH_OPENCLAMDFFT=off \
    -D WITH_OPENCLAMDBLAS=off \
    -D OPENCV_EXTRA_MODULES_PATH=$OPENCV_CONTRIB_MODULES_SRC_DIR \
    -D BUILD_opencv_gpu=off \
    .. \
  && make \
  && sudo make install \
  # cleanup
  && cd $WS_DIR \
  && sudo rm -rf opencv

RUN [ "cross-build-end" ]  

ADD /app/ .
ADD /build/ . 
ADD /test/ . 

ENTRYPOINT [ "bash" ]