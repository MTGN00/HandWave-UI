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

import pyautogui
import mediapipe as mp
import cv2
import time
import math

# Mediapipe'yi başlat
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Ekran boyutlarını al
screen_width, screen_height = pyautogui.size()

# Hassasiyet parametresi
sensitivity = 3.0  # Fare hareketi hassasiyeti

# Tıklama eşiği (baş parmağın kapanması)
click_threshold = 0.07  # 30 cm uzaklık için optimize edildi

# Webcam aç
cap = cv2.VideoCapture(0)

# Son tıklama zamanı
last_click_time = 0
click_interval = 0.25  # Çift tıklama aralığı (saniye)

# PyAutoGUI'nin fail-safe özelliğini devre dışı bırakma
pyautogui.FAILSAFE = False

# Kamera penceresini ekrana ortalama
cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
cv2.moveWindow("Hand Tracking", (screen_width // 2) - 320, (screen_height // 2) - 240)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    # Kameradan alınan görüntüyü BGR -> RGB'ye dönüştür
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Mediapipe ile el algılama
    results = hands.process(frame_rgb)
    
    # El algılandığında fareyi hareket ettir
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # İşaret parmağın ikinci ekleminin koordinatlarını al (PIP)
            index_finger_pip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]  # Baş parmağın orta eklemi

            # İşaret parmağının PIP noktasının ekrandaki konumunu hesapla
            cursor_x = screen_width - int(index_finger_pip.x * screen_width)
            cursor_y = int(index_finger_pip.y * screen_height)

            # Fare imlecini işaret parmağının PIP noktasına taşı
            pyautogui.moveTo(cursor_x, cursor_y)

            # Baş parmak kapanma kontrolü: Thumb Tip ile Thumb IP arasındaki mesafe
            thumb_closure_distance = math.sqrt(
                (thumb_tip.x - thumb_ip.x) ** 2 +
                (thumb_tip.y - thumb_ip.y) ** 2
            )

            # Tıklama: Baş parmağın kapanması (mesafe click_threshold'un altındaysa)
            if thumb_closure_distance < click_threshold:
                current_time = time.time()
                if current_time - last_click_time < click_interval:
                    pyautogui.doubleClick()  # Çift tıklama
                else:
                    pyautogui.click()  # Tek tıklama
                last_click_time = current_time

            # Elin üzerinde bağlantıları çiz
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Kameradaki görüntüyü göster
    cv2.imshow("Hand Tracking", frame)
    
    # 'q' tuşuna basarak çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()