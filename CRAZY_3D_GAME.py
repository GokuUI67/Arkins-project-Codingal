import tkinter as tk
import math

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 900, 500
root = tk.Tk()
root.title("ULTRA Python 3D (No pygame)")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# ---------------- SETTINGS ----------------
FOV = math.pi / 3
NUM_RAYS = 400
MAX_DEPTH = 20
STEP = 0.02
SPEED = 0.08
ROT_SPEED = 0.05

# ---------------- MAP ----------------
MAP = [
    "111111111111",
    "100000000001",
    "101111011101",
    "100000000001",
    "111011111101",
    "100000000001",
    "101111111101",
    "100000000001",
    "111111111111",
]

# ---------------- PLAYER ----------------
px, py = 3.5, 3.5
angle = 0

keys = set()
root.bind("<KeyPress>", lambda e: keys.add(e.keysym))
root.bind("<KeyRelease>", lambda e: keys.discard(e.keysym))

# ---------------- DRAW 3D ----------------
def cast_rays():
    canvas.delete("all")

    # Ceiling
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT // 2, fill="#202840", outline="")
    # Floor
    canvas.create_rectangle(0, HEIGHT // 2, WIDTH, HEIGHT, fill="#303030", outline="")

    start_angle = angle - FOV / 2
    ray_angle = start_angle
    ray_step = FOV / NUM_RAYS

    for ray in range(NUM_RAYS):

        depth = 0
        hit = False

        while depth < MAX_DEPTH:
            x = px + math.cos(ray_angle) * depth
            y = py + math.sin(ray_angle) * depth

            if int(x) < 0 or int(y) < 0 or int(y) >= len(MAP) or int(x) >= len(MAP[0]):
                break

            if MAP[int(y)][int(x)] == "1":
                hit = True
                break

            depth += STEP

        if hit:
            depth *= math.cos(angle - ray_angle)  # fix fish-eye

            wall_height = HEIGHT / (depth + 0.0001)

            shade = int(255 / (1 + depth * depth * 0.15))
            color = f"#{shade:02x}{shade:02x}{shade:02x}"

            x1 = ray * (WIDTH / NUM_RAYS)
            y1 = HEIGHT / 2 - wall_height / 2
            x2 = x1 + (WIDTH / NUM_RAYS) + 1
            y2 = y1 + wall_height

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        ray_angle += ray_step

# ---------------- GAME LOOP ----------------
def update():
    global px, py, angle

    # Rotation
    if "a" in keys: angle -= ROT_SPEED
    if "d" in keys: angle += ROT_SPEED

    nx, ny = px, py

    # Movement
    if "w" in keys:
        nx += math.cos(angle) * SPEED
        ny += math.sin(angle) * SPEED
    if "s" in keys:
        nx -= math.cos(angle) * SPEED
        ny -= math.sin(angle) * SPEED

    # Collision
    if MAP[int(ny)][int(nx)] == "0":
        px, py = nx, ny

    cast_rays()
    root.after(16, update)  # ~60 FPS

update()
root.mainloop()