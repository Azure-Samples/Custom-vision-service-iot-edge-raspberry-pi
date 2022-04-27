FROM balenalib/raspberrypi3-debian-python:3.7

RUN [ "cross-build-start" ]

RUN apt update && apt install -y libjpeg62-turbo libopenjp2-7 libtiff5 libatlas-base-dev libxcb1
RUN pip install absl-py six protobuf wrapt gast astor termcolor keras_applications keras_preprocessing --no-deps
RUN pip install numpy==1.16 tensorflow==1.13.1 --extra-index-url 'https://www.piwheels.org/simple' --no-deps
RUN pip install flask==1.1.2 pillow==7.1.2 --index-url 'https://www.piwheels.org/simple'

COPY app /app

# Expose the port
EXPOSE 80

# Set the working directory
WORKDIR /app

RUN [ "cross-build-end" ]

# Run the flask server for the endpoints
CMD python -u app.py