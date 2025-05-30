import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, ENA, IN1, IN2, ENB, IN3, IN4):
        self.ENA = ENA
        self.IN1 = IN1
        self.IN2 = IN2
        self.ENB = ENB
        self.IN3 = IN3
        self.IN4 = IN4
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.ENA, 100)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.ENB, 100)
        self.pwmB.start(0)
        
    def move(self, speed=0.5, turn=0, time=0):
        speed = int(speed * 100)
        turn = int(turn * 100)
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        
        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
            
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100
            
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        
        if leftSpeed > 0:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
        elif leftSpeed < 0:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            
        if rightSpeed > 0:
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
        elif rightSpeed < 0:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
        sleep(time)
        
    def stop(self, time=0):
        self.pwmA.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwmB.ChangeDutyCycle(0)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        sleep(time)
    
    def cleanup(self):
        self.pwmA.stop()
        self.pwmB.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    motor= Motor(27, 17, 18, 24, 22, 23)
    while True:
        motor.move(speed=0.2, time=0.2)
        print("Di")