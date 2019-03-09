# Azure IoT Edge Camera Capture module

This container is an IoT Edge module that can read a video stream from a camera or from a video file and optionally send frames to IoT Edge module for processing. It forwards all processing results to the Edge Hub.
It is a Linux Docker container made for AMD64 and ARM  processors written in Python.

## Additional configurations
You can use the current conifguration set in the deployment manifest file or update the configuration of this module as follow:

The camera mount path or the video file must be provided through the VIDEO_PATH environment variable:
- Camera mount:
    - In the deployment manifest:
    ```json
    "createOptions": "{\"Env\":[\"VIDEO_PATH=/dev/video0\"]}"
    ```
- Video file:
    - Make sure to include the video file in the .Dockerfile:
    ```docker
    ADD ./test/ .
    ```
    - In the deployment manifest:
    ```json
    "createOptions": "{\"Env\":[\"VIDEO_PATH=./AppleAndBanana.mp4\"]}"
    ```

## Optional parameters
The following parameters are optional and can be specified via environment variables in the deployment manifest (See 'createOptions' above).

|Environment variable  |Description  |
|---------|---------|
|IMAGE_PROCESSING_ENDPOINT     | Service endpoint to send the frames to for processing. Example: "http://my-ai-service:8080" (where "my-ai-service" is the name of another IoT Edge module). Leave empty when no external processing is needed (Default).  |
|IMAGE_PROCESSING_PARAMS     | Query parameters to send to the processing service. Example: "{'returnLabels': 'true'}". Empty by default. |
|SHOW_VIDEO     | Show the video. From a browser, go to "http://YourRaspberryPiIpAdress:5012". Examle: "FALSE". False by default. |
|VERBOSE     |  Show detailed logs and perf timers. Example: "FALSE". False by default.  |
|LOOP_VIDEO     | When reading from a video file, it will loop this video. Example: "TRUE". True by default. |
|CONVERT_TO_GRAY     | Convert to gray before sending to external service for processing. Example: "FALSE". False by default.  |
|RESIZE_WIDTH     | Resize frame width before sending to external service for processing. Example: "256". Does not resize by default (0). |
|RESIZE_HEIGHT     | Resize frame width before sending to external service for processing. Example: "456". Does not resize by default (0). |
