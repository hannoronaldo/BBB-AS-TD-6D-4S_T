#
import time
import math
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

# acronym table
# FLW = FrontLeftWheel MLW = MidLeftWheel RLW= RightLeftWheel
# FRW = FrontRightWheel MRW = MidRightWheel RRW = RearRightWheel


# global variable block
dim_front2mid_wheel: int = 235  # dimension from middle to front  wheel
dim_rear2mid_wheel: int = 210  # dimension from middle to back wheel
dim_frontwheel_base: int = 330  # dimension between the front wheels
dim_midwheel_base: int = 415  # dimension between the middle wheels
dim_rearwheel_base: int = 340  # dimension between the rear wheels

# wheel diameter and with definition for later use of calculate the traveled distance
wheel_diameter = 85
wheel_width = 53

# offset to trim the servos to neutral position values = [FLW,RLW,FRW,RRW]
offset_steering = [0.5, 0.28, 0.15, -0.65]

# rover_Drive dict has this content
# rover_Drive['drive_direction'] : ('forward' or 'backward')
# rover_Drive['steering_direction'] : ('right' or 'left')
# rover_Drive['cor'] : value of 'cor'(center of rotation)
# rover_Drive[name_of_the_wheel] : (steering_value, motor_speed)]
rover_Drive = {}

# hypotenuse values are an indicator for the speed calculation and for the
# arc diameter for the graphical representation
# value order of hypotenuse_values list
# hypo_FLW|hypo_MLW|hypo_RLW|hypo_FRW|hypo_MRW|hypo_RRW
hypotenuse_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# dict for wheel position
# 1. mid point of wheel 2. position of later calculated draw line
wheel_dict = {'MLW': [-dim_midwheel_base / 2, 0],
              'MRW': [dim_midwheel_base / 2, 0],
              'FLW': [-dim_frontwheel_base / 2, dim_front2mid_wheel],
              'FRW': [dim_frontwheel_base / 2, dim_front2mid_wheel],
              'RLW': [-dim_rearwheel_base / 2, -dim_rear2mid_wheel],
              'RRW': [dim_rearwheel_base / 2, -dim_rear2mid_wheel]}


# __________________________


