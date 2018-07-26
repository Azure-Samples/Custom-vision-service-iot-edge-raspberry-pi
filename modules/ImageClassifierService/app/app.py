
import json
import os
import io

# Imports for the REST API
from flask import Flask, request

# Imports for image procesing
from PIL import Image
#import scipy
#from scipy import misc

# Imports for prediction
from predict import initialize, predict_image, predict_url

app = Flask(__name__)

# Replace <Subscription Key> with your valid subscription key. Subscription Key is being passed as an Environment Variable.
subscription_key = os.getenv("SUBSCRIPTION_KEY")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
# assert subscription_key

# 4MB Max image size limit
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 

# Default route just shows simple text
@app.route('/')
def index():
    return 'CustomVision.ai model host harness'

notification_sent = False

# Like the CustomVision.ai Prediction service /image route handles either
#     - octet-stream image file 
#     - a multipart/form-data with files in the imageData parameter
@app.route('/image', methods=['POST'])
def predict_image_handler():
    try:
        imageData = None
        if ('imageData' in request.files):
            imageData = request.files['imageData']
        else:
            imageData = io.BytesIO(request.get_data())

        #img = scipy.misc.imread(imageData)
        img = Image.open(imageData)
        results = predict_image(img)

        # local model
        highestProb = highestProbabilityTagMeetingThreshold(results, 0.3)

        # cloud model
        if highestProb < 0.6:
            cloudResult = analyze_image_external(img)

            if "tags" in cloudResult:
                tags = cloudResult["tags"]
                print(tags)

                if "bear" in tags and notification_sent == False:
                    push_notification()
        else:
            if notification_sent == False:
                push_notification()

        return json.dumps(results)
    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image', 500

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

# get the Cogntive Services Computer Vision URL
def get_analysis_url(url):
    vision_base_url = str(url)
    vision_url = vision_base_url + "analyze"
    return vision_url

#Returns the highest probablity tag in the json object (takes the output as json.loads as input)
def highestProbabilityTagMeetingThreshold(allTagsAndProbability, threshold):
    highestProbabilityTag = 'none'
    highestProbability = 0
    for item in allTagsAndProbability:
        if item['Probability'] > highestProbability and item['Probability'] > threshold:
            highestProbability = item['Probability']
            highestProbabilityTag = item['Tag']
    return highestProbability

def analyze_image_external(image):
    image_data = image 
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    analyze_url = get_analysis_url(vision_base_url)
    response   = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    return image_caption

def push_notification():
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": pushover_token,
        "user": pushover_user,
        "message": "Bear Alert",
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# Like the CustomVision.ai Prediction service /url route handles url's
# in the body of hte request of the form:
#     { 'Url': '<http url>'}  
@app.route('/url', methods=['POST'])
def predict_url_handler():
    try:
        image_url = json.loads(request.get_data())['Url']
        results = predict_url(image_url)
        return json.dumps(results)
    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image'

if __name__ == '__main__':
    # Load and intialize the model
    initialize()

    # Run the server
    app.run(host='0.0.0.0', port=80)

