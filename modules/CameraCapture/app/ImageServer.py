# Imports for the REST API
from flask import Flask, Response, render_template
import time
import base64
import threading

IMAGE_SERVER_ALIVE = True

class ImageServer(threading.Thread):
    def __init__(self, ipAddr, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ipAddr = ipAddr
        self.port = port
        self.current_frame = None
        self.app = Flask(__name__)

    def run(self):
        try:
            @self.app.route('/')
            def index():
                return render_template('index.html')

            @self.app.route('/video_feed')
            def video_feed():
                return Response(self.gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

            self.app.run(host=self.ipAddr, port=self.port)
        except Exception as e:
            print('ImageServer::exited run loop. Exception - '+ str(e))

    def gen(self):
        while IMAGE_SERVER_ALIVE:
            frame = self.current_frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def update_frame(self, frame):
        try:
            self.current_frame = frame
        except Exception as e:
            print('ImageServer::update_frame Exception - ' + str(e))

    def close(self):
        global IMAGE_SERVER_ALIVE
        IMAGE_SERVER_ALIVE = False
        print ('ImageServer::Closed.')