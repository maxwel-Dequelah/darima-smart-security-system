import socket,cv2, pickle,struct
from mysql import connector
import pyshine as ps # pip install pyshine
import imutils # pip install imutils
from datetime import datetime
import cv2 as cv
from threading import Thread
import winsound
import time
import mysql



config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'security'
}

database = mysql.connector.connect(**config)
print(database)

mycursor = database.cursor()

camera = cv.VideoCapture(0)



client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '10.1.0.61' # Here according to your server ip write the address

port = 80
client_socket.connect((host_ip,port))

if client_socket:

    while (camera.isOpened()):
        try:
            ret, frame1 = camera.read()
            ret, frame2 = camera.read()
            #Calculating the absolute difference 
            # of the two frames for motion detection
            dif = cv.absdiff(frame1,frame2)
            gray = cv.cvtColor(dif, cv.COLOR_RGB2GRAY)
            blur = cv.GaussianBlur(gray, [5,5], 0)
            _, thresh = cv.threshold(blur,20, 2555, cv.THRESH_BINARY)
            dilated = cv.dilate(thresh, None, iterations=2)
            contours, _ = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
            def playsound():
                sound = 'CAMERA/alert.wav'
                type = winsound.SND_ASYNC
                return(winsound.PlaySound(sound,type))
            for c in contours:
                if cv.contourArea(c) >= 4000:

                    x, y, w, h = cv.boundingRect(c)
                    cv.rectangle(frame2, (x,y), (x+w, y+h), (255,128,3),2)
                    #th1.start()
                    th2 = Thread(playsound())
                    th2.start()
                   #th1.join()
                    th2.join()
                    dt = datetime.now()
                    imN = str(dt.strftime("%Y_%m_%d-%I:%M:%S_%p"))
                    imName = imN + '.jpg'

                    captured = cv.imwrite(imName,frame1)
            
                
                    print(imName)
                    ###############################
                    #################################
                    # saving images to Mysqldb

                    print(type(imN))
                    #mycursor.execute("INSERT INTO image(Name,image, DTime) VALUES(%s,%s,%s)", (imName,captured, dt))
                    #database.commit()

                    if True:

                        print(f"image {imName} succesfully saved")





                        #THE output videeo frame and frame window name
                        #cv.imshow('from Camera', frame2)
                    a = pickle.dumps(frame1)
                    message = struct.pack("Q",len(a))+a
                    th4=Thread(client_socket.sendall(message))
                    th4.start()
                
                    th5=Thread(cv.imshow(f"TO: {host_ip}",frame1))
                    th5.start()
                    th4.join()

                    key = cv2.waitKey(1) & 0xFF
                
                    th5.join()
                    if key == ord("q"):

                        client_socket.close()
                    



        except Exception as e:
            print('VIDEO FINISHED!')
            break





