from CameraCapture import CameraCapture
import CameraCapture
import sys
sys.path.insert(0, '../app/')


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

    print("Test #5 - video0 device - showvideo = True")
    with CameraCapture("../test/AppleAndBanana.mp4", showVideo=True, loopVideo=True, resizeHeight=256, resizeWidth=256) as cameraCapture:
        cameraCapture.start()
        print("Test #5 completed")

except Exception as exception:
    print("Error while executing camera Capture tests: (%s)" % exception)
