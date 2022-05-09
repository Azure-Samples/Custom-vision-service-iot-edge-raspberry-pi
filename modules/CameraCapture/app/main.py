# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import os
import random
import sys
import time

#import iothub_client
# pylint: disable=E0611
# Disabling linting that is not supported by Pylint for C extensions such as iothub_client. See issue https://github.com/PyCQA/pylint/issues/1955
#from iothub_client import (IoTHubModuleClient, IoTHubClientError, IoTHubError,
#                           IoTHubMessage, IoTHubMessageDispositionResult,
#                           IoTHubTransportProvider)

from azure.iot.device import IoTHubModuleClient, Message

import CameraCapture
from CameraCapture import CameraCapture


# global counters
SEND_CALLBACKS = 0


def send_to_Hub_callback(strMessage):
    message = Message(bytearray(strMessage, 'utf8'))
    hubManager.send_message_to_output(message, "output1")

# Callback received when the message that we're forwarding is processed.

class HubManager(object):

    def __init__(
            self,
            messageTimeout,
            verbose):
        '''
        Communicate with the Edge Hub

        :param int messageTimeout: the maximum time in milliseconds until a message times out. The timeout period starts at IoTHubClient.send_event_async. By default, messages do not expire.
        :param IoTHubTransportProvider protocol: Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
        :param bool verbose: set to true to get detailed logs on messages
        '''
        self.messageTimeout = messageTimeout
        self.client = IoTHubModuleClient.create_from_edge_environment()
        #self.client.set_option("messageTimeout", self.messageTimeout)
        #self.client.set_option("product_info", "edge-camera-capture")
        #if verbose:
        #    self.client.set_option("logtrace", 1)  # enables MQTT logging

    def send_message_to_output(self, event, outputQueueName):
        self.client.send_message_to_output(event, outputQueueName)
        global SEND_CALLBACKS
        SEND_CALLBACKS += 1

def main(
        debugy=False,
        videoPath="0",
        imageProcessingEndpoint="",
        imageProcessingParams="",
        showVideo=False,
        verbose=False,
        loopVideo=True,
        convertToGray=False,
        resizeWidth=0,
        resizeHeight=0,
        annotate=False,
        bypassIot=False
):
    '''
    Capture a camera feed, send it to processing and forward outputs to EdgeHub

    :param int videoPath: camera device path such as /dev/video0 or a test video file such as /TestAssets/myvideo.avi. /dev/video0 by default ("0")
    :param str imageProcessingEndpoint: service endpoint to send the frames to for processing. Example: "http://face-detect-service:8080". Leave empty when no external processing is needed (Default). Optional.
    :param str imageProcessingParams: query parameters to send to the processing service. Example: "'returnLabels': 'true'". Empty by default. Optional.
    :param bool showVideo: show the video in a windows. False by default. Optional.
    :param bool verbose: show detailed logs and perf timers. False by default. Optional.
    :param bool loopVideo: when reading from a video file, it will loop this video. True by default. Optional.
    :param bool convertToGray: convert to gray before sending to external service for processing. False by default. Optional.
    :param int resizeWidth: resize frame width before sending to external service for processing. Does not resize by default (0). Optional.
    :param int resizeHeight: resize frame width before sending to external service for processing. Does not resize by default (0). Optional.
    :param bool annotate: when showing the video in a window, it will annotate the frames with rectangles given by the image processing service. False by default. Optional. Rectangles should be passed in a json blob with a key containing the string rectangle, and a top left corner + bottom right corner or top left corner with width and height.
    :param bool bypassiot: When true will not initialize communication or send IoT messages. False by default Optional. 
    '''
    try:
        print("\nPython %s\n" % sys.version)
        print("Camera Capture Azure IoT Edge Module. Press Ctrl-C to exit.")
        #if debugy:
        #    print("Wait for debugger!!!")
        #    import debugpy
        #    debugpy.listen(5678)
        #    debugpy.wait_for_client()  # blocks execution until client is attached
        try:
            if not bypassIot:
                global hubManager
                hubManager = HubManager(
                    10000, verbose)
        except Exception as iothub_error:
            print("Unexpected error %s from IoTHub" % iothub_error)
            return
        with CameraCapture(videoPath, imageProcessingEndpoint, imageProcessingParams, showVideo, verbose, loopVideo, convertToGray, resizeWidth, resizeHeight, annotate, send_to_Hub_callback, bypassIot) as cameraCapture:
            cameraCapture.start()
    except KeyboardInterrupt:
        print("Camera capture module stopped")


def __convertStringToBool(env):
    if env in ['True', 'TRUE', '1', 'y', 'YES', 'Y', 'Yes']:
        return True
    elif env in ['False', 'FALSE', '0', 'n', 'NO', 'N', 'No']:
        return False
    else:
        raise ValueError('Could not convert string to bool.')


if __name__ == '__main__':
    try:
        DEBUGY = __convertStringToBool(os.getenv('DEBUG', 'False'))
        VIDEO_PATH = os.getenv('VIDEO_PATH', "0")
        IMAGE_PROCESSING_ENDPOINT = os.getenv('IMAGE_PROCESSING_ENDPOINT', "")
        IMAGE_PROCESSING_PARAMS = os.getenv('IMAGE_PROCESSING_PARAMS', "")
        SHOW_VIDEO = __convertStringToBool(os.getenv('SHOW_VIDEO', 'False'))
        VERBOSE = __convertStringToBool(os.getenv('VERBOSE', 'False'))
        LOOP_VIDEO = __convertStringToBool(os.getenv('LOOP_VIDEO', 'True'))
        CONVERT_TO_GRAY = __convertStringToBool(
            os.getenv('CONVERT_TO_GRAY', 'False'))
        RESIZE_WIDTH = int(os.getenv('RESIZE_WIDTH', 0))
        RESIZE_HEIGHT = int(os.getenv('RESIZE_HEIGHT', 0))
        ANNOTATE = __convertStringToBool(os.getenv('ANNOTATE', 'False'))
        BYPASS_IOT = __convertStringToBool(os.getenv('BYPASS_IOT', 'False'))

    except ValueError as error:
        print(error)
        sys.exit(1)

    main(DEBUGY, VIDEO_PATH, IMAGE_PROCESSING_ENDPOINT, IMAGE_PROCESSING_PARAMS, SHOW_VIDEO,
         VERBOSE, LOOP_VIDEO, CONVERT_TO_GRAY, RESIZE_WIDTH, RESIZE_HEIGHT, ANNOTATE, BYPASS_IOT)
