# The steps implemented in the object detection sample code: 
# 1. for an image of width and height being (w, h) pixels, resize image to (w', h'), where w/h = w'/h' and w' x h' = 262144
# 2. resize network input size to (w', h')
# 3. pass the image to network and do inference
# (4. if inference speed is too slow for you, try to make w' x h' smaller, which is defined with DEFAULT_INPUT_SIZE (in object_detection.py or ObjectDetection.cs))
from urllib.request import urlopen
from datetime import datetime

import sys
import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
from object_detection import ObjectDetection

MODEL_FILENAME = 'model.tflite'
LABELS_FILENAME = 'labels.txt'

class TFLiteObjectDetection(ObjectDetection):
    """Object Detection class for TensorFlow Lite"""
    def __init__(self, model_filename, labels):
        super(TFLiteObjectDetection, self).__init__(labels)
        self.interpreter = tflite.Interpreter(model_path=model_filename)
        self.interpreter.allocate_tensors()
        self.input_index = self.interpreter.get_input_details()[0]['index']
        self.output_index = self.interpreter.get_output_details()[0]['index']

    def predict(self, preprocessed_image):
        inputs = np.array(preprocessed_image, dtype=np.float32)[np.newaxis, :, :, (2, 1, 0)]  # RGB -> BGR and add 1 dimension.

        # Resize input tensor and re-allocate the tensors.
        self.interpreter.resize_tensor_input(self.input_index, inputs.shape)
        self.interpreter.allocate_tensors()
        
        self.interpreter.set_tensor(self.input_index, inputs)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(self.output_index)[0]

def log_msg(msg):
    print("{}: {}".format(datetime.now(),msg))

def initialize():
    print('Loading model...',end=''),
    # Load labels
    with open(LABELS_FILENAME, 'r') as f:
        labels = [l.strip() for l in f.readlines()]

    global od_model
    od_model = TFLiteObjectDetection(MODEL_FILENAME, labels)
#    image = Image.open("apple1.jpg")
#    image = Image.open("banana1.jpg")
#    predict_image(image)
    print(len(labels), 'found. Success!')

def predict_image(image):
    predictions = od_model.predict_image(image)
    print(predictions)
    response = { 
        'id': '',
        'project': '',
        'iteration': '',
        'created': datetime.utcnow().isoformat(),
        'predictions': predictions 
    }
    return response

def predict_url(imageUrl):
    with urlopen(imageUrl) as testImage:
        image = Image.open(testImage)
        predict_image(image)
