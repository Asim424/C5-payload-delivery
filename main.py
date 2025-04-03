from machine import Pin, PWM, ADC
from time import sleep
from hcsr04 import HCSR04 # Must have this library saved on Pico to work
import stepper # must have this file saved on Pico
# 
# 
# WARNING, GET RID OF THE FRONT US STAND IT FUCKS SHIT UP, SAUTER THE WIRES
# BLUE PURPLE WHITE TO PICO WHITE TO POWER
# 
# 
# 
ir = ADC(28)
button = Pin(10, Pin.IN, Pin.PULL_DOWN)
us_1 = HCSR04(trigger_pin=19, echo_pin=18) #back
us_2 = HCSR04(trigger_pin=26, echo_pin=27) #front
line_sen = Pin(16, Pin.IN)
led = Pin('LED', Pin.OUT)
reed_switch = Pin(15, Pin.IN, Pin.PULL_DOWN)
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
time = 1
# === L298N Motor Driver ===
# Motor R
motor_L_in1 = Pin(6, Pin.OUT)
motor_L_in2 = Pin(7, Pin.OUT)
motor_L_en = PWM(Pin(8))
motor_L_en.freq(1000)
motor_L_correction = 1 # Adjust so both motors have same speed

# Motor L
motor_R_in3 = Pin(12, Pin.OUT)
motor_R_in4 = Pin(11, Pin.OUT)
motor_R_en = PWM(Pin(13))
motor_R_en.freq(1000)
motor_R_correction = 1.05 # Adjust so both motors have same speed

# Function to control Motor A
def motor_L(direction = "stop", speed = 0):
    adjusted_speed = int(speed * motor_L_correction)  # Apply correction
    if direction == "forward":
        motor_L_in1.value(0)
        motor_L_in2.value(1)
    elif direction == "backward":
        motor_L_in1.value(1)
        motor_L_in2.value(0)
    else:  # Stop
        motor_L_in1.value(0)
        motor_L_in2.value(0)
    motor_L_en.duty_u16(int(adjusted_speed * 65535 / 100))  # Speed: 0-100%

# Function to control Motor B
def motor_R(direction = "stop", speed = 0):
    adjusted_speed = int(speed * motor_R_correction)  # Apply correction
    if direction == "forward":
        motor_R_in3.value(1)
        motor_R_in4.value(0)
    elif direction == "backward":
        motor_R_in3.value(0)
        motor_R_in4.value(1)
    else:  # Stop
        motor_R_in3.value(0)
        motor_R_in4.value(0)
    motor_R_en.duty_u16(int(adjusted_speed * 65535 / 100))  # Speed: 0-100%


# both turn fucntions turn 90 degrees, the time variables do not need to be the same

def forwards():
    motor_L(direction = "forward", speed = 50)
    motor_R(direction = "forward", speed = 50)
    sleep(0.1)

def turn_right():
    motor_L(direction = "forward", speed = 50)
    motor_R(direction = "backward", speed = 50)
    sleep(0.25)
    stop()

def turn_left():
    motor_L(direction = "backward", speed = 50)
    motor_R(direction = "forward", speed = 50)
    sleep(0.25)
    stop()

def stop():
    motor_R()
    motor_L()

def backwards():
    motor_L(direction = "backward", speed = 50)
    motor_R(direction = "backward", speed = 50)
    sleep(0.1)

def around_obstacle():
    turn_right()
    while(us_1.distance_cm()<= 2):
        forwards()
        sleep(time)
    turn_left()
    while(us_1.distance_cm()<= 2):
        forwards()
        sleep(time)
    turn_left()
    while(line_sen.value() != 0):
        forwards()
        sleep(time)
    turn_right()

def pickup():
    stepper_motor.step(3200)
    sleep(0.5)
    backwards()
    stepper_motor.step(-3200)
    sleep(0.5) # stop for a while
    forwards()
    turn_left()
    turn_left()

led.value(0)
sleep(1)
led.value(1)
sleep(0.25)
led.value(0)
turn_left()
while True:
    print(us_2.distance_cm())
    sleep(0.1)
# # initialize
# while(line_sen.value() != 0):
#     forwards()
# stop()
# turn_right()

# while (True):
#     if(button.value() != 1 and reed_switch.value() != 1):
#         forwards()
#     elif (reed_switch.value() == 1):
#          pickup()
#     elif(button.value() == 1): 
#         around_obstacle()
    