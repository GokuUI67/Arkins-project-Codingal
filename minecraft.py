import tkinter as tk
import random
import math

# -----------------------------
# 2D Minecraft-ish (no pygame)
# - WASD / Arrow keys to move
# - Space to jump
# - Left click: break block
# - Right click: place selected block
# - 1-5 selects hotbar item
# -----------------------------

W, H = 960, 540
TILE = 24
GRAVITY = 0.65
MAX_FALL = 12
MOVE_SPEED = 4.2
JUMP_V = -12.5

WORLD_W = 260
WORLD_H = 120

# Tile IDs
AIR   = 0
GRASS = 1
DIRT  = 2
STONE = 3
WOOD  = 4
LEAF  = 5
SAND  = 6
WATER = 7

TILE_COLORS = {
    AIR:   None,
    GRASS: "#3cb043",
    DIRT:  "#8b5a2b",
    STONE: "#7d7f86",
    WOOD:  "#a0703a",
    LEAF:  "#2e8b57",
    SAND:  "#d9c37a",
    WATER: "#3b82f6",
}

TILE_NAMES = {
    GRASS: "Grass",
    DIRT:  "Dirt",
    STONE: "Stone",
    WOOD:  "Wood",
    LEAF:  "Leaves",
    SAND:  "Sand",
    WATER: "Water",
}

HOTBAR = [DIRT, STONE, WOOD, SAND, WATER]
HOTBAR_KEYS = ["1", "2", "3", "4", "5"]

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

