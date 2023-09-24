import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
import cv2
import time

cred = credentials.Certificate('login-test-8397d-firebase-adminsdk-8rr6j-5ce64e5b27.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://login-test-8397d-default-rtdb.firebaseio.com/'
})
xml_face = 'haarcascades/haarcascade_frontalface_default.xml'
xml_eye = 'haarcascades/haarcascade_eye.xml'
face_cascade = cv2.CascadeClassifier(xml_face)
eye_cascade = cv2.CascadeClassifier(xml_eye)

cap = cv2.VideoCapture(0)  # Connect to the webcam on Raspberry Pi
cap.set(3, 320) 
cap.set(4, 240)  

y_diff_list = []  

def main():
    while True:
    # Check Firebase signal
        time=0
        signal_ref = db.reference('switch')  # Change to the actual path in your database
        sin = signal_ref.get()
       
        if sin == 1:
            time=opencv11()
        if time >=10:
            break

    

def opencv11():
    
    start_time = time.time()
    elapsed_time = 0


    while elapsed_time < 10:
        
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.05, 5)

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                eyes = eye_cascade.detectMultiScale(roi_gray)

                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                y_diff = y + h - y
                squared_diff = y_diff ** 2
                print("Squared: {}".format(squared_diff))
                y_diff_list.append(squared_diff)

        cv2.imshow('result', frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  
            break

        elapsed_time = time.time() - start_time

    cap.release()
    cv2.destroyAllWindows()

    if len(y_diff_list) > 0:
        average_squared_diff = np.mean(y_diff_list)
        average_squared_diff_rounded = round(average_squared_diff, 2)
        with open('face_avg.txt', 'w') as f:
            f.write("Average: {:.2f}".format(average_squared_diff_rounded))
        print("Average: {:.2f}".format(average_squared_diff_rounded))

    return elapsed_time

if __name__ == "__main__":
    main()