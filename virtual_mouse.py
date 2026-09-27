import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from collections import deque

screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
cam_w = int(cap.get(3))
cam_h = int(cap.get(4))

frame_reduction = 100
x_min = frame_reduction
x_max = cam_w - frame_reduction
y_min = frame_reduction
y_max = cam_h - frame_reduction

CLICK_THRESHOLD = 40
click_cooldown = 0.3
last_click_time = 0
prev_time = 0

# Cursor smoothing buffer
smooth_buffer = deque(maxlen=5)

def distance(p1, p2):
    return np.hypot(p1[0] - p2[0], p1[1] - p2[1])

def fingers_up(lm):
    """Return [thumb, index, middle, ring, pinky] - 1 if up"""
    fingers = []
    # Thumb
    if lm[4].x < lm[3].x:
        fingers.append(1)
    else:
        fingers.append(0)
    # 4 fingers
    for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
        if lm[tip].y < lm[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark
            fingers = fingers_up(lm)

            # Index finger tip
            index = lm[8]
            cx = int(index.x * cam_w)
            cy = int(index.y * cam_h)

            # Thumb tip
            thumb = lm[4]
            tx = int(thumb.x * cam_w)
            ty = int(thumb.y * cam_h)

            # ============ SCROLL MODE ============
            # Index + Middle up, Ring + Pinky down
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                cv2.putText(frame, "SCROLL MODE", (50, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                # Middle finger tip ki Y position
                mid_y = int(lm[12].y * cam_h)
                if mid_y < cam_h // 2:
                    pyautogui.scroll(50)
                    cv2.putText(frame, "SCROLL UP", (50, 130),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    pyautogui.scroll(-50)
                    cv2.putText(frame, "SCROLL DOWN", (50, 130),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 15, (0, 255, 255), -1)
                continue

            # ============ CURSOR MOVE MODE ============
            if x_min < cx < x_max and y_min < cy < y_max:
                screen_x = np.interp(cx, (x_min, x_max), (0, screen_w))
                screen_y = np.interp(cy, (y_min, y_max), (0, screen_h))

                # Smoothing
                smooth_buffer.append((screen_x, screen_y))
                avg_x = int(sum(p[0] for p in smooth_buffer) / len(smooth_buffer))
                avg_y = int(sum(p[1] for p in smooth_buffer) / len(smooth_buffer))
                pyautogui.moveTo(avg_x, avg_y)

            # ============ CLICK DETECTION ============
            dist = distance((cx, cy), (tx, ty))
            current_time = time.time()

            if dist < CLICK_THRESHOLD:
                if current_time - last_click_time > click_cooldown:
                    cv2.circle(frame, (cx, cy), 20, (0, 0, 255), -1)
                    pyautogui.click()
                    last_click_time = current_time
                    cv2.putText(frame, "CLICK!", (50, 180),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

            cv2.putText(frame, f"Dist: {int(dist)}", (50, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {int(fps)}", (cam_w - 150, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()