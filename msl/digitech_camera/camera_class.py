from time import time_ns
import numpy as np
import cv2

import matplotlib.pyplot as plt


class Camera(object):

    def __init__(self, id):
        # Variables
        self.id = id
        self.cam = self.connect()

    def connect(self):
        print("Connecting to camera")
        # Open the device at the ID
        cap = cv2.VideoCapture(self.id)
        # Check whether user selected camera is opened successfully.
        if not (cap.isOpened()):
            print("Could not open video device")
            return None
        else:
            print("Camera initialised")
            return cap

    def set_resolution(self):
        pass
        # To set the resolution
        # cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        # cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

    def take_image(self, display=True, y1=200, y2=400, threshold2=20):
        ret, frame = self.cam.read()
        height, width, dim = frame.shape
        print(height, width, dim)
        edge_data = []
        times = []
        while ret:
            ret, frame = self.cam.read()
            roi = frame[:, y1:y1 + y2]
            # Include image data processing here: in this case, use Canny edge detection to find the edge
            edges = cv2.Canny(roi, 0, threshold2)
            t_s = time_ns() / 1e9
            times.append(t_s)
            edge_data.append(np.median(([np.argmax(a) for a in np.transpose(edges)])))

            if display:
                # cv2.imshow("Raw image", frame)
                cv2.imshow("ROI", roi)
                cv2.imshow("Edges", edges)

            # Wait for a user input to quit the application
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        return times, edge_data

    def disconnect(self):
        # When everything done, release the capture
        self.cam.release()
        cv2.destroyAllWindows()



cam = Camera(id=1)
times, edge_data = cam.take_image(display=True,
                       y1=000, y2=300,
                       threshold2=180)

fig = plt.plot(edge_data)
plt.show()