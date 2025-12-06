

import cv2
import numpy as np
import time
import winsound  # For danger beep sound (Windows only)


# -----------------------------
# 1. Improved Skin Mask
# -----------------------------
def create_skin_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 40, 60], dtype=np.uint8)
    upper_skin = np.array([25, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    return mask


# -----------------------------
# 2. Contour detection
# -----------------------------
def find_hand_contour(mask, min_area=5000):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)

    if cv2.contourArea(largest) < min_area:
        return None

    return largest


# -----------------------------
# 3. Center of contour
# -----------------------------
def get_contour_center(contour):
    M = cv2.moments(contour)
    if M["m00"] == 0:
        return None

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy)


# -----------------------------
# 4. State classification
# -----------------------------
def classify_state(distance):
    if distance is None:
        return "NO HAND", (200, 200, 200)

    if distance > 150:
        return "SAFE", (0, 255, 0)
    elif distance > 60:
        return "WARNING", (0, 255, 255)
    else:
        return "DANGER", (0, 0, 255)


# -----------------------------
# 5. Main Loop
# -----------------------------
def main():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    frame_height, frame_width = frame.shape[:2]

    virtual_line_x = int(frame_width * 0.7)

    prev_time = time.time()
    last_beep_time = 0  # To avoid continuous beeping

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        mask = create_skin_mask(frame)
        hand_contour = find_hand_contour(mask)

        hand_center = None
        distance_to_boundary = None

        if hand_contour is not None:
            cv2.drawContours(frame, [hand_contour], -1, (255, 0, 0), 2)

            hull = cv2.convexHull(hand_contour)
            cv2.drawContours(frame, [hull], -1, (255, 255, 0), 2)

            hand_center = get_contour_center(hand_contour)

            if hand_center:
                cx, cy = hand_center
                cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)

                if cx <= virtual_line_x:
                    distance_to_boundary = virtual_line_x - cx
                else:
                    distance_to_boundary = 0

        # Draw virtual line
        cv2.line(frame, (virtual_line_x, 0), (virtual_line_x, frame_height), (255, 255, 255), 2)

        # Evaluate state
        state, color = classify_state(distance_to_boundary)

        # Draw state box
        cv2.rectangle(frame, (10, 10), (260, 60), (0, 0, 0), -1)
        cv2.putText(frame, f"State: {state}", (20, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Distance display
        if distance_to_boundary is not None:
            cv2.putText(frame, f"Distance: {int(distance_to_boundary)} px", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        # -------------- DANGER FEATURES -----------------
        if state == "DANGER":

            # 1️⃣ PLAY DANGER BEEP SOUND (every 0.5 seconds)
            if time.time() - last_beep_time > 0.5:
                winsound.Beep(1200, 200)  # (frequency, duration)
                last_beep_time = time.time()

            # 2️⃣ SHOW A DANGER SYMBOL TRIANGLE
            pts = np.array([[frame_width*0.5, frame_height*0.25],
                            [frame_width*0.45, frame_height*0.35],
                            [frame_width*0.55, frame_height*0.35]], np.int32)
            cv2.fillPoly(frame, [pts.astype(np.int32)], (0, 0, 255))

            cv2.putText(frame, "DANGER DANGER", (int(frame_width * 0.25), int(frame_height * 0.55)),
                        cv2.FONT_HERSHEY_DUPLEX, 1.4, (0, 0, 255), 3)
        # -------------------------------------------------

        # FPS counter
        current_time = time.time()
        fps = 1.0 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(frame, f"FPS: {fps:.1f}", (frame_width - 140, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Hand Tracking - Danger Sound + Symbol", frame)
        cv2.imshow("Skin Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
