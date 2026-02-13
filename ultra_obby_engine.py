import tkinter as tk
import math
import time

# ---------- WINDOW ----------
WIDTH, HEIGHT = 900, 600
root = tk.Tk()
root.title("Safe 3D Obby")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# ---------- CAMERA ----------
cam_x, cam_y, cam_z = 0, 2, -8
yaw = 0

# ---------- PHYSICS ----------
vel_y = 0
gravity = -0.025
jump_power = 0.38
on_ground = False
speed = 0.15
rot_speed = 0.05

# ---------- GAME ----------
level = 0
start_time = time.time()
dead = False

# ---------- INPUT ----------
keys = set()
root.bind("<KeyPress>", lambda e: keys.add(e.keysym))
root.bind("<KeyRelease>", lambda e: keys.discard(e.keysym))

# ---------- LEVELS ----------
LEVELS = [
    [("floor",0,0,0,6), ("move",4,1,8,2), ("lava",-4,0,12,3),
     ("enemy",0,1,16,1), ("win",0,2,22,3)],
    [("floor",0,0,0,6), ("move",-5,2,10,2), ("move",5,3,16,2),
     ("lava",0,0,20,4), ("enemy",-3,1,24,1), ("win",0,4,30,3)]
]

# ---------- PROJECTION ----------
def project(x,y,z):
    z -= cam_z
    if z <= 0.1:
        return None
    f = 400/z
    return WIDTH/2 + (x-cam_x)*f, HEIGHT/2 - (y-cam_y)*f

def draw_cube(x,y,z,s,color):
    pts=[]
    for dx in(-s,s):
        for dy in(-s,s):
            for dz in(-s,s):
                p=project(x+dx,y+dy,z+dz)
                if p: pts.append(p)
    if len(pts)>=4:
        canvas.create_polygon(pts[0],pts[1],pts[3],pts[2],
                              fill=color,outline="white")

# ---------- COLLISION ----------
def respawn():
    global cam_x,cam_y,cam_z,vel_y,dead,start_time
    cam_x,cam_y,cam_z=0,2,-8
    vel_y=0
    dead=False
    start_time=time.time()

def check(objects):
    global cam_y,vel_y,on_ground,dead,level
    on_ground=False

    for t,x,y,z,s in objects:

        if t in("floor","move","win"):
            if abs(cam_x-x)<s and abs(cam_z-z)<s and cam_y<=y+1:
                cam_y=y+1
                vel_y=0
                on_ground=True

        if t=="lava" and abs(cam_x-x)<s and abs(cam_z-z)<s:
            dead=True

        if t=="enemy" and abs(cam_x-x)<s and abs(cam_z-z)<s:
            dead=True

        if t=="win" and abs(cam_x-x)<s and abs(cam_z-z)<s:
            level=(level+1)%len(LEVELS)
            respawn()

# ---------- UPDATE ----------
enemy_angle=0

def update():
    global cam_x,cam_y,cam_z,yaw,vel_y,enemy_angle

    if dead:
        respawn()

    objs=LEVELS[level]

    # rotation (SAFE)
    if "a" in keys: yaw-=rot_speed
    if "d" in keys: yaw+=rot_speed

    dx=math.sin(yaw)*speed
    dz=math.cos(yaw)*speed

    if "w" in keys:
        cam_x+=dx; cam_z+=dz
    if "s" in keys:
        cam_x-=dx; cam_z-=dz

    if "space" in keys and on_ground:
        vel_y=jump_power

    vel_y+=gravity
    cam_y+=vel_y

    # moving + enemy
    moved=[]
    enemy_angle+=0.02
    for t,x,y,z,s in objs:
        if t=="move": x+=math.sin(time.time())*2
        if t=="enemy":
            x+=math.sin(enemy_angle)*0.05
            z+=math.cos(enemy_angle)*0.05
        moved.append((t,x,y,z,s))

    check(moved)

    # ----- DRAW -----
    canvas.delete("all")
    canvas.create_rectangle(0,0,WIDTH,HEIGHT/2,fill="#203a60",outline="")
    canvas.create_rectangle(0,HEIGHT/2,WIDTH,HEIGHT,fill="#101010",outline="")

    colors={"floor":"#6aa9ff","move":"#ffd966","lava":"#ff3b3b",
            "enemy":"#a000ff","win":"#00ff88"}

    for t,x,y,z,s in moved:
        draw_cube(x,y,z,s,colors[t])

    t=round(time.time()-start_time,2)
    canvas.create_text(80,30,text=f"⏱ {t}s",fill="white",
                       font=("Arial",18,"bold"))
    canvas.create_text(80,60,text=f"LEVEL {level+1}",
                       fill="white",font=("Arial",14))

    root.after(16, update)   # FPS limit → SAFE

update()
root.mainloop()