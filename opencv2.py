import numpy as np
import cv2
import time
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('login-test-8397d-firebase-adminsdk-8rr6j-5ce64e5b27.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://login-test-8397d-default-rtdb.firebaseio.com/'
})
xml_face = 'haarcascades/haarcascade_frontalface_default.xml'
xml_eye = 'haarcascades/haarcascade_eye.xml'
face_cascade = cv2.CascadeClassifier(xml_face)
eye_cascade = cv2.CascadeClassifier(xml_eye)

cap = cv2.VideoCapture(0)  # Raspberry Pi에 연결된 웹캠 사용
cap.set(3, 320)  # 너비 설정
cap.set(4, 240)  # 높이 설정



#face_avg.txt에서 숫자만 추출하여 평균값으로 사용
with open('face_avg.txt', 'r') as f:
    content = f.read()
    average_squared_diff = float(content.split(': ')[1])
ref = db.reference('/')
firebase_cnt = 0
time_reached_5 = None

def main():
    
    while True:
        
        signal_ref = db.reference('switch')  # Change to the actual path in your database
        sin = signal_ref.get()

        if sin == 1:
            opencv22()
            break
            

# 누적 cnt 값 및 5가 되는 시간 기록을 위한 변수
def opencv22():
    global time_reached_5
    cnt = 0
    reached_threshold = False 
    start_time = time.time()
    elapsed_time = 0
    while True:
        cos_ref = db.reference('camera/camera')
        cos = cos_ref.get()
        ret, frame = cap.read()
        if not ret:  # 프레임을 정상적으로 읽지 못한 경우
            continue
        frame = cv2.flip(frame, 1)  #좌우 반전
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.05, 5)

        elapsed_time = time.time() - start_time

        if elapsed_time >= 10:
            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    diff_y = y + h - y
                    squared_diff = diff_y ** 2

                    if squared_diff - average_squared_diff >= 8000:
                        cnt += 1

                        if cnt >= 5:
                            reached_threshold = True  # 플래그 설정
                            print("누적 횟수: {}".format(cnt))
                            time_reached_5 = datetime.now()
                            month = time_reached_5.month
                            day = time_reached_5.day
                            hour = time_reached_5.hour
                            minute = time_reached_5.minute
                            second = time_reached_5.second
                            print("(시간: {})".format(time_reached_5))
                            ref.update({
                            'warn': 1,
                            'month':  month,
                            'day':  day,
                            'hour': hour,
                            'minute': minute,
                            'second': second,
                            }
                        )
                            if cos == 1:
                                break
                            else:
                                cnt=0
                                opencv22()

                        roi_gray = gray[y:y + h, x:x + w]
                        roi_color = frame[y:y + h, x:x + w]
                        ref.update({
                            'cnt': cnt,
                        })
                        

                if elapsed_time % 60 == 0:
                    print("상하 차이의 제곱: {}".format(squared_diff))
                    print("누적 횟수: {}".format(cnt))

                start_time = time.time()  # 시작 시간 재설정

            if reached_threshold:  # 임계값에 도달하면 종료
                break

        cv2.imshow('결과', frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # ESC 키를 누르면 종료
            break

    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
