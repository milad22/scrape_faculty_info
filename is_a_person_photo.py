import cv2
import numpy as np 
import matplotlib.pyplot as plt

#xlm files copied from here:
#https://github.com/furetosan/FaceDetect
frame = cv2.imread('bianco.jpg')
# print(type(img))
# print(img.shape)
# plt.imshow(img)
# plt.show()

frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
frame_gray = cv2.equalizeHist(frame_gray)

#print(frame_gray.shape)
# plt.imshow(img_gray, cmap='gray')
# plt.show()

path = '/home/miliverse/faculty_data_scrapping_project/scrape_faculty_info/scrape_faculty_info/face_recognition_xml_data/haarcascades/haarcascade_frontalface_alt.xml'
haar_cascade_face = cv2.CascadeClassifier(path)
# Detect faces in the image
faces = haar_cascade_face.detectMultiScale(frame_gray)

print("Found {0} faces!".format(len(faces)))