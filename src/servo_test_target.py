#
import time
import math
import Adafruit_BBIO.PWM as PWM 
import Adafruit_BBIO.GPIO as GPIO

# list of steering values to test the Adafruit lib can manage more than two servos
steering_list = [5.5, 10, 12, 5.5, 2, 6, 9]
# offset to trim the servos to neutral position values = [FLW,RLW,FRW,RRW]
offset_steering = [0.5, 0.28, 0.15, -0.65]

# define the pins for the steering servos
steer_flw = "P9_22"  # set the PWM pin for steering servo of FLW
steer_rlw = "P9_21"  # set the PWM pin for steering servo of RLW
steer_frw = "P9_14"  # set the PWM pin for steering servo of FRW
steer_rrw = "P9_16"  # set the PWM pin for steering servo of RRW


# min and max values for the servo's
duty_min = 2  # set the min PWM percent -> value come from manual tests of the servos
duty_max = 13  # set the max PWM percent-> value come from manual tests of the servos
duty_span = duty_max - duty_min

# initial setup and start the PWM instance ->
# set all steering servos to the 90° neutral position -> must be found by manual tests
# Adafruit_BBIO.PWM has the following arguments: 1 arg=PWM pin, 2arg=duty-cycle, 3arg=frequency
# Adafruit_BBIO.PMW need percentage value for duty cycle!!!!


# calculate the duty cycle for the servos'
# definition: 0°=1ms -> duty_min  180°=2ms -> duty_max
# move the servo to the center or neutral position: 90°=1.5ms -> duty_span/2


# set all steering servos to neutral (90°) position
scv_flw = round((90 * (duty_max-duty_min) / (180 + duty_min) + offset_steering[0]), 2)
scv_rlw = round((90 * (duty_max-duty_min) / (180 + duty_min) + offset_steering[1]), 2)
scv_frw = round((90 * (duty_max-duty_min) / (180 + duty_min) + offset_steering[2]), 2)
scv_rrw = round((90 * (duty_max-duty_min) / (180 + duty_min) + offset_steering[3]), 2)

# initialize the servos to the neutral position
PWM.start(steer_flw, scv_flw, 50)
PWM.start(steer_rlw, scv_rlw, 50)
PWM.start(steer_frw, scv_frw, 50)
PWM.start(steer_rrw, scv_rrw, 50)


# start of steering duty cycle calculation of BBB PWM
# 0°=1ms -> duty_min  180°=2ms -> duty_max based on 90°=1.5ms -> duty_span/2
# loop over a list of steering values

for i in steering_list:

    steering_fl_dc = round(i + offset_steering[0], 2)
    steering_rl_dc = round(i + offset_steering[1], 2)
    steering_fr_dc = round(i + offset_steering[2], 2)
    steering_rr_dc = round(i + offset_steering[3], 2)

    PWM.set_duty_cycle(steer_flw, steering_fl_dc)
    PWM.set_duty_cycle(steer_rlw, steering_rl_dc)
    PWM.set_duty_cycle(steer_frw, steering_fr_dc)
    PWM.set_duty_cycle(steer_rrw, steering_rr_dc)
    # end of the steering section of BBB PWM

    # time delay for finish steering settling
    time.sleep(2)

# set the servos back to the neutral position
PWM.set_duty_cycle(steer_flw, scv_flw)
PWM.set_duty_cycle(steer_rlw, scv_rlw)
PWM.set_duty_cycle(steer_frw, scv_frw)
PWM.set_duty_cycle(steer_rrw, scv_rrw)

# wait for set the steering to neutral position
time.sleep(2)

# end of the drive section of BBB PWM
PWM.stop(steer_flw)
PWM.stop(steer_rlw)
PWM.stop(steer_frw)
PWM.stop(steer_rrw)

PWM.cleanup()
