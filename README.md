---
services: iot-edge, custom-vision-service, iot-hub
platforms: python
author: ebertrams
---

# Custom Vision + Azure IoT Edge on a Raspberry Pi 3

> [!NOTE]
> This sample still uses the IoT Edge Preview bits. To use it with the new IoT Edge GA bits, you will need to update the **Camera capture** and **SenseHat display** modules manually to use the latest IoT SDK versions. The **Custom vision** should remain the same. 

This is a sample showing how to deploy a Custom Vision model to a Raspberry Pi 3 device running Azure IoT Edge. This solution is made of 3 modules:

- **Camera capture** - this module captures the video stream from a USB camera, sends the frames for analysis to the custom vision module and shares the output of this analysis to the edgeHub. This module is written in python and uses [OpenCV](https://opencv.org/) to read the video feed.
- **Custom vision** - it is a web service over HTTP running locally that takes in images and classifies them based on a custom model built via the [Custom Vision website](https://azure.microsoft.com/en-us/services/cognitive-services/custom-vision-service/). This module has been exported from the Custom Vision website and slightly modified to run on a ARM architecture. You can modify it by updating the model.pb and label.txt files to update the model.
- **SenseHat display** - this module gets messages from the edgeHub and blinks the raspberry Pi's senseHat according to the tags specified in the inputs messages. This module is written in python and requires a [SenseHat](https://www.raspberrypi.org/products/sense-hat/) to work.

## Get started
1- Update the module.json files of the 3 modules above to point to your own Azure Container Registry

2- Build the full solution by running the `Build IoT Edge Solution` command from the [Azure IoT Edge extension in VS Code](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-edge).

## Prerequisites

You can run this solution on either of the following hardware:

- **Raspberry Pi 3**: Set up Azure IoT Edge on a Raspberry Pi 3 ([instructions](https://blog.jongallant.com/2017/11/azure-iot-edge-raspberrypi/)) with a [SenseHat](https://www.raspberrypi.org/products/sense-hat/) and use the arm32v7 module tags.

- **Simulated Azure IoT Edge device** (such as a PC): Set up Azure IoT Edge ([instructions on Windows](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-simulate-device-windows), [instructions on Linux](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-simulate-device-linux)) and use the amd64 module tags. A test x64 deployment manifest is already available. To use it, rename the 'deployment.template.test-amd-64' to 'deployment.template.json', then build the IoT Edge solution from this manifest and deploy it to an x64 device.
