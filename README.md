# Edge
EdgeQuiz

    

    Lab 1: Guide on how to configure the Raspberry Pi 400 with a Webcam 
Section 1: Raspberry Pi OS Installation & Initial Configuration 
MCQs 
    1. Which software tool is used to write the Raspberry Pi OS image to a microSD 
card? 
A. Etcher 
B. Raspberry Pi Imager 
C. Rufus 
D. Win32 Disk Imager 
Answer: B. Raspberry Pi Imager

3. When using Raspberry Pi Imager, which setting would you adjust to 
configure WiFi credentials before booting for the first time? 
A. Localisation settings 
B. OS Customisation settings 
C. Advanced display settings 
D. Timezone settings 
Answer: B. OS Customisation settings

Short Answer 
5. In the Raspberry Pi Imager’s advanced settings, name two items you can 
configure before flashing the microSD card. 
Answer: 
o Hostname of the Raspberry Pi 
o Username and password 
o WiFi credentials (SSID and password) 
o SSH enabling 
o Locale settings (timezone, keyboard layout) 

6. What is the command to update the list of available packages on a 
Raspberry Pi running Raspberry Pi OS? 
Answer: sudo apt update

8. What is the command to upgrade all currently installed packages on a 
Raspberry Pi? 
Answer: sudo apt upgrade

Section 2: Hardware Setup & Basic Configuration 
MCQs 

10. Which of the following components is not strictly required to get the 
Raspberry Pi 400 up and running with a webcam? 
A. MicroSD card with Raspberry Pi OS 
B. Power supply 
C. Ethernet cable 
D. USB webcam 
Answer: C. Ethernet cable (WiFi can be used instead.)

12. To enable VNC on a headless Raspberry Pi via SSH, which tool do you 
typically use? 
A. raspi-config 
B. config.txt 
C. sudo raspi-config 
D. /boot/cmdline.txt 
Answer: C. sudo raspi-config

Short Answer 
14. Which command would you run to edit the network configuration file 
(dhcpcd.conf) on Raspberry Pi OS? 
Answer: sudo nano /etc/dhcpcd.conf 

15. Explain why assigning a static IP to your Raspberry Pi can be useful in a lab 
environment. 
Answer: 
It ensures the Pi always has the same IP address, making it easier to connect 
via SSH or VNC without repeatedly looking up the IP.

Section 3: Using SSH and VNC 
MCQs 
17. Which of the following protocols is used by VNC to provide a graphical 
desktop over the network? 
A. RDP (Remote Desktop Protocol) 
B. RFB (Remote Framebuffer Protocol) 
C. SSH (Secure Shell) 
D. FTP (File Transfer Protocol) 
Answer: B. RFB (Remote Framebuffer Protocol) 

Short Answer 
18. What is the default port used by VNC on a Raspberry Pi? 
Answer: Port 5900 

19. State one way to find your Raspberry Pi’s IP address on a local network if you 
do not have direct access to its desktop. 
Answer: 
o Check the device list on your router or mobile hotspot 
o Use arp -a on your local machine 
o Use a network scanning tool (e.g., nmap)

Section 4: Webcam Setup & Testing 
MCQs 
21. Which command-line tool is typically used to capture a still image on the 
Raspberry Pi with a USB webcam? 
A. motion 
B. fswebcam 
C. raspistill 
D. gstreamer 
Answer: B. fswebcam 

22. What is the Linux subsystem or driver model used for webcams on 
Raspberry Pi OS? 
A. ALSA 
B. Video4Linux2 (v4l2) 
C. GStreamer 
D. MESA 
Answer: B. Video4Linux2 (v4l2)

Short Answer 
24. Write the exact command to capture a 1280×720 image named image.jpg 
using fswebcam without displaying the banner text. 
Answer: fswebcam -r 1280x720 --no-banner image.jpg 

25. Which command is used to list all USB devices connected to the Raspberry 
Pi? 
Answer: lsusb

Section 5: Audio Input & arecord 
MCQs 
27. Which command can be used to record audio on a Raspberry Pi from a 
recognized microphone? 
A. aplay 
B. ffmpeg 
C. arecord 
D. sox 
Answer: C. arecord 

28. If your webcam’s microphone is recognized as card 2, device 0, which of the 
following commands records a 10-second clip? 
A. arecord -D plughw:0,2 -d 10 test.wav 
B. arecord -D plughw:2,0 -d 10 test.wav 
C. arecord -D hw:2,0 -d 10 test.wav 
D. arecord -d 10 test.wav 
Answer: B. arecord -D plughw:2,0 -d 10 test.wav

