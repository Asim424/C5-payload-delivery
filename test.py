from machine import Pin, PWM
from time import sleep
from hcsr04 import HCSR04 # Must have this library saved on Pico to work
import stepper # must have this file saved on Pico

button = Pin(10, Pin.IN, Pin.PULL_DOWN)
us_1 = HCSR04(trigger_pin=21, echo_pin=20) #back
us_2 = HCSR04(trigger_pin=21, echo_pin=20) #front
line_sen = Pin(16, Pin.IN)
reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
# Define the stepper motor pins
IN1 = 2
IN2 = 3
IN3 = 4
IN4 = 5

# Initialize the stepper motor
stepper_motor = stepper.HalfStepMotor.frompins(IN1, IN2, IN3, IN4)

# Set the current position as position 0
stepper_motor.reset()

region = 1 #0 = box zone, 1 = middle, 2 = drop off

# === L298N Motor Driver ===
# Motor L
motor_L_in1 = Pin(6, Pin.OUT)
motor_L_in2 = Pin(7, Pin.OUT)
motor_L_en = PWM(Pin(8))
motor_L_en.freq(1000)
motor_L_correction = 1.0 # Adjust so both motors have same speed

# Motor R
motor_R_in3 = Pin(4, Pin.OUT)
motor_R_in4 = Pin(3, Pin.OUT)
motor_R_en = PWM(Pin(2))
motor_R_en.freq(1000)
motor_R_correction = 1.0 # Adjust so both motors have same speed

# both turn fucntions turn 90 degrees, the time variables do not need to be the same

def forwards():
    motor_L_in1.value(0)
    motor_L_in2.value(1)
    motor_R_in3.value(1)
    motor_R_in4.value(0)
    sleep(time)

def turn_right():
    motor_L_in1.value(0)
    motor_L_in2.value(1)
    motor_R_in3.value(0)
    motor_R_in4.value(1)
    sleep(time)

def turn_left():
    motor_L_in1.value(1)
    motor_L_in2.value(0)
    motor_R_in3.value(1)
    motor_R_in4.value(0)
    sleep(time)

def backwards():
    motor_L_in1.value(1)
    motor_L_in2.value(0)
    motor_R_in3.value(0)
    motor_R_in4.value(1)
    sleep(time)

def around_obstacle():
    turn_left()
    while(us_1.distance_cm()<= 2):
        forwards()
        sleep(time)
    turn_right()
    while(us_1.distance_cm()<= 2):
        forwards()
        sleep(time)
    turn_right()
    while(line_sen.value() != 0):
        forwards()
        sleep(time)
    turn_left()

def pickup():
    stepper_motor.step(3200)
    sleep(0.5)
    backwards()
    stepper_motor.step(-3200)
    sleep(0.5) # stop for a while
    forwards()
    turn_left()
    turn_left()


# initialize
while(line_sen.value() != 0):
    pass
    forwards()
turn_right()

while (True):
    if(button.value() != 1 and reed_switch.value() != 1):
        pass
        forwards()
    elif (reed_switch.value() == 1):
         pickup()
    elif(button.value() == 1): 
        around_obstacle()
    