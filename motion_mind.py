
from ursina import *
import cv2
import mediapipe as mp

app = Ursina()
window.title = "MOTION MIND - AI SUN EXPLORER"
window.color = color.rgb(5, 8, 20)

camera.position = (0, 0, -9)
camera.look_at(Vec3(0, 0, 0))
AmbientLight(color=color.white)

# 3D Sun
sun = Entity(
    model="sphere",
    color=color.orange,
    scale=2,
    position=(1.5, 0, 0)
)

# Dashboard
panel = Entity(
    parent=camera.ui,
    model="quad",
    color=color.rgb(15, 25, 45),
    scale=(0.42, 0.9),
    position=(-0.72, 0)
)

Text("MOTION MIND", parent=camera.ui,
     position=(-0.91, 0.35), scale=1.4, color=color.cyan)

Text("AI SUN EXPLORER", parent=camera.ui,
     position=(-0.91, 0.25), scale=0.8, color=color.white)

gesture_text = Text(
    "GESTURE: WAITING",
    parent=camera.ui,
    position=(-0.91, 0.08),
    scale=0.8,
    color=color.lime
)

Text(
    "SHOW YOUR HAND TO CAMERA",
    parent=camera.ui,
    position=(-0.91, -0.05),
    scale=0.65,
    color=color.yellow
)

Text(
    "OPEN PALM = ROTATE\n"
    "FIST = STOP\n"
    "PEACE = ZOOM IN",
    parent=camera.ui,
    position=(-0.91, -0.20),
    scale=0.75,
    color=color.white
)

# Webcam and MediaPipe
webcam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

last_gesture = "WAITING"
zoomed = False

def update():
    global last_gesture, zoomed

    success, frame = webcam.read()

    if not success:
        gesture_text.text = "CAMERA NOT FOUND"
        return

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "WAITING"

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        # Four fingers: index, middle, ring, little
        index = lm[8].y < lm[6].y
        middle = lm[12].y < lm[10].y
        ring = lm[16].y < lm[14].y
        little = lm[20].y < lm[18].y

        fingers = [index, middle, ring, little]

        if all(fingers):
            gesture = "OPEN PALM"
        elif not any(fingers):
            gesture = "FIST"
        elif index and middle and not ring and not little:
            gesture = "PEACE"
        else:
            gesture = "HAND DETECTED"

        if gesture == "OPEN PALM":
            sun.rotation_y += time.dt * 80

        elif gesture == "FIST":
            pass

        elif gesture == "PEACE" and not zoomed:
            sun.scale = 2.5
            zoomed = True

        elif gesture != "PEACE":
            sun.scale = 2
            zoomed = False

        mp.solutions.drawing_utils.draw_landmarks(
            frame, hand, mp_hands.HAND_CONNECTIONS
        )

    gesture_text.text = "GESTURE: " + gesture

    cv2.imshow("MOTION MIND - HAND CAMERA", frame)
    cv2.waitKey(1)

def on_destroy():
    webcam.release()
    hands.close()
    cv2.destroyAllWindows()

app.run()
