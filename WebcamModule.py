from picamera2 import Picamera2
import cv2
import numpy as np

picam = Picamera2()
# picam.configure(picam.create_preview_configuration(main={"size": picam.sensor_resolution}))
picam.configure(picam.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
picam.start()

def getImg(display=False, size=[640, 640]):
    img = picam.capture_array()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (size[0], size[1]))
    
    if display:
        cv2.imshow('IMG', img)
        cv2.waitKey(1)
    
    return img

if __name__ == '__main__':
    try:
        while True:
            img = getImg(True)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        picam.stop()
        cv2.destroyAllWindows()