class Game:
    def __init__(self, root):
        self.root = root
        root.title("2D Minecraft-ish (tkinter)")

        self.canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0)
        self.canvas.pack()

        self.keys = set()
        self.mouse_x = 0
        self.mouse_y = 0
        self.selected = 0  # hotbar index

        # world + inventory
        self.world = [[AIR for _ in range(WORLD_W)] for _ in range(WORLD_H)]
        self.inv = {t: 0 for t in TILE_NAMES.keys()}
        self.generate_world()

        # player (in pixels)
        self.pw = TILE * 0.75
        self.ph = TILE * 1.25
        self.px = TILE * 10
        self.py = TILE * 10
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False

        # camera
        self.cam_x = 0
        self.cam_y = 0

        # render cache: only draw visible tiles
        self.tile_items = {}  # (tx,ty) -> canvas item id

        # UI items
        self.ui_text = self.canvas.create_text(
            10, 10, anchor="nw", fill="white", font=("Arial", 12),
            text=""
        )

        # bindings
        root.bind("<KeyPress>", self.on_key_down)
        root.bind("<KeyRelease>", self.on_key_up)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.break_block)
        self.canvas.bind("<Button-3>", self.place_block)  # right click

        self.loop()

    # -------- World Gen --------
    def height_fn(self, x):
        # Smooth hills
        return int(55 + 8*math.sin(x/14) + 6*math.sin(x/33) + random.randint(-1, 1))

    def generate_world(self):
        random.seed()

        heights = [self.height_fn(x) for x in range(WORLD_W)]

        for x in range(WORLD_W):
            ground = clamp(heights[x], 20, WORLD_H - 10)
            for y in range(WORLD_H):
                if y < ground:
                    self.world[y][x] = AIR
                else:
                    depth = y - ground
                    if depth == 0:
                        self.world[y][x] = GRASS
                    elif depth < 4:
                        self.world[y][x] = DIRT
                    else:
                        self.world[y][x] = STONE

            # add sand near "beach" areas
            if 90 < x < 120:
                for y in range(ground, min(WORLD_H, ground + 4)):
                    self.world[y][x] = SAND

            # water pool
            if 100 < x < 115:
                water_top = ground - 3
                for y in range(max(0, water_top), ground):
                    self.world[y][x] = WATER

            # trees sometimes
            if x > 5 and x < WORLD_W - 5 and random.random() < 0.08:
                g = ground
                if self.world[g][x] == GRASS and self.world[g-1][x] == AIR:
                    self.place_tree(x, g-1)

        # player spawn: find a safe spot near x=10
        sx = 10
        gy = heights[sx]
        self.px = sx * TILE
        self.py = (gy - 4) * TILE

    def place_tree(self, x, y):
        trunk_h = random.randint(4, 6)
        for i in range(trunk_h):
            ty = y - i
            if 0 <= ty < WORLD_H:
                self.world[ty][x] = WOOD

        top = y - trunk_h
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if abs(dx) + abs(dy) <= 3:
                    tx, ty = x + dx, top + dy
                    if 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
                        if self.world[ty][tx] == AIR:
                            self.world[ty][tx] = LEAF

    # -------- Input --------
    def on_key_down(self, e):
        k = e.keysym.lower()
        self.keys.add(k)
        if k in HOTBAR_KEYS:
            self.selected = int(k) - 1

    def on_key_up(self, e):
        k = e.keysym.lower()
        if k in self.keys:
            self.keys.remove(k)

    def on_mouse_move(self, e):
        self.mouse_x, self.mouse_y = e.x, e.y

    # -------- Helpers --------
    def tile_at(self, tx, ty):
        if 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
            return self.world[ty][tx]
        return STONE  # outside world is solid

    def set_tile(self, tx, ty, t):
        if 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
            self.world[ty][tx] = t

    def world_to_screen(self, wx, wy):
        return wx - self.cam_x, wy - self.cam_y

    def screen_to_tile(self, sx, sy):
        wx = sx + self.cam_x
        wy = sy + self.cam_y
        return int(wx // TILE), int(wy // TILE)

    def is_solid(self, t):
        return t not in (AIR, WATER)

    # -------- Mining / Placing --------
    def break_block(self, _=None):
        tx, ty = self.screen_to_tile(self.mouse_x, self.mouse_y)
        t = self.tile_at(tx, ty)
        if t == AIR:
            return

        # don't let you break blocks inside your body (simple protection)
        if self.player_intersects_tile(tx, ty):
            return

        # collect (except water)
        if t != WATER and t in self.inv:
            self.inv[t] += 1

        self.set_tile(tx, ty, AIR)

    def place_block(self, _=None):
        block = HOTBAR[self.selected]
        if self.inv.get(block, 0) <= 0:
            return

        tx, ty = self.screen_to_tile(self.mouse_x, self.mouse_y)
        if self.tile_at(tx, ty) != AIR:
            return

        # don't place inside your body
        if self.player_intersects_tile(tx, ty):
            return

        self.set_tile(tx, ty, block)
        self.inv[block] -= 1

    def player_intersects_tile(self, tx, ty):
        # tile rect in world pixels
        rx1, ry1 = tx * TILE, ty * TILE
        rx2, ry2 = rx1 + TILE, ry1 + TILE

        px1, py1 = self.px, self.py
        px2, py2 = self.px + self.pw, self.py + self.ph

        return not (px2 <= rx1 or px1 >= rx2 or py2 <= ry1 or py1 >= ry2)

    # -------- Physics / Collision --------
    def move_and_collide(self, dx, dy):
        # move X
        self.px += dx
        if dx != 0:
            self.resolve_collisions(axis="x")

        # move Y
        self.py += dy
        if dy != 0:
            self.on_ground = False
            self.resolve_collisions(axis="y")

    def resolve_collisions(self, axis):
        # check tiles around player
        px1, py1 = self.px, self.py
        px2, py2 = self.px + self.pw, self.py + self.ph

        left = int(px1 // TILE) - 1
        right = int(px2 // TILE) + 1
        top = int(py1 // TILE) - 1
        bottom = int(py2 // TILE) + 1

        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                t = self.tile_at(tx, ty)
                if not self.is_solid(t):
                    continue

                rx1, ry1 = tx * TILE, ty * TILE
                rx2, ry2 = rx1 + TILE, ry1 + TILE

                # AABB overlap?
                if (px2 <= rx1 or px1 >= rx2 or py2 <= ry1 or py1 >= ry2):
                    continue

                if axis == "x":
                    if self.vx > 0:
                        # push left
                        self.px = rx1 - self.pw
                    elif self.vx < 0:
                        # push right
                        self.px = rx2
                    self.vx = 0
                    px1, px2 = self.px, self.px + self.pw

                else:  # y
                    if self.vy > 0:
                        # falling: land on top
                        self.py = ry1 - self.ph
                        self.vy = 0
                        self.on_ground = True
                    elif self.vy < 0:
                        # jumping: hit head
                        self.py = ry2
                        self.vy = 0
                    py1, py2 = self.py, self.py + self.ph

    # -------- Render --------
    def draw(self):
        # camera follows player
        self.cam_x = clamp(self.px + self.pw/2 - W/2, 0, WORLD_W*TILE - W)
        self.cam_y = clamp(self.py + self.ph/2 - H/2, 0, WORLD_H*TILE - H)

        # sky bg
        self.canvas.configure(bg="#79c2ff")

        # visible tile range
        tx0 = int(self.cam_x // TILE) - 1
        ty0 = int(self.cam_y // TILE) - 1
        tx1 = int((self.cam_x + W) // TILE) + 2
        ty1 = int((self.cam_y + H) // TILE) + 2

        tx0 = max(0, tx0); ty0 = max(0, ty0)
        tx1 = min(WORLD_W - 1, tx1); ty1 = min(WORLD_H - 1, ty1)

        visible_now = set()

        for ty in range(ty0, ty1 + 1):
            wy = ty * TILE
            for tx in range(tx0, tx1 + 1):
                t = self.world[ty][tx]
                key = (tx, ty)
                visible_now.add(key)

                color = TILE_COLORS.get(t)
                if color is None:
                    # delete if exists
                    if key in self.tile_items:
                        self.canvas.delete(self.tile_items[key])
                        del self.tile_items[key]
                    continue

                sx, sy = self.world_to_screen(tx * TILE, wy)

                if key not in self.tile_items:
                    self.tile_items[key] = self.canvas.create_rectangle(
                        sx, sy, sx + TILE, sy + TILE,
                        fill=color, outline=""
                    )
                else:
                    self.canvas.coords(self.tile_items[key], sx, sy, sx + TILE, sy + TILE)
                    self.canvas.itemconfig(self.tile_items[key], fill=color)

        # remove tiles that are no longer visible
        for key in list(self.tile_items.keys()):
            if key not in visible_now:
                self.canvas.delete(self.tile_items[key])
                del self.tile_items[key]

        # player
        pxs, pys = self.world_to_screen(self.px, self.py)
        if not hasattr(self, "player_item"):
            self.player_item = self.canvas.create_rectangle(
                pxs, pys, pxs + self.pw, pys + self.ph,
                fill="#ffd54a", outline="#c49d1a", width=2
            )
        else:
            self.canvas.coords(self.player_item, pxs, pys, pxs + self.pw, pys + self.ph)

        # crosshair highlight (tile under mouse)
        tx, ty = self.screen_to_tile(self.mouse_x, self.mouse_y)
        sx, sy = self.world_to_screen(tx * TILE, ty * TILE)
        if not hasattr(self, "cursor_box"):
            self.cursor_box = self.canvas.create_rectangle(
                sx, sy, sx + TILE, sy + TILE,
                outline="white", width=2
            )
        else:
            self.canvas.coords(self.cursor_box, sx, sy, sx + TILE, sy + TILE)

        # UI text + hotbar
        sel_tile = HOTBAR[self.selected]
        inv_line = " | ".join([f"{i+1}:{TILE_NAMES[HOTBAR[i]]}={self.inv.get(HOTBAR[i],0)}" for i in range(5)])
        self.canvas.itemconfig(
            self.ui_text,
            text=f"Move: A/D or ←/→  Jump: Space  Break: Left Click  Place: Right Click\n"
                 f"Selected: {self.selected+1} ({TILE_NAMES[sel_tile]})\n"
                 f"{inv_line}"
        )

        # hotbar rectangles
        if not hasattr(self, "hotbar_items"):
            self.hotbar_items = []
            base_x = W//2 - (5*(48+10)-10)//2
            y = H - 60
            for i in range(5):
                x = base_x + i*(48+10)
                r = self.canvas.create_rectangle(x, y, x+48, y+48, fill="#1f2937", outline="white", width=2)
                c = TILE_COLORS[HOTBAR[i]]
                s = self.canvas.create_rectangle(x+10, y+10, x+38, y+38, fill=c, outline="")
                n = self.canvas.create_text(x+24, y+58, text=str(i+1), fill="white", font=("Arial", 10))
                self.hotbar_items.append((r, s, n))
        # update selection outline
        for i, (r, s, n) in enumerate(self.hotbar_items):
            self.canvas.itemconfig(r, outline="yellow" if i == self.selected else "white", width=3 if i == self.selected else 2)

    # -------- Main Loop --------
    def loop(self):
        # movement input
        left = ("a" in self.keys) or ("left" in self.keys)
        right = ("d" in self.keys) or ("right" in self.keys)

        self.vx = 0
        if left:
            self.vx -= MOVE_SPEED
        if right:
            self.vx += MOVE_SPEED

        if ("space" in self.keys) and self.on_ground:
            self.vy = JUMP_V
            self.on_ground = False

        # gravity
        self.vy = clamp(self.vy + GRAVITY, -100, MAX_FALL)

        # apply movement
        self.move_and_collide(self.vx, self.vy)

        # draw
        self.draw()

        self.root.after(16, self.loop)  # ~60fps


if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()