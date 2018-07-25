import os
import requests
if sys.version_info[0] < 3:#e.g python version <3
    from urllib2 import urlopen
    #import cv2
else:
    from urllib.request import urlopen
    #from cv2 import cv2

# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
#import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key. Subscription Key is being passed as an Environment Variable.
subscription_key = os.getenv("SUBSCRIPTION_KEY")
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the westcentralus region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

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
def analyze_url_external(subscription_key, analyze_url, imageUrl):
    print('Predicting from url: ',imageUrl)
    #with urlopen(imageUrl) as testImage: # python 3 implementation? requires __start__ & __End___ ->Context manager is missing in urllib2
    testImage = urlopen(imageUrl).read()
    image_data = testImage
    image_caption = analyze_image_external(subscription_key, analyze_url, image_data)
    return image_caption
def analyze_image_external(subscription_key, analyze_url, image):
    image_data = image 
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    response   = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    return image_caption
