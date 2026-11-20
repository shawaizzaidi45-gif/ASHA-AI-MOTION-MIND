
from ursina import *

app = Ursina()
window.title = "MOTION MIND - AI SUN EXPLORER"
window.color = color.rgb(5, 8, 20)

camera.position = (0, 0, -9)
camera.look_at(Vec3(0, 0, 0))

AmbientLight(color=color.white)

# Sun on right side
sun = Entity(
    model="sphere",
    color=color.orange,
    scale=2,
    position=(1.5, 0, 0)
)

# Left dashboard
panel = Entity(
    parent=camera.ui,
    model="quad",
    color=color.rgb(15, 25, 45),
    scale=(0.38, 0.9),
    position=(-0.32, 0)
)

Text(
    "MOTION MIND",
    parent=camera.ui,
    position=(-0.47, 0.35),
    scale=1.5,
    color=color.cyan
)

Text(
    "AI SUN EXPLORER",
    parent=camera.ui,
    position=(-0.46, 0.25),
    scale=0.8,
    color=color.white
)

Text(
    "GESTURE STATUS",
    parent=camera.ui,
    position=(-0.46, 0.10),
    scale=0.9,
    color=color.lime
)

Text(
    "WAITING FOR HAND...",
    parent=camera.ui,
    position=(-0.46, 0.02),
    scale=0.7,
    color=color.yellow
)

Text(
    "SOLAR LAYERS",
    parent=camera.ui,
    position=(-0.46, -0.12),
    scale=0.9,
    color=color.cyan
)

Text(
    "1 - Corona\n"
    "2 - Chromosphere\n"
    "3 - Photosphere\n"
    "4 - Core\n\n"
    "Arrow keys - Rotate\n"
    "+ / - - Zoom",
    parent=camera.ui,
    position=(-0.46, -0.20),
    scale=0.7,
    color=color.white
)

def input(key):
    if key in ["1", "2", "3", "4"]:
        colors = [
            color.orange,
            color.red,
            color.rgb(255, 150, 20),
            color.yellow
        ]
        sun.color = colors[int(key)-1]

    if key == "left arrow":
        sun.rotation_y -= 15
    if key == "right arrow":
        sun.rotation_y += 15
    if key == "+" or key == "=":
        sun.scale += 0.2
    if key == "-":
        sun.scale -= 0.2

def update():
    sun.rotation_y += time.dt * 8

app.run()
