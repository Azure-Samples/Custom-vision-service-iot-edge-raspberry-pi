
from urllib.request import urlopen

import tensorflow as tf

from PIL import Image
import numpy as np
# import scipy
# from scipy import misc
import sys
import os  

filename = 'model.pb'
labels_filename = 'labels.txt'

network_input_size = 227
mean_values_b_g_r = (0,0,0)

size = (256, 256)
output_layer = 'loss:0'
input_node = 'Placeholder:0'

graph_def = tf.GraphDef()
labels = []

def initialize():
    print('Loading model...',end=''),
    with tf.gfile.FastGFile(filename, 'rb') as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
    print('Success!')
    print('Loading labels...', end='')
    with open(labels_filename, 'rt') as lf:
        for l in lf:
            l = l[:-1]
            labels.append(l)
    print(len(labels), 'found. Success!')
    
def crop_center(img,cropx,cropy):
    y,x,z = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)
    print('crop_center: ', x, 'x', y, 'to', cropx, 'x', cropy)
    return img[starty:starty+cropy,startx:startx+cropx]

def predict_url(imageUrl):
    print('Predicting from url: ',imageUrl)
    with urlopen(imageUrl) as testImage:
        # image = scipy.misc.imread(testImage)
        image = Image.open(testImage)
        return predict_image(image)

def predict_image(image):
    print('Predicting image')
    tf.reset_default_graph()
    tf.import_graph_def(graph_def, name='')
    
    with tf.Session() as sess:
        prob_tensor = sess.graph.get_tensor_by_name(output_layer)

        # w = image.shape[0]
        # h = image.shape[1]
        w, h = image.size
        print('Image size',w,'x',h)

        # scaling
        if w > h:
            new_size = (int((float(size[1]) / h) * w), size[1], 3)
        else:
            new_size = (size[0], int((float(size[0]) / w) * h), 3)

        # resize
        if  not (new_size[0] == w and new_size[0] == h):
            print('Resizing to', new_size[0],'x',new_size[1])
            #augmented_image = scipy.misc.imresize(image, new_size)
            augmented_image = np.asarray(image.resize((new_size[0], new_size[1])))
        else:
            augmented_image = np.asarray(image)

        # crop center
        try:
            augmented_image = crop_center(augmented_image, network_input_size, network_input_size)
        except:
            return 'error: crop_center'

        augmented_image = augmented_image.astype(float)

        # RGB -> BGR
        red, green, blue = tf.split(axis=2, num_or_size_splits=3, value=augmented_image)

        image_normalized = tf.concat(axis=2, values=[
            blue - mean_values_b_g_r[0],
            green - mean_values_b_g_r[1],
            red - mean_values_b_g_r[2],
        ])

        image_normalized = image_normalized.eval()
        image_normalized = np.expand_dims(image_normalized, axis=0)

        predictions, = sess.run(prob_tensor, {input_node: image_normalized})

        result = []
        idx = 0
        for p in predictions:
            truncated_probablity = np.float64(round(p,8))
            if (truncated_probablity > 1e-8):
                result.append({'Tag': labels[idx], 'Probability': truncated_probablity })
            idx += 1
        print('Results: ', str(result))
        return result
