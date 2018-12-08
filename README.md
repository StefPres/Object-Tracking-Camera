# Servo-Tracker-ArdPi
Two pieces of code, one for Arduino, one for Raspberry Pi Opencv, to create a camera that tracks and follows objects of green color

This repository also includes a diagram made using Fritzing

The object tracking camera takes inputs from a camera mounted on a set of servos. As of now, it is programmed to look for green/yellow objects, but this can be changed at will. Based on where the object is, the Raspberry Pi will send inputs to an Arduino which controls the servos and will adjust it to keep the object in frame.

The Python code is a modified version of code from the following website:
https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

Arduino code is custom
