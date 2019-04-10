FROM tensorflow/tensorflow:latest-py3

RUN echo "BUILD MODULE: ImageClassifierService"

COPY /build/amd64-requirements.txt amd64-requirements.txt

# Install Python packages
RUN pip install -r amd64-requirements.txt
 
ADD app /app

# Expose the port
EXPOSE 80

# Set the working directory
WORKDIR /app

# Run the flask server for the endpoints
CMD python app.py
