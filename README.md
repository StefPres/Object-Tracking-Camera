# Object-Tracking-Camera

The <code>Object-Tracking-Camera</code> takes inputs from a camera mounted on a set of servos and uses the information to position the camera so that 
the object it is tracking remains in the center of the frame. The servos are controlled by an Arduino microcontroller, which in turn 
receives inputs from a Raspberry Pi that processes the video feed from the camera. 

The Python code is a modified version of code from the following website:

https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

### Fritzing Schematic
![alt text](https://raw.githubusercontent.com/StefPres/Object-Tracking-Camera/master/Images/Ard_Rasp_Camera_bb.png)

### Overview of object detection algorithm :
1. Camera sends image to computer (Raspberry Pi)
2. Computer analyzes image. Looks for objects of specific size, color, appearance, etc
3. If desired object is detected, Computer sends output (Message to Arduino)
4. Arduino moves servos based on message received
5. Repeat sequence from Step 1

### Overview of Raspberry Pi code:
1. Computer loads in a single frame from camera video feed
2. Frame is blurred using a Gaussian Blur filter to remove noise <code>cv2.GaussianBlur</code>
3. Computer scans all pixels in blurred frame <code>cv2.inRange</code>. All pixels outside of desired color range are set to black, 
while those within the color range are set to white.
4. Image is eroded <code>cv2.erode</code> to further remove noise
5. Image is dilated <code>cv2.dialate</code> to reset object to original size
6. Find object contours <code>cv2.findContours</code> to determine if there are any objects in color range
7. If object found, determine where it is in the frame by looking at where its center is
8. Based on where center is, update servo position variables.
9. Send updated servo positions to arduino over the USB serial connection (arduino.write)
10. Arduino sets servo position based on the received position message
11. Next frame is loaded and process repeats

### Overview of Arduino code:
1. Import Servo library
2. Initialize servos to set position (center horizontal, 25 degrees down)
3. Loop:
a. Read message from Raspberry Pi using Serial Monitor
b. Set new servo position based on message

### Argparse Arguments:

  *-x Horizontal Screen Size (default 480px) 
  *-y Vertical Screen Size (default 360px) 
  *-s Minimum Object Size (default 10px)
  *-f Camera Framerate (default 32 frames/sec)
  
These arguments can be applied when the software is run to change the parameters that the
software uses to detect objects.
The two screen size arguments (-x, -y) adjust the size of the screen in pixels. Smaller screen
sizes run faster but have less precision in detecting objects. I found that resolutions above
640x480 slowed down the object detection considerably and thus were not useful for this
application
The object size argument (-s) sets the smallest possible radius in pixels an object needs to be
before it will be detected. Smaller sizes are more likely to detect objects but are also more likely
to detect background clutter as objects and thus introduce more noise.
The camera framerate argument (-f) sets how fast the camera sends images to the computer in
frames per second. Higher framerates lead to greater responsiveness but take up more
computer resources. Above a certain framerate (in the case of the pi, 32), the increased
resource usage overtakes the faster image loading speed, negating its benefits

### Results and Conclusion:
Under optimum conditions (even lighting, clean background), the camera had no issue tracking
the objects. But under less-than-optimal conditions (uneven, excessively bright, or low lighting),
the camera would sometimes not detect the object, even when the object in question was only a
foot in front of it.
Color based object tracking works best in a controlled environment simply due to the number of
things that can affect the color that the camera “sees”. A situation where this would work well is
in a factory. In a factory, you can control lighting, the size of the objects you are trying to
monitor, and the placement of the camera. A camera could be placed above a conveyor belt to
monitor the size and/or color of different objects passing under it, and count/sort the objects.
Given enough computing power, color-based object tracking could work in even the most
uncontrolled environments with the computers being able to clean up any clutter that shows up,
but since a lot of applications limit the size, and by extension the power, of a computer,
color-based object tracking is not practical for applications in uncontrolled environments such as
outdoors or in a cluttered environment.