# define function block
def cal_steering_and_speed(speed, cor):
    """
    cal_steering_and_speed ->
    calculates the steering angle (in degree) and motor speed (in percentage)
    of each wheel
    :param speed: amount of percentage -100 up to +100%
    :param cor: virtual center of rotation of the rover
    (calculated in function: ackermann_steering)
    :return: none
    """

    # set speed value to positive to calculate the duty cycle if the value is negative
    if speed < 0:
        speed -= speed * 2

    # steering_value list only a temp list for internal use in this function
    # steering_values order -> degree_FLW|degree_RLW|degree_RLW|degree_RRW
    steering_values = [0.0, 0.0, 0.0, 0.0]
    # motor_speed value list only a temp list for internal use in this function
    # value order -> speed_FLW|speed_MLW|speed_RLW|speed_FRW|speed_MRW|speed_RRW
    motor_speed = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # inner angle atan() = cor - dim_frontwheel_base/2
    # outer angle atan() = cor + dim_frontwheel_base/2

    if rover_Drive['steering_direction'] == 'right':
        # value order of steering_values list -> degree_FLW|degree_RLW|degree_FRW|degree_RRW
        steering_values[0] = round(math.degrees(math.atan(dim_front2mid_wheel / (cor + dim_frontwheel_base / 2))), 5)
        steering_values[1] = round(math.degrees(math.atan(dim_rear2mid_wheel / (cor + dim_rearwheel_base / 2))), 5)
        steering_values[2] = round(math.degrees(math.atan(dim_front2mid_wheel / (cor - dim_frontwheel_base / 2))), 5)
        steering_values[3] = round(math.degrees(math.atan(dim_rear2mid_wheel / (cor - dim_rearwheel_base / 2))), 5)

        # calculate the hypotenuse of each wheel to calculate the speed for each motor
        # value order of hypotenuse_values list
        # hypo_FLW|hypo_MLW|hypo_RLW|hypo_FRW|hypo_MRW|hypo_RRW
        hypotenuse_values[0] = round(math.sqrt(
            (cor + (-wheel_dict['FLW'][0])) * (cor + (-wheel_dict['FLW'][0])) + wheel_dict['FLW'][1] *
            wheel_dict['FLW'][1]), 3)

        hypotenuse_values[1] = round(math.sqrt(
            (cor + (-wheel_dict['MLW'][0])) * (cor + (-wheel_dict['MLW'][0])) + wheel_dict['MLW'][1] *
            wheel_dict['MLW'][1]), 3)

        hypotenuse_values[2] = round(math.sqrt(
            (cor + (-wheel_dict['RLW'][0])) * (cor + (-wheel_dict['RLW'][0])) + wheel_dict['RLW'][1] *
            wheel_dict['RLW'][1]), 3)

        hypotenuse_values[3] = round(math.sqrt(
            (cor - wheel_dict['FRW'][0]) * (cor - wheel_dict['FRW'][0]) + wheel_dict['FRW'][1] * wheel_dict['FRW'][1]),
            3)

        hypotenuse_values[4] = round(math.sqrt(
            (cor - wheel_dict['MRW'][0]) * (cor - wheel_dict['MRW'][0]) + wheel_dict['MRW'][1] * wheel_dict['MRW'][1]),
            3)

        hypotenuse_values[5] = round(math.sqrt(
            (cor - wheel_dict['RRW'][0]) * (cor - wheel_dict['RRW'][0]) + wheel_dict['RRW'][1] * wheel_dict['RRW'][1]),
            3)

    else:
        # if direction is left
        # value order of steering_values list -> degree_FLW|degree_RLW|degree_FRW|degree_RRW
        steering_values[0] = round(math.degrees(math.atan(dim_front2mid_wheel / (cor - dim_frontwheel_base / 2))), 3)
        steering_values[1] = round(math.degrees(math.atan(dim_rear2mid_wheel / (cor - dim_rearwheel_base / 2))), 3)
        steering_values[2] = round(math.degrees(math.atan(dim_front2mid_wheel / (cor + dim_frontwheel_base / 2))), 3)
        steering_values[3] = round(math.degrees(math.atan(dim_rear2mid_wheel / (cor + dim_rearwheel_base / 2))), 3)

        # use "cor + wheel_dict element" why the value in the dict is negative if the center of rotation is negative
        # hypo_FLW|hypo_MLW|hypo_RLW|hypo_FRW|hypo_MRW|hypo_RRW
        hypotenuse_values[0] = round(math.sqrt(
            (cor + wheel_dict['FLW'][0]) * (cor + wheel_dict['FLW'][0]) + wheel_dict['FLW'][1] * wheel_dict['FLW'][1]),
            3)

        hypotenuse_values[1] = round(math.sqrt(
            (cor + wheel_dict['MLW'][0]) * (cor + wheel_dict['MLW'][0]) + wheel_dict['MLW'][1] * wheel_dict['MLW'][1]),
            3)

        hypotenuse_values[2] = round(math.sqrt(
            (cor + wheel_dict['RLW'][0]) * (cor + wheel_dict['RLW'][0]) + wheel_dict['RLW'][1] * wheel_dict['RLW'][1]),
            3)

        hypotenuse_values[3] = round(math.sqrt(
            (cor + wheel_dict['FRW'][0]) * (cor + wheel_dict['FRW'][0]) + wheel_dict['FRW'][1] * wheel_dict['FRW'][1]),
            3)

        hypotenuse_values[4] = round(math.sqrt(
            (cor + wheel_dict['MRW'][0]) * (cor + wheel_dict['MRW'][0]) + wheel_dict['MRW'][1] * wheel_dict['MRW'][1]),
            3)

        hypotenuse_values[5] = round(math.sqrt(
            (cor + wheel_dict['RRW'][0]) * (cor + wheel_dict['RRW'][0]) + wheel_dict['RRW'][1] * wheel_dict['RRW'][1]),
            3)

    # based on the formular = hypotenuse value / max. hypotenuse value * speed
    # we define the speed in percentage of the speed from the user input
    # find max value of hypotenuse
    max_hypotenuse = 0.0
    for i in hypotenuse_values:
        if i < 0:
            i = -i
        if i > max_hypotenuse:
            max_hypotenuse = i

    # motor_speed value order -> speed_FLW|speed_MLW|speed_RLW|speed_FRW|speed_MRW|speed_RRW
    for i in range(len(hypotenuse_values)):  # fill the motor speed
        motor_speed[i] = round(hypotenuse_values[i] / max_hypotenuse * speed, 2)

    # rover_Drive dict has the following form
    # rover_Drive{name_of_the_wheel:steering_value, motor_speed}
    # motor_speed value order -> speed_FLW|speed_MLW|speed_RLW|speed_FRW|speed_MRW|speed_RRW
    # value order of steering_values list -> degree_FLW|degree-_MLW=0|degree_RLW|degree_FRW|degree-_MRW=0|degree_RRW
    rover_Drive['FLW'] = steering_values[0], motor_speed[0]
    rover_Drive['MLW'] = 0, motor_speed[1]
    rover_Drive['RLW'] = steering_values[1], motor_speed[2]
    rover_Drive['FRW'] = steering_values[2], motor_speed[3]
    rover_Drive['MRW'] = 0, motor_speed[4]
    rover_Drive['RRW'] = steering_values[3], motor_speed[5]

    return 0


