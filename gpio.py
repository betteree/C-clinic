import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import RPi.GPIO as GPIO
import time

servo_pin1 = 18
servo_pin2 = 14
servo_pin3 = 17
servo_pin4 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)
GPIO.setup(servo_pin3, GPIO.OUT)
GPIO.setup(servo_pin4, GPIO.OUT)

pwm1 = GPIO.PWM(servo_pin1, 30)
pwm2 = GPIO.PWM(servo_pin2, 30)
pwm3 = GPIO.PWM(servo_pin3, 30)
pwm4 = GPIO.PWM(servo_pin4, 30)

pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)

def main():
    cred = credentials.Certificate('login-test-8397d-firebase-adminsdk-8rr6j-5ce64e5b27.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://login-test-8397d-default-rtdb.firebaseio.com/'
    })
    dir = db.reference('angle/angle')  # 기본 위치 지정
    
    
    try:
        angle_value = dir.get()
        print('angle 값:', angle_value)

         # 3번 반복
           
        if angle_value == 0:
            function_for_angle_0()  # angle 값이 0일 때 호출할 함수
        elif angle_value == 1:
            function_for_angle_1()  # angle 값이 1일 때 호출할 함수
        elif angle_value == 2:
            function_for_angle_2()  # angle 값이 2일 때 호출할 함수

    except KeyboardInterrupt:
        pwm1.stop()
        pwm2.stop()
        GPIO.cleanup()

def function_for_angle_0():
    pwm1.ChangeDutyCycle(2.5)  # 180도
    pwm2.ChangeDutyCycle(2.5)  # 180도
    time.sleep(1)
    pwm1.ChangeDutyCycle(5)  # 0도
    pwm2.ChangeDutyCycle(5)  # 0도
    time.sleep(1) 
    return 0

def function_for_angle_1():
    pwm1.ChangeDutyCycle(5)  # 180도
    pwm2.ChangeDutyCycle(2.5)  # 180도
    time.sleep(1)
    pwm1.ChangeDutyCycle(2.5)  # 0도
    pwm2.ChangeDutyCycle(5)  # 0도
    time.sleep(1) 

def function_for_angle_2():
    
    return 0

if __name__ == "__main__":
    main()

