import turtle
import random
import math
import time

# ---------- SETUP ----------
screen = turtle.Screen()
screen.setup(800, 800)
screen.title("TURTLE MAYHEM 🔥")
screen.bgcolor("black")
screen.tracer(0)

# ---------- PLAYER ----------
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.speed(0)
player.goto(0, -300)
player.setheading(90)

player_speed = 6
health = 5

# ---------- BULLETS ----------
bullets = []

def shoot():
    bullet = turtle.Turtle()
    bullet.shape("circle")
    bullet.color("yellow")
    bullet.penup()
    bullet.speed(0)
    bullet.goto(player.position())
    bullet.setheading(90)
    bullets.append(bullet)

# ---------- ENEMIES ----------
enemies = []
enemy_speed = 2

def spawn_enemy():
    enemy = turtle.Turtle()
    enemy.shape("square")
    enemy.color("red")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-380, 380)
    y = random.randint(200, 380)
    enemy.goto(x, y)
    enemies.append(enemy)

# ---------- HUD ----------
hud = turtle.Turtle()
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(-380, 360)

score = 0

def update_hud():
    hud.clear()
    hud.write(f"Score: {score}   Health: {health}", font=("Arial", 16, "bold"))

# ---------- MOVEMENT ----------
keys = {"w": False, "a": False, "s": False, "d": False}

def key_press(k): keys[k] = True
def key_release(k): keys[k] = False

for k in keys:
    screen.onkeypress(lambda k=k: key_press(k), k)
    screen.onkeyrelease(lambda k=k: key_release(k), k)

screen.onkeypress(shoot, "space")
screen.listen()

# ---------- GAME LOOP ----------
spawn_timer = 0
last_time = time.time()

update_hud()

while True:
    screen.update()
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    # Player movement
    if keys["a"] and player.xcor() > -380:
        player.setx(player.xcor() - player_speed)
    if keys["d"] and player.xcor() < 380:
        player.setx(player.xcor() + player_speed)
    if keys["w"] and player.ycor() < 380:
        player.sety(player.ycor() + player_speed)
    if keys["s"] and player.ycor() > -380:
        player.sety(player.ycor() - player_speed)

    # Bullets
    for bullet in bullets[:]:
        bullet.sety(bullet.ycor() + 10)
        if bullet.ycor() > 400:
            bullet.hideturtle()
            bullets.remove(bullet)

    # Enemies
    spawn_timer += dt
    if spawn_timer > max(0.5, 2 - score * 0.05):
        spawn_enemy()
        spawn_timer = 0

    for enemy in enemies[:]:
        enemy.sety(enemy.ycor() - enemy_speed)

        # Collision with player
        if enemy.distance(player) < 25:
            enemy.hideturtle()
            enemies.remove(enemy)
            health -= 1
            update_hud()
            if health <= 0:
                hud.goto(0, 0)
                hud.write("💀 GAME OVER 💀", align="center",
                          font=("Arial", 30, "bold"))
                screen.update()
                time.sleep(3)
                turtle.bye()
                quit()

        # Enemy off screen
        if enemy.ycor() < -400:
            enemy.hideturtle()
            enemies.remove(enemy)

        # Bullet collision
        for bullet in bullets[:]:
            if enemy.distance(bullet) < 20:
                enemy.hideturtle()
                bullet.hideturtle()
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                update_hud()
                enemy_speed = 2 + score * 0.1
                break