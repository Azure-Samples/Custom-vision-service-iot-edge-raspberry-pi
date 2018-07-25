import requests
from urllib.request import urlopen

# If using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
# Sucscription key for Azure cognitive services
subscription_key = "55b5b49fc2cb4438a3927576fe2e2938"
assert subscription_key

# Must use the same region in your REST call as you used to get your subscription keys. 

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
image_src = "C:\Users\\a-paasga\\Documents\\Hackathon\\BearDetection\\samples\\bearcubs.jpg"#"https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/2010-brown-bear.jpg/200px-2010-brown-bear.jpg"

# get the Cogntive Services Computer Vision URL
def get_analysis_url(url):
    vision_base_url = str(url)
    vision_url = vision_base_url + "analyze"
    return vision_url
# not used unless we want to import image form local storage
def get_image_local(path):
    image_data = open(path, "rb").read()
    return image_local
# analyze/classifies an image from url utilizing Cognetive Services's Computer Vision (cloud service)
def predict_url_external(subscription_key, analyze_url, imageUrl):
    print('Predicting from url: ',imageUrl)
    #with urlopen(imageUrl) as testImage: # python 3 implementation? requires __start__ & __End___ ->Context manager is missing in urllib2
    testImage = urlopen(imageUrl).read()
    image_data = testImage
    image_caption = predict_image_external(subscription_key, analyze_url, image_data)
    return image_caption
def predict_image_external(subscription_key, analyze_url, image):
    image_data = image 
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    response   = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    return image_caption