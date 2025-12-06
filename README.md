
# 🖐️ Hand Tracking Safety Boundary Detection (SAFE / WARNING / DANGER)

A real-time computer vision prototype that detects a user's hand using **classical computer vision techniques** (WITHOUT MediaPipe or OpenPose) and triggers alerts when the hand approaches or crosses a **virtual safety boundary**.

This project was developed as part of the **Arvyax Internship Assignment**.

---

## 🚀 Features

### 🔍 **1. Real-time Hand Tracking (No MediaPipe/OpenPose)**

Uses only:

* HSV skin segmentation
* Contours
* Convex Hull
* Centroid detection

### 🎯 **2. Virtual Safety Boundary**

A vertical line drawn on the screen.
The system monitors how close the hand is to this boundary.

### ⚠️ **3. Distance-based Interaction States**

| State       | Condition                     | UI Feedback                          | Sound |
| ----------- | ----------------------------- | ------------------------------------ | ----- |
| **SAFE**    | Hand far from boundary        | Green label                          | ❌ No  |
| **WARNING** | Hand approaching boundary     | Yellow label                         | ❌ No  |
| **DANGER**  | Hand touches/crosses boundary | Red label + Triangle + “DANGER” text | ✅ Yes |

### 🔔 **4. Danger Sound Alert**

A high-frequency beep plays repeatedly when hand enters **DANGER** zone.

### 🛑 **5. Danger Symbol (Red Triangle)**

A visual warning symbol appears during danger state for stronger feedback.

### 📈 **6. Real-time FPS Display**

Runs smoothly at **15–30 FPS** on CPU.

---

## 🧠 Why This Project Matters

This project demonstrates key CV engineering skills:

* Real-time tracking without heavy ML libraries
* Safety interaction systems
* Classical vision processing (HSV, contours, hull)
* Dynamic distance-based logic
* Clean UI feedback + sound warnings
* Efficient CPU-only execution

Designed exactly to satisfy Arvyax’s assignment constraints.

---

## 📂 Project Structure

```
hand_boundary_poc/
│── main.py
│── requirements.txt
│── README.md
│── .gitignore

```

---

## 🛠 Technologies Used

* Python
* OpenCV
* NumPy
* winsound (for DANGER alert)

---

## ▶️ How to Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run main script

```bash
python main.py
```

### 3. Quit anytime

```
Press 'q'
```

---

## 📏 Interaction Logic (How It Works)

### Step-by-step Processing Pipeline

```
Camera Frame → Skin Mask → Morphology → Contour → Convex Hull → 
Hand Center → Distance to Boundary → State Classification → UI + Sound Alerts
```

### Distance Calculation

```text
distance = boundary_x - hand_center_x
```

---

## 🖼️ Visual Output Includes:

* Hand contour (blue)
* Convex hull (yellow)
* Hand center marker (red dot)
* Virtual boundary line (white)
* State label (top-left)
* FPS counter (top-right)
* DANGER triangle + sound warning

---

## 🔧 Possible Improvements

These features can be added later:

* Adjustable boundary sensitivity (trackbar)
* Fingertip detection using convexity defects
* Virtual object interaction (grab/push gestures)
* Background subtraction for robustness
* Voice alert instead of beep
* Multi-hand support

---

## 📜 Assignment Compliance

This project **fully adheres** to all Arvyax constraints:

✔ Classical CV only (no MediaPipe, no OpenPose, no cloud APIs)
✔ Real-time hand detection
✔ Virtual object present
✔ Dynamic SAFE/WARNING/DANGER thresholds
✔ Clear alert when boundary is crossed
✔ CPU-only execution ≥ 8 FPS
✔ Visual + audio feedback

---

## 👤 Developer

**Vishal Verma**
B.Tech CSE (AI) | Developer | CV & AI enthusiast
GitHub: *[https://github.com/Vishal-Verma71](https://github.com/Vishal-Verma71)*
Email: *vermavishal958784@gmail.com*


