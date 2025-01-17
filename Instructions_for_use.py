"""
Hand Tracking Mouse Control Script
==================================
This Python script uses MediaPipe and PyAutoGUI libraries to enable mouse control through hand gestures. 
The script allows the user to move the mouse pointer and perform click actions based on hand movements 
and gestures captured via a webcam.

Features:
---------
1. **Mouse Pointer Control**:
   - The mouse pointer follows the position of the **second joint (PIP)** of the index finger.
   - Movements are sensitive and optimized for a distance of approximately 30 cm from the camera.

2. **Click Actions**:
   - **Single Click**: Performed when the thumb is closed towards the palm (measured as the distance between 
     the tip and the middle joint of the thumb falling below a certain threshold).
   - **Double Click**: Automatically triggered when consecutive thumb closures occur within a defined time interval.

3. **Enhanced Usability**:
   - The script is designed to work within the visible screen area and avoids mouse pointer movement beyond 
     screen boundaries.
   - Sensitivity can be adjusted for smoother or more precise movements.

4. **Visual Feedback**:
   - The script provides a live video feed showing hand tracking landmarks and connections for better feedback.

Usage Instructions:
--------------------
1. **Environment Setup**:
   - Install the required libraries using pip:
     ```
     pip install opencv-python mediapipe pyautogui
     ```

2. **Starting the Script**:
   - Run the script using Python. A window titled "Hand Tracking" will open in the center of the screen.

3. **Hand Position**:
   - Place your hand approximately 30 cm from the webcam.
   - Use the "thumbs-up" gesture as the neutral position for optimal performance:
       👍 (Thumb extended, index finger pointing upwards)

4. **Mouse Movement**:
   - Move your **index finger's second joint (PIP)** to control the mouse pointer.

5. **Click Actions**:
   - Close your thumb towards your palm to perform a single or double click. The threshold for recognition is 
     preconfigured.

6. **Stopping the Script**:
   - Press the 'q' key to exit the program.

Technical Details:
-------------------
- **Libraries Used**:
  - `mediapipe`: For hand tracking and gesture detection.
  - `pyautogui`: For controlling mouse movements and clicks.
  - `cv2`: For capturing video feed and rendering visuals.
  
- **Screen Size Detection**:
  - The script dynamically adapts to the screen resolution to map hand positions to mouse coordinates.

- **Click Threshold**:
  - Configured for a 30 cm distance from the webcam, with a threshold of `0.07` for thumb closure detection.

- **Sensitivity**:
  - Mouse pointer movements are scaled using a sensitivity factor (`3.0` by default), which can be adjusted 
    based on user preference.

"""