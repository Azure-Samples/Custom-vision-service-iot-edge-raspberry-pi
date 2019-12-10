FROM python:3.7-slim

RUN pip install -U pip
RUN pip install numpy==1.17.3 tensorflow==2.0.0 flask pillow

RUN mkdir app
COPY ./app/app-amd64.py ./app/app.py
COPY ./app/predict-amd64.py ./app/predict.py
COPY ./app/labels.txt ./app/model.pb ./app/

# Expose the port
EXPOSE 80

# Set the working directory
WORKDIR /app

# Run the flask server for the endpoints
CMD python -u app.py
