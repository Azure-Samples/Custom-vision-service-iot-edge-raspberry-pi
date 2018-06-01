import sys
sys.path.insert(0, '../app/')
import CameraCapture
from CameraCapture import CameraCapture


try:
    print("Test #1 - recorded video - verbose = True")
    with CameraCapture("./AppleAndBanana.mp4", verbose=True, loopVideo=False) as cameraCapture:
        cameraCapture.start()
        print("Test #1 completed")

    print("Test #2 - recorded video - verbose = False")
    with CameraCapture("./AppleAndBanana.mp4", verbose=False, loopVideo=False) as cameraCapture:
        cameraCapture.start()
        print("Test #2 completed")

    print("Test #3 - recorded video - verbose = True")
    with CameraCapture("./AppleAndBanana.mp4", imageProcessingEndpoint='http://localhost:5001/image', verbose=True, loopVideo=False) as cameraCapture:
        cameraCapture.start()
        print("Test #3 completed")

    print("Test #4 - video0 device - verbose = True")
    with CameraCapture("1", verbose=True, loopVideo=False) as cameraCapture:
        cameraCapture.start()
        print("Test #4 completed")

except Exception as exception:
    print ( "Error while executing camera Capture tests: (%s)" % exception)