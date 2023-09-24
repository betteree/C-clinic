import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
 
 
cred = credentials.Certificate('test-20953-firebase-adminsdk-3knef-828ead12a2.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-20953-default-rtdb.firebaseio.com/'
})
dir_ref = db.reference('cos') #기본 위치 지정

angle_value = dir_ref.get()

# 값 출력
print("angle 값:", angle_value)