Short Answer 
30. What is the command to play back the recorded audio file test.wav? 
Answer: aplay test.wav 

31. If you cannot hear any audio on playback, mention one troubleshooting step 
you might try. 
Answer: 
o Check alsamixer to ensure the volume isn’t muted 
o Ensure correct audio output (HDMI vs. headphone jack) 
o Verify the proper audio device is selected

Section 6: Video Recording with ffmpeg 
MCQs 
33. Which flag specifies the video input format when using ffmpeg on a 
Raspberry Pi with a USB webcam? 
A. -i 
B. -r 
C. -video_size 
D. -f 
Answer: D. -f 

34. In the command below, what does the -framerate 25 parameter control? 
f
 fmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 output.mp4 
A. The bitrate 
B. The resolution 
C. The capture frames per second 
D. The audio sampling rate 
Answer: C. The capture frames per second

Short Answer 
36. Write a sample ffmpeg command to record a 30-second video clip from 
/dev/video0 at 800×600 resolution into a file called myvideo.mp4. 
Answer: ffmpeg -f v4l2 -t 30 -video_size 800x600 -i /dev/video0 myvideo.mp4 

Section 7: Virtual Environments & Python 
MCQs 
37. Which command is used to create a Python virtual environment named 
myenv? 
A. python3 -m venv myenv 
B. virtualenv myenv 
C. mkvenv myenv 
D. pip install myenv 
Answer: A. python3 -m venv myenv 

38. After creating a virtual environment, which command do you use to activate 
it on a Raspberry Pi OS (bash shell)? 
A. enable myenv 
B. bash myenv 
C. source myenv/bin/activate 
D. activate myenv 
Answer: C. source myenv/bin/activate

Short Answer 
40. Why is it recommended to use a Python virtual environment when installing 
packages like opencv-python? 
Answer: 
It prevents version conflicts by isolating package installations from the 
system-wide Python packages, keeping your global environment clean. 

Section 8: Motion Detection & OpenCV Basics (Advanced/Optional) 
MCQs 
41. Which OpenCV function is commonly used to convert a frame to grayscale? 
A. cv2.absdiff 
B. cv2.cvtColor 
C. cv2.threshold 
D. cv2.findContours 
Answer: B. cv2.cvtColor 

42. In a simple motion detection script using OpenCV, which function is used to 
f
 ind the outlines of detected shapes or movements? 
A. cv2.GaussianBlur 
B. cv2.dilate 
C. cv2.absdiff 
D. cv2.findContours 
Answer: D. cv2.findContours

Short Answer 
44. Briefly explain what the following line of code does in a motion detection 
script: 
frame_delta = cv2.absdiff(gray1, gray2) 
Answer: 
It calculates the absolute difference between two grayscale frames, 
highlighting areas where changes (motion) occur. 

45. What is one practical use of a Python-based motion detection system on a 
Raspberry Pi? 
Answer: 
o Home security or surveillance 
o Wildlife monitoring 
o Triggering automated tasks when movement is detected

Section 9: General Troubleshooting & Best Practices 
MCQs 
47. If the webcam video is lagging or dropping frames, which of the following 
might improve performance? 
A. Increase resolution to 4K 
B. Lower the frame rate 
C. Use a lower resolution 
D. Switch to the composite video output 
Answer: C. Use a lower resolution 

Short Answer 
48. Name two commands or methods you can use to check the CPU and 
memory usage on your Raspberry Pi when troubleshooting performance 
issues. 
Answer: 
o top or htop 
o free -h 
o (vcgencmd measure_temp for temperature) 

49. Why might you need to install haveged on a headless Raspberry Pi when 
enabling VNC? 
Answer: 
It provides additional entropy for secure operations (including SSH/VNC) 
when there is little keyboard/mouse input, preventing entropy starvation.

Section 10: Additional Open-Ended/Discussion Questions 
1. Explain how to configure the Raspberry Pi 400 so that it automatically logs in 
upon boot and starts the desktop environment (useful for kiosk-like setups). 
Answer will vary. Consider using raspi-config or editing config files to auto
login.

3. Discuss how changing contour area thresholds in a motion detection script 
affects sensitivity and false positives. 
Answer will vary. Lower thresholds might detect very small movements or 
noise; higher thresholds ignore small changes but may miss subtle motion.

5. Propose a simple Python script flow that captures an image every 30 
seconds and uploads it to a cloud service. 
Answer will vary. A sample approach: use a loop with time.sleep(30), capture 
an image (e.g., with fswebcam or OpenCV), then upload via an API (AWS S3, 
Google Cloud, etc.).

