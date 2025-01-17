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
