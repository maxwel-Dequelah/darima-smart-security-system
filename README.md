# darima-smart-security-system


This is a  project on opencv Python

the three main python scripts are:
    Camera read.py
    - this is responsible for reading the camera.
    - Startin a motionn sensor
    - play the alert.wav file incase motion is detected
   server.py
      - starts a socket server
      - picks the videoframe from cameraread.py
      - sends it to a soocket server
   client.py
      - starts a stream connection to socket server(server.py)
      - picks videoframe using pickle module, unpacks 
      uses the opencv's imshow() methord to display the videoframe.
      
     
     configure your PC's ip idress on the client.py
     
     set up a database named image and create a table named on Xammp sever's Htdocs
     
    
    