Lab 1 In-Lab questions (Found in the Github) 
Section 5: Questions to think about 
1. Identify and explain the additional functionalities introduced in Code #2. How do 
these changes transform the program from a simple image capture to a 
movement detection system? 
2. Several new OpenCV functions are used (like cv2.absdiff, cv2.cvtColor, 
cv2.GaussianBlur, cv2.threshold, cv2.dilate, and cv2.findContours). Research 
each of these functions and understand their role in processing the video frames 
for movement detection. 
3. The program uses specific conditions (such as contour area) to decide when to 
draw rectangles and indicate movement. Experiment with these parameters to 
see how they affect the accuracy and sensitivity of movement detection. 
4. Loop Mechanics and Video Processing: Analyze the role of the while loop in the 
2nd Code for continuous video capture and processing. How does this looping 
mechanism differ from the single capture approach in the 1st Code, especially in 
terms of real-time processing and movement detection? 
5. Consider aspects like improving the accuracy of movement detection, 
optimizing performance, or adding new features (like recording video when 
movement is detected). 
1. What additional functionalities are introduced in Code #2 compared to Code #1? 
Answer: 
Code #1 simply captures a single image from the webcam and saves it to disk. 
In contrast, Code #2 introduces a continuous loop that captures and compares 
consecutive frames in real time. It detects movement by calculating differences 
between frames and highlights motion by drawing rectangles around moving objects 
and displaying a "Movement" status. This transforms the program from a basic image 
grabber into a real-time motion detection system. 
2. What does cv2.absdiff(frame1, frame2) do? 
Answer: 
This function calculates the absolute difference between two frames. 
It highlights the pixels that have changed between the frames—indicating possible 
movement. 
3. What does cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) do? 
Answer: 
It converts the difference image from color (BGR) to grayscale. 
This simplifies the data by reducing the number of channels, making further image 
processing faster and more efficient. 
4. Why is cv2.GaussianBlur() used in the motion detection process? 
Answer: 
cv2.GaussianBlur() applies a blur to the grayscale image to reduce noise and minor 
pixel fluctuations. 
This helps in avoiding false positives by smoothing out insignificant variations. 
5. What is the role of cv2.threshold() in detecting motion? 
Answer: 
cv2.threshold() converts the blurred image into a binary black-and-white image. 
Pixels brighter than a certain value become white (motion), and others become black 
(background), helping to isolate movement areas clearly. 
6. What does cv2.dilate() do in this context? 
Answer: 
It expands white regions in the binary image, helping to fill in gaps and make motion 
areas more solid. 
This improves contour detection by ensuring small holes or noise don’t break apart 
moving objects. 
7. What is the purpose of cv2.findContours() in Code #2? 
Answer: 
cv2.findContours() identifies the outlines of white regions (areas of motion) in the 
image. 
Each contour corresponds to a detected moving object. 
8. Why does the code check cv2.contourArea(contour) < 900? 
Answer: 
This condition filters out small contours, which are likely caused by noise or minor 
changes. 
Only contours larger than 900 pixels are considered significant enough to count as real 
movement. 
9. How does adjusting the contour area threshold affect the system? 
Answer: 
• A lower threshold increases sensitivity but may cause false alarms from small 
or irrelevant movement. 
• A higher threshold reduces false positives but might miss subtle motion. 
Tuning this value balances accuracy and sensitivity. 
10. How does the loop in Code #2 enable real-time processing? 
Answer: 
The while True: loop continuously captures and processes frames from the webcam. 
Each frame is compared to the previous one, and any detected motion is immediately 
displayed. This allows for live monitoring, unlike Code #1, which only takes one 
snapshot. 
11. How does Code #2 differ from Code #1 in terms of structure? 
Answer: 
• Code #1: Captures one image, saves it, and exits. 
• Code #2: Uses a loop to constantly read new frames, detect motion, and update 
the display, enabling ongoing surveillance. 
12. What are some ways to improve the motion detection system? 
Answer: 
• Accuracy Improvements: 
o Adjust blur kernel, threshold values, or contour area. 
o Use background subtraction or adaptive thresholding. 
• Performance Optimizations: 
o Lower frame resolution. 
o Use multi-threading or hardware acceleration. 
o Optimize frame rate or processing frequency. 
• New Features to Add: 
o Automatically record video when motion is detected. 
o Send alerts via email or app notifications. 
o Log timestamps and store data for reviewing past events. 
13. What is the overall impact of these changes in Code #2? 
Answer: 
Code #2 transforms the application from a simple image capture tool into a fully 
functional motion detection system. 
It enables real-time surveillance, processes video frames to detect changes, and 
provides the foundation for advanced features like automated recording and alerts. 
