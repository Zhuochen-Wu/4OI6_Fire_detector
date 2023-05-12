import cv2
import numpy as np
import threading
import urllib.request
import time
import datetime

Alarm_Status = False
Fire_Detected = False
Fire_Reported = 0

def print_alarm_message_function():
    while True:
        if Fire_Detected:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(current_time, ": Suspected fire incident occurred")
        time.sleep(1)

url = 'http://192.168.50.1:8080/?action=stream'
stream = urllib.request.urlopen(url)
byte_stream = b''

cv2.namedWindow("Original Frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("Processed Frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Original Frame", 640, 480)
cv2.resizeWindow("Processed Frame", 640, 480)

while True:
    byte_stream += stream.read(1024)
    a = byte_stream.find(b'\xff\xd8')
    b = byte_stream.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = byte_stream[a:b+2]
        byte_stream = byte_stream[b+2:]
        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Frame processing
        processed_frame = cv2.resize(frame, (960, 540))
        blur = cv2.GaussianBlur(processed_frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        lower = [18, 55, 55]
        upper = [25, 255, 255]
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(hsv, lower, upper)

        output = cv2.bitwise_and(processed_frame, hsv, mask=mask)

        no_red = cv2.countNonZero(mask)

        if int(no_red) > 10000:
            Fire_Reported += 1
        else:
            Fire_Reported = max(0, Fire_Reported - 1)

        cv2.imshow("Original Frame", frame)
        cv2.imshow("Processed Frame", output)

        if Fire_Reported >= 1:
            if Alarm_Status == False:
                threading.Thread(target=print_alarm_message_function).start()
                Alarm_Status = True
            Fire_Detected = True
        else:
            Fire_Detected = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()