# __________________________

def set_pwm_values_at_bbb(dist_to_travel, speed):
    """
    set_pwm_values_at_bbb ->
    set up the PWM values for steering and motor speed for each wheel direct at BBB
    the values are stored in the dictionary -> rover_Drive{}
    the function call the Adafruit_BBIO classes and there methods
    : param dist_to_travel -> int value in mm length
    : param speed -> int value in %
    :return: none
    """
    # calculate the BBB conform steering and motor drive values

    # definition section
    # if forward=1 backward=0 will realize over a dual pole switch IC hardware side has a pull up!
    forward_backward_switch = 'P9_12'
    GPIO.setup(forward_backward_switch, GPIO.OUT)

    # define the pins for the steering servos
    steer_flw = "P9_22"  # set the PWM pin for steering servo of FLW
    steer_rlw = "P9_21"  # set the PWM pin for steering servo of RLW
    steer_frw = "P9_14"  # set the PWM pin for steering servo of FRW
    steer_rrw = "P9_16"  # set the PWM pin for steering servo of RRW

    # define BBB IO pins for the motor drive PWM
    # check is ECAP PWM pins are avalible
    drive_owl = "P8_13"  # set the PWM pin for drive the outer wheels left side!!! only if the dimension front and rear equal!!!
    # drive_mwl = 'P9_42'  # set the PWM pin for drive the mid wheel left side
    drive_owr = "P8_19"  # set the PWM pin for drive the outer wheels right side!!! only if the dimension front and rear equal!!!
    # drive_mwr = 'P9_28'  # set the PWM pin for drive the mid wheel right side

    # min and max values for the servo's
    duty_min = 2  # set the min PWM percent -> value come from manual tests of the servos
    duty_max = 13  # set the max PWM percent-> value come from manual tests of the servos
    duty_span = duty_max - duty_min

    # initial setup and start the PWM instance ->
    # set all steering servos to the 90° neutral position -> must be found by manual tests
    # Adafruit_BBIO.PWM has the following arguments: 1 arg=PWM pin, 2arg=duty-cycle, 3arg=frequency
    # Adafriut BBIO.PMW need percentage value for duty cycle!!!!

    # calculate the duty cycle for the servos
    # definition: 0°=1ms -> duty_min  180°=2ms -> duty_max
    # move the servo to the center or neutral postion: 90°=1.5ms -> duty_span/2

    # set all steering servos to neutral (90°) position
    scv_flw = round((90 * (duty_max - duty_min) / (180 + duty_min) + offset_steering[0]), 2)
    scv_rlw = round((90 * (duty_max - duty_min) / (180 + duty_min) + offset_steering[1]), 2)
    scv_frw = round((90 * (duty_max - duty_min) / (180 + duty_min) + offset_steering[2]), 2)
    scv_rrw = round((90 * (duty_max - duty_min) / (180 + duty_min) + offset_steering[3]), 2)

    # initialize the servos to the neutral position
    PWM.start(steer_flw, scv_flw, 50)
    PWM.start(steer_rlw, scv_rlw, 50)
    PWM.start(steer_frw, scv_frw, 50)
    PWM.start(steer_rrw, scv_rrw, 50)

    # set the drive speed to zero for outer and mid wheels
    PWM.start(drive_owl, 0, 200)
    # PWM.start(drive_mwl, 0, 200)
    PWM.start(drive_owr, 0, 200)
    # PWM.start(drive_mwr, 0, 200)

    # start of steering duty cycle calculation of BBB PWM

    # 0°=1ms -> duty_min  180°=2ms -> duty_max based on 90°=1.5ms -> duty_span/2
    # example: steering value is 52.3° right then we must add 90° + 52.3° to find the steering angle = 142.3°
    # that's equal to steering_duty_cycle (in %)= (((142.3° - 0°) * duty_span) / (steer_max - steer_min)) + duty_min
    # formular for all steering servos -> =round(((steer_value + 90° - steer_min) * (duty_max-duty_min)) / (steer_max-steer_min) + duty_min,3)
    # TODO check how the build in position change the rotation direction -> try this on 2 servos for front and back

    if rover_Drive['steering_direction'] == 'right':
        steering_fl_dc = round(
            ((90 + rover_Drive['FLW'][0] - 0) * (duty_max - duty_min)) / (180 + duty_min) + offset_steering[0], 2)
        steering_rl_dc = round(
            ((90 - rover_Drive['RLW'][0] - 0) * (duty_max - duty_min)) / (180 + duty_min) + offset_steering[1], 2)
        steering_fr_dc = round(
            ((90 + rover_Drive['FRW'][0] - 0) * (duty_max - duty_min)) / (180 + duty_min) + offset_steering[2], 2)
        steering_rr_dc = round(
            ((90 - rover_Drive['RRW'][0] - 0) * (duty_max - duty_min)) / (180 + duty_min) + offset_steering[3], 2)

    else:
        steering_fl_dc = round(
            ((90 - rover_Drive['FLW'][0] - 0) * (duty_max - duty_min)) / (180 + duty_min) + offset_steering[0], 2)
        steering_rl_dc = round(
            ((90 + rover_Drive['RLW'][0] - 0) * (duty_max - duty_min)) / (180 + duty_min) + offset_steering[1], 2)
        steering_fr_dc = round(
            ((90 - rover_Drive['FRW'][0] - 0) * (duty_max - duty_min)) / (180 + duty_min) + offset_steering[2], 2)
        steering_rr_dc = round(
            ((90 + rover_Drive['RRW'][0] - 0) * (duty_max - duty_min)) / (180 + duty_min) + offset_steering[3], 2)

    PWM.set_duty_cycle(steer_flw, steering_fl_dc)
    PWM.set_duty_cycle(steer_rlw, steering_rl_dc)
    PWM.set_duty_cycle(steer_frw, steering_fr_dc)
    PWM.set_duty_cycle(steer_rrw, steering_rr_dc)
    # end of the steering section of BBB PWM

    # wait until the steering servos are in the right position
    time.sleep(1)

    # start of drive section of BBB PWM
    if rover_Drive['drive_direction'] == 'forward':

        GPIO.output(forward_backward_switch, GPIO.HIGH)  # set forward/backward switch to forward
        print(rover_Drive['drive_direction'])


    else:

        GPIO.output(forward_backward_switch, GPIO.LOW)  # set forward/backward switch to backward
        print(rover_Drive['drive_direction'])

    PWM.set_duty_cycle(drive_owl, rover_Drive['FLW'][1])
    # PWM.set_duty_cycle(drive_mwl, rover_Drive['MLW'][1])
    PWM.set_duty_cycle(drive_owr, rover_Drive['FRW'][1])
    # PWM.set_duty_cycle(drive_mwr, rover_Drive['MRW'][1])

    # TODO calculate the distance to time until the encoder section for the midwheels are not implemented in hardware
    # times must be set to the appropriate value on the hardware base
    # take the wheel diameter multiply with PI to get the circumstance and
    # divide then the distance that will be hand over as parameter -> dist_to_travel
    wheel_cir = math.pi * wheel_diameter
    # wheel_rotations = dist_to_travel / wheel_cir
    run_time = wheel_cir / speed
    time.sleep(run_time)

    # set the servos to the neutral position
    PWM.set_duty_cycle(steer_flw, scv_flw)
    PWM.set_duty_cycle(steer_rlw, scv_rlw)
    PWM.set_duty_cycle(steer_frw, scv_frw)
    PWM.set_duty_cycle(steer_rrw, scv_rrw)

    # wait for set the steering to neutral positon
    time.sleep(1)

    # end of the drive section of BBB PWM
    PWM.stop(steer_flw)
    PWM.stop(steer_rlw)
    PWM.stop(steer_frw)
    PWM.stop(steer_rrw)
    PWM.stop(drive_owl)
    # PWM.stop(drive_mwl)
    PWM.stop(drive_owr)
    # PWM.stop(drive_mwr)
    PWM.cleanup()
    GPIO.cleanup()

    # return to main
    return 0


