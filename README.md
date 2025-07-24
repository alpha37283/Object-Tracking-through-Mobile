1. Camera Stream from Android to Laptop
Android phone sends camera frames via WebSocket to your laptop.

Laptop receives and decodes the JPEG frames correctly.

2. Object Detection on Laptop
Laptop uses YOLOv8 to detect objects on incoming frames.

Detections include class, confidence, and bounding boxes.

3. Drawing on Laptop Feed
Bounding boxes are correctly drawn and displayed on the laptop using OpenCV.

Debugging tools like cv2.imshow() are working.

4. Sending Detections to Android
After detection, bounding boxes are sent back to the Android phone via WebSocket as JSON.

5. Bounding Box Rescaling for Android
You've added a scale_bboxes_for_android() function to:

Scale the coordinates



# I am somewhat done with project leaving it in the middle 


