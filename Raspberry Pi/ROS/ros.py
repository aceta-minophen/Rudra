import RPi.GPIO as GPIO          
from time import sleep
import socket

in1 = 24
in2 = 23
enA = 25
in3 = 12
in4 = 20
enB = 21
temp1=1
y = 0
x = 0

speedA = 25
speedB = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
pA=GPIO.PWM(enA,1000)
pA.start(25)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
pB=GPIO.PWM(enB,1000)
pB.start(25)


# Create a stream based socket(i.e, a TCP socket)
# operating on IPv4 addressing scheme
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# Bind and listen
serverSocket.bind(("0.0.0.0",9090));
serverSocket.listen();
# Accept connections


def stopMoving():
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    
def goForward(y):
    print("forward")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    temp1=1
    
    speedA = 0.85 * y
    speedB = 0.85 * y
    
    print("speedA:" + str(speedA))
    print("speedB:" + str(speedB))
    pA.ChangeDutyCycle(speedA)
    pB.ChangeDutyCycle(speedB)

def goBack(y):
    print("backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    temp1=0
    
    speedA = 0.85 * (-y)
    speedB = 0.85 * (-y)
    
    print("speedA:" + str(speedA))
    print("speedB:" + str(speedB))
    pA.ChangeDutyCycle(speedA)
    pB.ChangeDutyCycle(speedB)

def clockwiseFor():
    print("Clockwise Forward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    
    pA.ChangeDutyCycle(50)
    pB.ChangeDutyCycle(50)

def antiClockwiseFor():
    print("Anti Clockwise Forward")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    
    pA.ChangeDutyCycle(50)
    pB.ChangeDutyCycle(50)
    
def clockwiseBack():
    print("Clockwise Backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    
    pA.ChangeDutyCycle(50)
    pB.ChangeDutyCycle(50)
    
def antiClockwiseBack():
    print("Anti Clockwise backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    
    pA.ChangeDutyCycle(50)
    pB.ChangeDutyCycle(50)
    

while(True):
    (clientConnected, clientAddress) = serverSocket.accept();
    #print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));
    dataFromClient = clientConnected.recv(1024)
    data = dataFromClient.decode()
    data1 = data.replace("+", "")
    data2 = data1.replace(" HTTP/1.1", "")
    data3 = data2.replace("GET /", "")
    data4 = data3.replace("User-Agent: Dalvik/2.1.0 (Linux; U; Android 12; SM-M317F Build/SP1A.210812.016)", "")
    data5 = data4.replace("Host: 192.168.29.47:9090", "")
    data6 = data5.replace("Connection: Keep-Alive","")
    data7 = data6.replace("Accept-Encoding: gzip","")
    data8 = data7.strip()
    val = int(data8)
    print(val);
    
    
    
    if(val <= 200):
        x = 100 - val
    
    if((val>200) and (val<=400)):
        y = val - 300
    
    if((y>=-10) and (y<=10)):
        stopMoving()
        
    if((y>10) and (x<-30)):
        clockwiseFor()
        
        
    if((y>10) and (x>=-30) and (x<=30)):
        goForward(y)
        
    if((y>10) and (x>30)):
        antiClockwiseFor()
        
    if((y<-10) and (x<-30)):
        clockwiseBack()
        
    if((y<-10) and (x>30)):
        antiClockwiseBack()
    
    if((y<-10) and (x>=-30) and (x<=30)):
        goBack(y)
