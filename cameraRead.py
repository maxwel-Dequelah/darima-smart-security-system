import threading
from typing import Concatenate
import cv2 as cv
import winsound
from threading import Thread
from datetime import datetime
from time import sleep


from datetime import datetime
import mysql.connector


#################################
#################################
#Database configuration


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



while True:
    #ACCEPTING TWO CAMERA FRAMES 
    #(ret== retry variable, Frame1,2 == Videoframes)

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
        sound = 'alert.wav'
        type = winsound.SND_ASYNC and winsound.SND_NOWAIT
        return(winsound.PlaySound(sound,type))
    for c in contours:
        if cv.contourArea(c) >= 4000:

             x, y, w, h = cv.boundingRect(c)
            cv.rectangle(frame2, (x,y), (x+w, y+h), (255,128,3),2)
            #th1.start()
            th2 = Thread(playsound())
            th2.start()
            sleep(2)
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
            mycursor.execute("INSERT INTO image(Name,image, DTime) VALUES(%s,%s,%s)", (imName,captured, dt))
            database.commit()


    #THE output videeo frame and frame window name
    (cv.imshow('from Camera', frame2))

        #########EXITING WHEN KEY Q IS PRESSED
    if cv.waitKey(5) == ord('q'):
        print('Exiting in 0 seconds...')
        break
        cv.destroyWindow()