# __________________________

def ackermann_steering(inp_tuple):
    """
    ackerman_steering -> set the direction of steering for each wheel
    also limits the max value of steering to +-30 degree
    motor speed is also handled and calculated max is 100%
    calculate the virtual center of rotation of the rover
    (variable later use as cor)
    :param degree: int value, negative value= left, positive value= right,
    limiter built in to -30 to +30
    :param speed:  int value, negative values means backward drive,
    positive values means forward drive, limiter built in to -100 to +100
    :param distance:  int value of mm to travel
    :return: none
    """
    # some init
    degree, speed, dist_to_travel = inp_tuple
    # value check and set max of degrees incl at 0 degree to add 0.001 degree
    if degree == 0:
        degree = 0.01  # needed to not have a div by zero
    if degree < -30:
        degree = -30
    if degree > 30:
        degree = 30
    if speed < -100:
        speed = -100
    if speed > 100:
        speed = 100
    cor = 0
    if degree < 0:
        rover_Drive['steering_direction'] = 'left'
    else:
        rover_Drive['steering_direction'] = 'right'

    if speed < 0:
        rover_Drive['drive_direction'] = 'backward'
    else:
        rover_Drive['drive_direction'] = 'forward'

    # take the dim_front2mid_wheel divided by tangent of degree (in grad)
    # then you get the cor
    # math.tan() want's radians as input!!!
    radiant_value = round(math.radians(degree), 4)
    # get the center of rotation
    cor = round(dim_front2mid_wheel / math.tan(radiant_value), 4)
    rover_Drive['cor'] = cor
    # read direction and set the steering left or right
    if rover_Drive['steering_direction'] == 'left':
        cor = -cor

    # calculate then the inner and outer steering angle with the following formular
    # function call for calculation of the steering values and
    # the motor speed for each motor
    # calculate the steering and motor speed values
    cal_steering_and_speed(speed, cor)
    # set up the PWM values in BBB
    set_pwm_values_at_bbb(dist_to_travel, speed)


# __________________________


# funktion call's as main
# test list for steering angles
# steering_values=[0, 10, -10, 25, -25, 30,-30, 45,-45]

# test loop for repeated angle steerings
# for i in steering_values:
ackermann_steering((10, -25, 200))  # eg.  +/-=indicate left or right, 15 = 15 degree, 100 = speed in duty cycle percent, 200=distance in mm


