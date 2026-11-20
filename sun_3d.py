
from ursina import *
import random
import math

app = Ursina()
window.title = "MOTION MIND - THE SUN"
window.color = color.rgb(5, 8, 20)

camera.position = (0, 0, -8)
camera.look_at(Vec3(0, 0, 0))

sun = Entity(
    model="sphere",
    color=color.orange,
    scale=2
)

# Glowing particles around the Sun
particles = []

for i in range(350):
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    radius = random.uniform(1.8, 2.8)

    x = radius * math.sin(phi) * math.cos(theta)
    y = radius * math.cos(phi)
    z = radius * math.sin(phi) * math.sin(theta)

    particle = Entity(
        model="sphere",
        position=(x, y, z),
        scale=random.uniform(0.015, 0.035),
        color=random.choice([
            color.orange,
            color.yellow,
            color.rgb(255, 190, 90)
        ])
    )

    particles.append(particle)

Text(
    text="THE SUN",
    position=(-0.85, 0.43),
    scale=2,
    color=color.white
)

def update():
    sun.rotation_y += time.dt * 10

    for particle in particles:
        particle.rotation_y += time.dt * 5

app.run()
