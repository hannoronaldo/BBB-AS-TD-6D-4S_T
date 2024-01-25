# BBB-AS-TD-6D-4S_T
Python implementation of a rover drive chain with 6 drives and 4 steering wheels on a Beagle Bone Black platform


### BBB = BeagleBoneBlack   AS = AckermanSteering TD = TestDrive 6D = 6 drive motors 6S = 4 steering servos


first implementation of the ackerman steering on the BeagleBone black
-------------------------------------------------------------------------
This repo is for the first implementation of a drive base for a Buggy Rocker vehicle.

![Setup of the wheel for the Boggy Rocker vehicle](/description/IMG/setup_AS-boggy-rocker.png)

The Ackermann steering method is used to avoid push or drag wheels in curve drive.

![Concept of Ackerman Steering](/description/IMG/prinzip_of_steering_calculation.png)

There are 6 drive motors and 4 steering servo motors involved.
On each side we have a front wheel with a steering servo, a mid wheel and a back wheel also with a steering servo.
The drive motor get a dedicated speed depended from the steering angle. 

![Calculation of the Steering values](/description/IMG/calculation_of_steering_and_speed.png)

The drive motor speed is also depended from the steering angle and the position of the motor in the chassis.
This is the function call structure:

![Function call structure](/description/IMG/function_calls.png)
