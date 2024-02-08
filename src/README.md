# Test folder contains Python files for test the for Ackermann steering drive on BBB

## Development of a drive class to use later on Leraso-Rover1

Task:

- [x] setup all dimensions of the wheels, steering offsets,
- [x] define a dictionary for the wheels -> wheel_dict{} 
- [x] define the ackermann steering function to calculate the center of rotation -> ackermann_steering()
- [x] define a function that calculate the steering of each wheel -> cal_steering_and_speed()
- [x] define a funktion that use the Adafruit_BBIO.PWM class to move the servos and drives -> set_pwm_values_at_bbb()
- [x] cal_steering_and_speed() -> calculate the hypotenuse lines from center of rotation to the wheels center dots to calculate the steering angle
- [x] cal_steering_and_speed() -> use the calculate hypotenuse lines to recalculate the speed of each wheel
- [x] set_pwm_values_at_bbb() -> use the content of the rover_drive{} dict to set the duty cycle for the PWM
- [ ] TODO define a function for calculate the traveled distance to set a timer for the given duty cycle (25% dc = x seconds= x cm of driving) like that
- [ ] TODO implement a distance measurement module, when the rotary encoder are installed in hardware
- [ ] refactor the drive class as a proper Python module
- [ ] x
