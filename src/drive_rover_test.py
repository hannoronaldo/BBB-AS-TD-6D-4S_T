#
import time
import math
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

speed = 100
direction = 1

# definition section
# if forward=1 backward=0 will realize over a dual pole switch IC hardware side has a pull up!
forward_backward_switch = 'P9_12'
GPIO.setup(forward_backward_switch, GPIO.OUT)

#define BBB IO pins for the motor drive PWM
#check is ECAP PWM pins are avalible
drive_owl = "P8_13"  # set the PWM pin for drive the outer wheels left side!!! only if the dimension front and rear equal!!!
#drive_mwl = 'P9_42'  # set the PWM pin for drive the mid wheel left side
drive_owr = "P8_19"  # set the PWM pin for drive the outer wheels right side!!! only if the dimension front and rear equal!!!
#drive_mwr = 'P9_28'  # set the PWM pin for drive the mid wheel right side

# set the drive speed to zero for outer and mid wheels
PWM.start(drive_owl, 0, 200)
#PWM.start(drive_mwl, 0, 200)
PWM.start(drive_owr, 0, 200)
#PWM.start(drive_mwr, 0, 200)

# start of drive section of BBB PWM
if direction:

    GPIO.output(forward_backward_switch, GPIO.HIGH)  # set forward/backward switch to forward
    print('drive direction is forward')

else:

    GPIO.output(forward_backward_switch, GPIO.LOW)  # set forward/backward switch to backward
    print('drive direction is backward')

PWM.set_duty_cycle(drive_owl, speed)
#PWM.set_duty_cycle(drive_mwl, speed)
PWM.set_duty_cycle(drive_owr, speed)
#PWM.set_duty_cycle(drive_mwr, speed)

#TODO check speed to travel distance
wheel_cir = math.pi * 226.5
# wheel_rotations = dist_to_travel / wheel_cir
run_time = wheel_cir / speed
time.sleep(run_time)

PWM.stop(drive_owl)
#PWM.stop(drive_mwl)
PWM.stop(drive_owr)
#PWM.stop(drive_mwr)
PWM.cleanup()
GPIO.cleanup()
