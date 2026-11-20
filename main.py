
from ursina import *
import cv2
import mediapipe as mp
import math
import time as pytime

# ========== APP ==========
app = Ursina()
window.title = "ASHA AI - MOTION MIND"
window.color = color.black
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False

camera.position = (0, 0, -13)
camera.fov = 65

# ========== HEADER ==========
Text(
    "ASHA AI",
    origin=(0, 0),
    position=(0, 0.43),
    scale=2.5,
    color=color.yellow
)

Text(
    "MOTION MIND | SOLAR EXPLORER",
    origin=(0, 0),
    position=(0, 0.31),
    scale=0.9,
    color=color.azure
)

# ========== SUN ==========
center = (0, -0.25, 0)

sun = Entity(
    model="sphere",
    color=color.orange,
    scale=1.35,
    position=center
)

# Sun outer glow layers
Entity(
    model="sphere",
    color=color.rgba(255, 130, 0, 35),
    scale=1.55,
    position=center
)

# ========== ORBIT RINGS ==========
orbit_data = [
    (1.65, color.yellow),
    (2.25, color.orange),
    (2.85, color.rgb(180, 100, 40)),
    (3.45, color.azure)
]

for radius, shade in orbit_data:
    Entity(
        model="sphere",
        color=shade,
        scale=(radius * 2, radius * 2, 0.015),
        position=center,
        wireframe=True
    )

# ========== PLANETS ==========
planet_data = [
    (1.65, 0.18, color.azure, 1.0),
    (2.25, 0.24, color.orange, 0.75),
    (2.85, 0.20, color.rgb(180, 130, 80), 0.55),
    (3.45, 0.30, color.cyan, 0.4)
]

planets = []

for radius, size, shade, speed in planet_data:
    planet = Entity(
        model="sphere",
        color=shade,
        scale=size,
        position=(radius, center[1], 0)
    )

    planets.append({
        "entity": planet,
        "radius": radius,
        "angle": 0,
        "speed": speed
    })

# ========== STATUS PANEL ==========
Text(
    "SYSTEM MONITOR",
    position=(-0.84, -0.28),
    scale=1,
    color=color.yellow
)

gesture_text = Text(
    "GESTURE: WAITING",
    position=(-0.84, -0.35),
    scale=0.85,
    color=color.azure
)

status_text = Text(
    "SYSTEM: STARTING",
    position=(-0.84, -0.41),
    scale=0.85,
    color=color.lime
)

meter_text = Text(
    "AI PROCESSING: 0 ms",
    position=(-0.84, -0.47),
    scale=0.85,
    color=color.white
)

count_text = Text(
    "GESTURE COUNT: 0",
    position=(0.25, -0.47),
    scale=0.85,
    color=color.orange
)

# ========== CAMERA + HAND DETECTION ==========
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65
)

# ========== CONTROL VARIABLES ==========
solar_running = True
last_camera_time = 0
camera_interval = 1 / 20
last_gesture = "WAITING"
gesture_count = 0
hand_missing_time = None

# ========== HAND GESTURE ==========
def detect_gesture(lm):

    fingers = [
        lm[8].y < lm[6].y,
        lm[12].y < lm[10].y,
        lm[16].y < lm[14].y,
        lm[20].y < lm[18].y
    ]

    if all(fingers):
        return "OPEN PALM"

    if not any(fingers):
        return "FIST"

    if fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:
        return "PEACE"

    return "HAND DETECTED"


# ========== UPDATE ==========
def update():

    global solar_running
    global last_camera_time
    global last_gesture
    global gesture_count
    global hand_missing_time

    # SOLAR SYSTEM MOVEMENT
    if solar_running:

        sun.rotation_y += 25 * time.dt
        sun.rotation_x += 10 * time.dt

        for p in planets:

            p["angle"] += p["speed"] * time.dt

            p["entity"].x = (
                p["radius"] * math.cos(p["angle"])
            )

            p["entity"].y = (
                center[1] + p["radius"] * math.sin(p["angle"])
            )

    # CAMERA PROCESSING
    now = pytime.perf_counter()

    if now - last_camera_time < camera_interval:
        return

    last_camera_time = now
    start = pytime.perf_counter()

    success, frame = cap.read()

    if not success:
        gesture_text.text = "GESTURE: CAMERA ERROR"
        status_text.text = "SYSTEM: CAMERA OFFLINE"
        return

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        lm = result.multi_hand_landmarks[0].landmark

        gesture = detect_gesture(lm)
        gesture_text.text = "GESTURE: " + gesture

        hand_missing_time = None

        if gesture != last_gesture:
            gesture_count += 1
            last_gesture = gesture

        # OPEN PALM = STOP
        if gesture == "OPEN PALM":

            solar_running = False
            status_text.text = "SYSTEM: PAUSED - OPEN PALM"
            status_text.color = color.yellow

        # FIST = PLAY
        elif gesture == "FIST":

            solar_running = True
            status_text.text = "SYSTEM: RUNNING - FIST"
            status_text.color = color.lime

        elif solar_running:
            status_text.text = "SYSTEM: RUNNING"
            status_text.color = color.lime

        else:
            status_text.text = "SYSTEM: PAUSED"
            status_text.color = color.yellow

    else:

        gesture_text.text = "GESTURE: NO HAND"

        if hand_missing_time is None:
            hand_missing_time = now

        # Keep previous solar state when hand disappears
        if solar_running:
            status_text.text = "SYSTEM: RUNNING"
        else:
            status_text.text = "SYSTEM: PAUSED"

    # PROCESSING METER
    elapsed = (
        pytime.perf_counter() - start
    ) * 1000

    meter_text.text = f"AI PROCESSING: {elapsed:.1f} ms"
    count_text.text = f"GESTURE COUNT: {gesture_count}"


# ========== KEYBOARD CONTROL ==========
def input(key):

    global solar_running

    if key == "space":
        solar_running = not solar_running

        status_text.text = (
            "SYSTEM: RUNNING"
            if solar_running else "SYSTEM: PAUSED"
        )

    if key == "escape":
        cap.release()
        hands.close()
        application.quit()


app.run()
cap.release()


