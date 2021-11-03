#OpenCV の顔認識

import cv2

OBJECT_NAME='tempFace.png'
face_cascade = cv2.CascadeClassifier('C:\ProgramData\Anaconda3\pkgs\libopencv-4.5.1-py37ha0199f4_0\Library\etc\haarcascades\haarcascade_frontalface_default.xml')

if __name__ == '__main__':
  print('start program')

  #f = open(OBJECT_NAME, "rb")
  #img = f.read()
  #f.close()
  img = cv2.imread(OBJECT_NAME)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
  for x, y, w, h in faces:
    print('x: '+ str(x) +', y:'+ str(y) +', w:'+ str(w) +', h:'+ str(h) +'')
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(OBJECT_NAME,img)
