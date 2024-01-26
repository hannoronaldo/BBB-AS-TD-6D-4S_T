import time
import math
import Adafruit_BBIO.PWM as PWM

# define the pins for the steering servos
steer_flw = "P9_22"  # set the PWM pin for steering servo of FLW
steer_rlw = "P9_21"  # set the PWM pin for steering servo of RLW
steer_frw = "P9_14"  # set the PWM pin for steering servo of FRW
steer_rrw = "P9_16"  # set the PWM pin for steering servo of RRW

# offset values for the servos
servo_offset_values = [0.5, 0.28, 0.15, -0.65]
#set neutral value for each steering wheel
zsv_flw = 5.5 + servo_offset_values[0]
zsv_rlw = 5.5 + servo_offset_values[1]
zsv_frw = 5.5 + servo_offset_values[2]
zsv_rrw = 5.5 + servo_offset_values[3]

PWM.start(steer_flw, zsv_flw, 50)
PWM.start(steer_rlw, zsv_rlw, 50)
PWM.start(steer_frw, zsv_frw, 50)
PWM.start(steer_rrw, zsv_rrw, 50)

time.sleep(2)

# set the desired angle
PWM.set_duty_cycle(steer_flw, (4 + servo_offset_values[0]))
PWM.set_duty_cycle(steer_rlw, (4 + servo_offset_values[1]))
PWM.set_duty_cycle(steer_frw, (4 + servo_offset_values[2]))
PWM.set_duty_cycle(steer_rrw, (4 + servo_offset_values[3]))

time.sleep(2)


# make cleanup
PWM.stop(steer_flw)
PWM.stop(steer_rlw)
PWM.stop(steer_frw)
PWM.stop(steer_rrw)

PWM.cleanup()
