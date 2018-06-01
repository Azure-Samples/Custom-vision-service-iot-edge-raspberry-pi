# Copyright (c) Emmanuel Bertrand. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import os
import random
import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientRetryPolicy
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
import DisplayManager
from DisplayManager import DisplayManager
import MessageParser
from MessageParser import MessageParser
import json

RECEIVE_CALLBACKS = 0

# receive_message_callback is invoked when an incoming message arrives on the specified  input queue
def receive_message_callback(message, HubManager):
    global RECEIVE_CALLBACKS
    RECEIVE_CALLBACKS += 1
    print("Received message #: "+ str(RECEIVE_CALLBACKS))
    message_buffer = message.get_bytearray()
    body=message_buffer[:len(message_buffer)].decode('utf-8')
    allTagsAndProbability = json.loads(body)
    DISPLAY_MANAGER.displayImage(MESSAGE_PARSER.highestProbabilityTagMeetingThreshold(allTagsAndProbability, THRESHOLD))
    return IoTHubMessageDispositionResult.ACCEPTED

class HubManager(object):

    def __init__(self, connection_string):
        # Defines settings of the IoT SDK
        self.client = IoTHubClient(connection_string, IoTHubTransportProvider.MQTT)
        self.client.set_option("logtrace", 1)#enables MQTT logging
        self.client.set_option("messageTimeout", 10000)
        #self.client.set_retry_policy(IoTHubClientRetryPolicy.RETRY_INTERVAL, 50)
        self.set_certificates()
        # sets the callback when a message arrives on "input1" queue.  Messages sent to 
        # other inputs or to the default will be silently discarded.
        self.client.set_message_callback("input1", receive_message_callback, self)
        print ( "Module is now waiting for messages in the input1 queue.")

        

    def set_certificates(self):
        isWindows = sys.platform.lower() in ['windows', 'win32']
        if not isWindows:
            CERT_FILE = os.environ['EdgeModuleCACertificateFile']        
            print("Adding TrustedCerts from: {0}".format(CERT_FILE))
            # this brings in x509 privateKey and certificate
            file = open(CERT_FILE)
            try:
                self.client.set_option("TrustedCerts", file.read())
                print ( "set_option TrustedCerts successful" )
            except IoTHubClientError as iothub_client_error:
                print ( "set_option TrustedCerts failed (%s)" % iothub_client_error )
            file.close()


def main(connection_string):
    try:
        print ( "Starting the SenseHat module...")

        global DISPLAY_MANAGER
        global MESSAGE_PARSER
        DISPLAY_MANAGER = DisplayManager()
        MESSAGE_PARSER = MessageParser()
        hubManager = HubManager(connection_string)

        while True:
            time.sleep(1000)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    try:
        CONNECTION_STRING = os.environ['EdgeHubConnectionString']
        global THRESHOLD
        THRESHOLD = float(os.getenv('THRESHOLD', 0))

    except Exception as error:
        print ( error )
        sys.exit(1)

    main(CONNECTION_STRING)