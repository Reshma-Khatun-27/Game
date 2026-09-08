"""
Garden Turtle Adventure - Shelly's Garden Tour
A vibrant interactive Python Turtle simulation featuring a scenic garden,
blooming flowers, a lily pond, stepping stones, and an animated turtle that
explores autonomously or responds to player controls.
"""

import math
import random
import turtle

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
SCREEN_WIDTH = 920
SCREEN_HEIGHT = 720
FPS_MS = 25  # ~40 frames per second for smooth movement
WALK_SPEED = 3.5

# Landmark destinations in the garden (x, y, name, interaction_text, emoji)
LANDMARKS = [
    {
        "name": "Lily Pond",
        "pos": (-240, 110),
        "radius": 95,
        "text": "Splashing gently and taking a drink at the cool Lily Pond",
        "emoji": "💧",
    },
    {
        "name": "Sunflower Patch",
        "pos": (250, 170),
        "radius": 85,
        "text": "Basking under the tall golden Sunflowers",
        "emoji": "🌻",
    },
    {
        "name": "Tulip Garden",
        "pos": (-220, -180),
        "radius": 80,
        "text": "Admiring the bright red and purple Tulips",
        "emoji": "🌷",
    },
    {
        "name": "Daisy & Wildflower Meadow",
        "pos": (230, -170),
        "radius": 85,
        "text": "Catching gentle scents in the Daisy Meadow",
        "emoji": "🌼",
    },
    {
        "name": "Old Shady Tree",
        "pos": (70, 140),
        "radius": 90,
        "text": "Resting cozily in the breezy shade of the Apple Tree",
        "emoji": "🌳",
    },
    {
        "name": "Fresh Clover Patch",
        "pos": (-60, -90),
        "radius": 75,
        "text": "Munching on tasty tender green Clover leaves",
        "emoji": "🍀",
    },
    {
        "name": "Stepping Stone Path",
        "pos": (30, -220),
        "radius": 70,
        "text": "Sunbathing warmly on the smooth garden stones",
        "emoji": "🪨",
    },
]

# ==============================================================================
# DRAWING UTILITIES
# ==============================================================================
def draw_rectangle(t, x, y, width, height, fill_color, border_color=None):
    """Draw a filled rectangle with top-left at (x, y)."""
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    if border_color:
        t.pencolor(border_color)
    else:
        t.pencolor(fill_color)
    t.fillcolor(fill_color)
    t.pendown()
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()
    t.penup()


def draw_circle(t, x, y, radius, fill_color, border_color=None, border_width=1):
    """Draw a filled circle centered at (x, y)."""
    t.penup()
    t.goto(x, y - radius)
    t.setheading(0)
    t.width(border_width)
    if border_color:
        t.pencolor(border_color)
    else:
        t.pencolor(fill_color)
    t.fillcolor(fill_color)
    t.pendown()
    t.begin_fill()
    t.circle(radius)
    t.end_fill()
    t.penup()


def draw_ellipse(t, x, y, rx, ry, fill_color, border_color=None):
    """Approximate a filled ellipse centered at (x, y)."""
    t.penup()
    t.goto(x + rx, y)
    t.setheading(90)
    if border_color:
        t.pencolor(border_color)
    else:
        t.pencolor(fill_color)
    t.fillcolor(fill_color)
    t.pendown()
    t.begin_fill()
    steps = 36
    for i in range(steps + 1):
        angle = (2 * math.pi / steps) * i
        px = x + rx * math.cos(angle)
        py = y + ry * math.sin(angle)
        t.goto(px, py)
    t.end_fill()
    t.penup()


# ==============================================================================
# GARDEN LANDSCAPE DRAWING
# ==============================================================================
def draw_garden_fence(t):
    """Draw a wooden boundary fence around the garden."""
    fence_color = "#c89d66"
    post_color = "#9b6b38"
    fence_y = 295

    # Horizontal rails across top
    draw_rectangle(t, -440, fence_y, 880, 10, fence_color, post_color)
    draw_rectangle(t, -440, fence_y - 25, 880, 10, fence_color, post_color)

    # Vertical pickets
    for x in range(-430, 440, 28):
        t.penup()
        t.goto(x - 5, fence_y - 45)
        t.fillcolor(fence_color)
        t.pencolor(post_color)
        t.pendown()
        t.begin_fill()
        t.goto(x - 5, fence_y + 10)
        t.goto(x, fence_y + 20)  # Pointed picket top
        t.goto(x + 5, fence_y + 10)
        t.goto(x + 5, fence_y - 45)
        t.goto(x - 5, fence_y - 45)
        t.end_fill()
        t.penup()


def draw_stepping_stones(t):
    """Draw an organic meandering stone walkway."""
    stones = [
        (-40, -250, 22, 17, 10),
        (-10, -230, 24, 18, -15),
        (20, -205, 26, 20, 5),
        (45, -170, 25, 19, 25),
        (60, -125, 23, 17, -10),
        (55, -75, 24, 18, 15),
        (35, -25, 25, 19, -20),
        (5, 25, 23, 18, 10),
        (-35, 65, 26, 20, -15),
        (-80, 95, 24, 18, 20),
        (-130, 110, 22, 16, -5),
    ]

    for sx, sy, rx, ry, rot in stones:
        # Cast soft shadow
        draw_ellipse(t, sx + 2, sy - 2, rx + 1, ry + 1, "#3e6d27")
        # Base stone
        draw_ellipse(t, sx, sy, rx, ry, "#9ca3af", "#64748b")
        # Highlight texture
        draw_ellipse(t, sx - 4, sy + 3, rx * 0.5, ry * 0.45, "#cbd5e1")


def draw_pond(t, cx, cy):
    """Draw a realistic layered lily pond with lily pads and flowers."""
    # Outer stone shoreline
    pebbles = [
        (cx - 100, cy + 10, 14), (cx - 95, cy + 50, 12), (cx - 70, cy + 80, 15),
        (cx - 30, cy + 95, 16), (cx + 20, cy + 90, 13), (cx + 65, cy + 70, 15),
        (cx + 90, cy + 30, 14), (cx + 95, cy - 20, 16), (cx + 70, cy - 65, 13),
        (cx + 25, cy - 85, 15), (cx - 25, cy - 90, 16), (cx - 75, cy - 65, 14),
        (cx - 95, cy - 25, 13),
    ]
    for px, py, pr in pebbles:
        draw_circle(t, px, py, pr, "#78716c", "#44403c")
        draw_circle(t, px - 2, py + 2, pr * 0.45, "#a8a29e")

    # Mud/soil ring
    draw_ellipse(t, cx, cy, 95, 78, "#4d7c0f", "#365314")
    # Shallow water
    draw_ellipse(t, cx, cy, 90, 72, "#38bdf8", "#0284c7")
    # Deep water
    draw_ellipse(t, cx - 5, cy - 2, 78, 60, "#0284c7", "#0369a1")

    # Water reflections/ripples
    for rx_off, ry_off, w in [(-30, 20, 35), (20, -15, 40), (-10, -35, 25)]:
        t.penup()
        t.goto(cx + rx_off - w / 2, cy + ry_off)
        t.setheading(0)
        t.pencolor("#e0f2fe")
        t.width(2)
        t.pendown()
        t.forward(w)
        t.penup()

    # Lily Pads
    pads = [(cx - 45, cy - 15, 17, 30), (cx + 35, cy + 20, 19, 120), (cx - 10, cy + 40, 14, 210)]
    for lx, ly, lr, cutout_angle in pads:
        t.penup()
        t.goto(lx, ly)
        t.setheading(cutout_angle)
        t.fillcolor("#15803d")
        t.pencolor("#166534")
        t.width(1.5)
        t.pendown()
        t.begin_fill()
        t.circle(lr, 320)  # Classic lily pad notch
        t.goto(lx, ly)
        t.end_fill()
        t.penup()

    # Water Lilies (Blossoms)
    blossoms = [(cx - 45, cy - 15), (cx + 35, cy + 20)]
    for bx, by in blossoms:
        t.penup()
        for pet_angle in range(0, 360, 45):
            rad = math.radians(pet_angle)
            px = bx + math.cos(rad) * 6
            py = by + math.sin(rad) * 6
            draw_circle(t, px, py, 4, "#fbcfe8", "#f472b6")
        draw_circle(t, bx, by, 3.5, "#fef08a", "#eab308")


def draw_tree(t, tx, ty):
    """Draw a shady, beautiful garden apple tree."""
    # Tree shadow
    draw_ellipse(t, tx + 10, ty - 60, 85, 30, "#3e6d27")

    # Trunk
    t.penup()
    t.goto(tx - 18, ty - 60)
    t.fillcolor("#78350f")
    t.pencolor("#451a03")
    t.width(2)
    t.pendown()
    t.begin_fill()
    t.goto(tx - 12, ty + 10)
    t.goto(tx - 35, ty + 45)  # Left branch
    t.goto(tx - 25, ty + 50)
    t.goto(tx - 5, ty + 20)
    t.goto(tx + 20, ty + 50)  # Right branch
    t.goto(tx + 30, ty + 45)
    t.goto(tx + 12, ty + 10)
    t.goto(tx + 18, ty - 60)
    t.goto(tx - 18, ty - 60)
    t.end_fill()
    t.penup()

    # Foliage layers (multi-tone clusters for lush depth)
    foliage = [
        (tx - 45, ty + 40, 42, "#15803d"),
        (tx + 45, ty + 40, 42, "#166534"),
        (tx, ty + 75, 48, "#16a34a"),
        (tx - 25, ty + 70, 38, "#22c55e"),
        (tx + 25, ty + 70, 38, "#15803d"),
        (tx, ty + 45, 40, "#16a34a"),
    ]
    for fx, fy, fr, fc in foliage:
        draw_circle(t, fx, fy, fr, fc)

    # Ripe red apples
    apples = [
        (tx - 35, ty + 30), (tx + 30, ty + 25), (tx - 10, ty + 65),
        (tx + 25, ty + 65), (tx - 40, ty + 65), (tx + 40, ty + 45)
    ]
    for ax, ay in apples:
        draw_circle(t, ax, ay, 6, "#dc2626", "#991b1b")
        # Tiny apple shine
        draw_circle(t, ax - 1.5, ay + 1.5, 1.8, "#fca5a5")


def draw_sunflower(t, x, y, size=1.0):
    """Draw a sunflower with bright golden petals and chocolate center."""
    stem_h = 55 * size
    # Stem
    t.penup()
    t.goto(x, y - stem_h)
    t.pencolor("#15803d")
    t.width(4 * size)
    t.pendown()
    t.goto(x, y)
    t.penup()

    # Leaf
    t.goto(x, y - stem_h * 0.45)
    t.setheading(30)
    t.fillcolor("#16a34a")
    t.pencolor("#15803d")
    t.pendown()
    t.begin_fill()
    t.circle(12 * size, 90)
    t.left(90)
    t.circle(12 * size, 90)
    t.end_fill()
    t.penup()

    # Petals
    num_petals = 14
    for i in range(num_petals):
        angle = (360 / num_petals) * i
        rad = math.radians(angle)
        px = x + math.cos(rad) * (14 * size)
        py = y + math.sin(rad) * (14 * size)
        draw_circle(t, px, py, 6 * size, "#fbbf24", "#d97706")

    # Center seed disk
    draw_circle(t, x, y, 14 * size, "#451a03", "#78350f")
    # Texture ring in center
    draw_circle(t, x, y, 9 * size, "#78350f")


def draw_tulip(t, x, y, color="#ef4444", size=1.0):
    """Draw an elegant tulip blossom with leaves."""
    stem_h = 42 * size
    # Stem
    t.penup()
    t.goto(x, y - stem_h)
    t.pencolor("#16a34a")
    t.width(3 * size)
    t.pendown()
    t.goto(x, y)
    t.penup()

    # Leaf on stem
    t.goto(x, y - stem_h * 0.5)
    t.setheading(120)
    t.fillcolor("#22c55e")
    t.pendown()
    t.begin_fill()
    t.circle(14 * size, 70)
    t.left(110)
    t.circle(14 * size, 70)
    t.end_fill()
    t.penup()

    # Tulip Cup (3 overlapping petals)
    draw_ellipse(t, x - 5 * size, y + 4 * size, 6 * size, 11 * size, color)
    draw_ellipse(t, x + 5 * size, y + 4 * size, 6 * size, 11 * size, color)
    draw_ellipse(t, x, y + 3 * size, 7 * size, 12 * size, color)


def draw_daisy(t, x, y, size=1.0):
    """Draw a daisy with white petals and sunny center."""
    stem_h = 35 * size
    # Stem
    t.penup()
    t.goto(x, y - stem_h)
    t.pencolor("#15803d")
    t.width(2.5 * size)
    t.pendown()
    t.goto(x, y)
    t.penup()

    # White petals
    num_petals = 10
    for i in range(num_petals):
        angle = (360 / num_petals) * i
        rad = math.radians(angle)
        px = x + math.cos(rad) * (9 * size)
        py = y + math.sin(rad) * (9 * size)
        draw_circle(t, px, py, 4.2 * size, "#ffffff", "#e2e8f0")

    # Yellow center
    draw_circle(t, x, y, 5.5 * size, "#facc15", "#ca8a04")


def draw_clover_patch(t, cx, cy):
    """Draw sweet little 3-leaf clovers."""
    clover_spots = [
        (cx - 30, cy + 10), (cx - 10, cy + 25), (cx + 18, cy + 15),
        (cx - 20, cy - 20), (cx + 10, cy - 15), (cx + 30, cy - 5),
    ]
    for clx, cly in clover_spots:
        for angle in [90, 210, 330]:
            rad = math.radians(angle)
            lx = clx + math.cos(rad) * 6
            ly = cly + math.sin(rad) * 6
            draw_circle(t, lx, ly, 4.5, "#4ade80", "#16a34a")
        draw_circle(t, clx, cly, 2.5, "#22c55e")


def draw_grass_tufts(t):
    """Scatter subtle aesthetic grass blades across the lawn."""
    tufts = [
        (-380, -50), (-320, 200), (-160, 230), (-100, -220), (-10, -140),
        (130, -50), (140, 240), (340, 230), (370, -100), (340, -240),
        (-320, -120), (-140, -50), (10, 180), (180, 50)
    ]
    t.width(2)
    t.pencolor("#4d7c0f")
    for gx, gy in tufts:
        t.penup()
        t.goto(gx, gy)
        t.pendown()
        t.goto(gx - 4, gy + 12)
        t.penup()
        t.goto(gx, gy)
        t.pendown()
        t.goto(gx, gy + 15)
        t.penup()
        t.goto(gx, gy)
        t.pendown()
        t.goto(gx + 5, gy + 11)
        t.penup()


def render_entire_garden(bg):
    """Render the full high-detail garden scenery."""
    bg.clear()
    bg.hideturtle()
    bg.speed(0)

    # 1. Base Garden Lawn (Vibrant meadow green)
    draw_rectangle(bg, -SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 + 10,
                   SCREEN_WIDTH + 20, SCREEN_HEIGHT + 20, "#5b933d")

    # 2. Border Fence along top edge
    draw_garden_fence(bg)

    # 3. Grass Tufts for organic texture
    draw_grass_tufts(bg)

    # 4. Stepping Stones
    draw_stepping_stones(bg)

    # 5. Lily Pond (top-left)
    draw_pond(bg, -240, 110)

    # 6. Shady Tree (top-center/right)
    draw_tree(bg, 70, 140)

    # 7. Clover Patch (center-left)
    draw_clover_patch(bg, -60, -90)

    # 8. Sunflower Corner (top-right)
    draw_sunflower(bg, 230, 210, 1.1)
    draw_sunflower(bg, 285, 200, 1.2)
    draw_sunflower(bg, 340, 190, 1.0)
    draw_sunflower(bg, 255, 145, 0.95)
    draw_sunflower(bg, 315, 140, 1.05)

    # 9. Tulip Patch (bottom-left)
    tulip_colors = ["#ef4444", "#a855f7", "#f43f5e", "#ec4899", "#ef4444"]
    t_coords = [
        (-260, -170), (-220, -160), (-180, -175),
        (-280, -210), (-240, -205), (-200, -215), (-160, -200)
    ]
    for idx, (tx, ty) in enumerate(t_coords):
        draw_tulip(bg, tx, ty, color=tulip_colors[idx % len(tulip_colors)], size=1.0)

    # 10. Daisy Meadow (bottom-right)
    d_coords = [
        (190, -160), (230, -145), (270, -155), (310, -140),
        (210, -200), (250, -195), (290, -205), (330, -190), (360, -165)
    ]
    for dx, dy in d_coords:
        draw_daisy(bg, dx, dy, size=1.0)


# ==============================================================================
# MAIN SIMULATION CLASS
# ==============================================================================
class GardenSimulation:
    def __init__(self):
        # Set up Window & Screen
        self.screen = turtle.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.title("Shelly's Garden Tour 🐢 (Python Turtle)")
        self.screen.bgcolor("#5b933d")
        self.screen.tracer(0, 0)  # Smooth instant rendering

        # Turtles
        self.bg_turtle = turtle.Turtle()
        self.trail_turtle = turtle.Turtle()
        self.trail_turtle.hideturtle()
        self.trail_turtle.speed(0)
        self.trail_turtle.penup()

        self.hud_turtle = turtle.Turtle()
        self.hud_turtle.hideturtle()
        self.hud_turtle.speed(0)
        self.hud_turtle.penup()

        # Shelly (The Hero Turtle)
        self.shelly = turtle.Turtle()
        self.shelly.shape("turtle")
        self.shelly.shapesize(1.8, 1.8, 2.5)
        self.shelly.fillcolor("#34d399")   # Fresh jade green shell
        self.shelly.pencolor("#065f46")   # Dark forest outline
        self.shelly.speed(0)
        self.shelly.penup()
        self.shelly.goto(0, -60)
        self.shelly.setheading(90)

        # State Variables
        self.is_running = True
        self.mode = "AUTO"  # "AUTO" or "MANUAL"
        self.current_activity = "Warming up on the lawn and looking around..."
        self.current_emoji = "🌿"
        self.status_detail = "Auto-exploring landmarks"

        # Autonomous Navigation State
        self.current_target_index = 0
        self.target_pos = LANDMARKS[0]["pos"]
        self.pause_timer = 0  # When reaching a spot, Shelly pauses to enjoy it
        self.wiggle_counter = 0

        # Movement tracking
        self.last_footprint_pos = self.shelly.position()
        self.footprint_counter = 0

        # Click navigation target (for manual click-to-walk)
        self.click_target = None

        # Build Background
        render_entire_garden(self.bg_turtle)
        self.screen.update()

        # Bindings
        self.setup_controls()

        # Update initial HUD
        self.update_hud()
        self.screen.update()

    def setup_controls(self):
        """Register keyboard and mouse event listeners."""
        self.screen.listen()
        # Mode Toggle
        self.screen.onkey(self.toggle_mode, "space")
        # Movement
        self.screen.onkey(self.move_forward, "Up")
        self.screen.onkey(self.move_forward, "w")
        self.screen.onkey(self.move_forward, "W")
        self.screen.onkey(self.move_backward, "Down")
        self.screen.onkey(self.move_backward, "s")
        self.screen.onkey(self.move_backward, "S")
        self.screen.onkey(self.turn_left, "Left")
        self.screen.onkey(self.turn_left, "a")
        self.screen.onkey(self.turn_left, "A")
        self.screen.onkey(self.turn_right, "Right")
        self.screen.onkey(self.turn_right, "d")
        self.screen.onkey(self.turn_right, "D")
        # Utility keys
        self.screen.onkey(self.clear_trails, "c")
        self.screen.onkey(self.clear_trails, "C")
        self.screen.onkey(self.exit_game, "Escape")
        self.screen.onkey(self.exit_game, "q")
        self.screen.onkey(self.exit_game, "Q")
        # Mouse Click
        self.screen.onscreenclick(self.handle_click)

    def toggle_mode(self):
        """Toggle between Auto-Wander and Manual Control."""
        if self.mode == "AUTO":
            self.mode = "MANUAL"
            self.click_target = None
            self.current_activity = "Under manual control! Use Arrow Keys, WASD, or Click anywhere."
            self.current_emoji = "🎮"
        else:
            self.mode = "AUTO"
            self.click_target = None
            self.pick_next_destination()
        self.update_hud()

    def handle_click(self, x, y):
        """Direct Shelly to walk towards a clicked spot."""
        # Check boundary bounds
        clamped_x = max(-400, min(400, x))
        clamped_y = max(-300, min(240, y))
        self.click_target = (clamped_x, clamped_y)
        self.mode = "MANUAL"
        self.current_activity = f"Walking over to investigate clicked spot ({int(x)}, {int(y)})"
        self.current_emoji = "🐾"
        self.update_hud()

    def move_forward(self):
        """Move turtle forward manually."""
        if self.mode != "MANUAL":
            self.mode = "MANUAL"
        self.click_target = None
        self.shelly.forward(12)
        self.constrain_bounds()
        self.leave_footprint()
        self.check_nearby_landmarks()
        self.update_hud()

    def move_backward(self):
        """Move turtle backward manually."""
        if self.mode != "MANUAL":
            self.mode = "MANUAL"
        self.click_target = None
        self.shelly.backward(10)
        self.constrain_bounds()
        self.leave_footprint()
        self.check_nearby_landmarks()
        self.update_hud()

    def turn_left(self):
        """Turn turtle left."""
        self.shelly.left(15)

    def turn_right(self):
        """Turn turtle right."""
        self.shelly.right(15)

    def clear_trails(self):
        """Erase footprints on the grass."""
        self.trail_turtle.clear()

    def exit_game(self):
        """Cleanly exit the program."""
        self.is_running = False
        try:
            self.screen.bye()
        except Exception:
            pass

    def constrain_bounds(self):
        """Prevent Shelly from crawling out of the fenced garden boundaries."""
        x, y = self.shelly.position()
        min_x, max_x = -400, 400
        min_y, max_y = -310, 245
        new_x = max(min_x, min(max_x, x))
        new_y = max(min_y, min(max_y, y))
        if new_x != x or new_y != y:
            self.shelly.goto(new_x, new_y)

    def leave_footprint(self):
        """Leave tiny whimsical footprints along the grass."""
        cur_pos = self.shelly.position()
        dist = math.hypot(cur_pos[0] - self.last_footprint_pos[0], cur_pos[1] - self.last_footprint_pos[1])
        if dist >= 18:
            self.last_footprint_pos = cur_pos
            self.footprint_counter += 1

            # Alternate left & right paw offset
            heading_rad = math.radians(self.shelly.heading())
            offset_side = 6 if (self.footprint_counter % 2 == 0) else -6
            px = cur_pos[0] + math.cos(heading_rad + math.pi / 2) * offset_side
            py = cur_pos[1] + math.sin(heading_rad + math.pi / 2) * offset_side

            self.trail_turtle.penup()
            self.trail_turtle.goto(px, py)
            # Cute small earthy dot
            self.trail_turtle.dot(3.5, "#466e2c")

    def check_nearby_landmarks(self):
        """Detect if Shelly is currently near any landmark."""
        sx, sy = self.shelly.position()
        for lm in LANDMARKS:
            lx, ly = lm["pos"]
            dist = math.hypot(sx - lx, sy - ly)
            if dist <= lm["radius"]:
                self.current_activity = lm["text"]
                self.current_emoji = lm["emoji"]
                return
        if self.mode == "MANUAL" and not self.click_target:
            self.current_activity = "Happily strolling through the green grass"
            self.current_emoji = "🌿"

    def pick_next_destination(self):
        """Pick the next landmark to explore in Auto mode."""
        # Choose a different landmark
        options = [i for i in range(len(LANDMARKS)) if i != self.current_target_index]
        self.current_target_index = random.choice(options)
        lm = LANDMARKS[self.current_target_index]

        # Add minor natural offset so Shelly doesn't hit the exact same pixel
        ox = random.randint(-20, 20)
        oy = random.randint(-20, 20)
        self.target_pos = (lm["pos"][0] + ox, lm["pos"][1] + oy)
        self.current_activity = f"Heading over to explore the {lm['name']}..."
        self.current_emoji = "🐾"

    def update_hud(self):
        """Draw the elegant HUD status banner at the top of the window."""
        self.hud_turtle.clear()

        # Banner Background card
        banner_x = -SCREEN_WIDTH // 2 + 20
        banner_y = SCREEN_HEIGHT // 2 - 15
        banner_w = SCREEN_WIDTH - 40
        banner_h = 60

        draw_rectangle(self.hud_turtle, banner_x, banner_y, banner_w, banner_h,
                       "#1e293b", "#0f172a")

        # Top line: Mode & Current Activity
        self.hud_turtle.penup()
        self.hud_turtle.goto(banner_x + 15, banner_y - 26)
        self.hud_turtle.pencolor("#f8fafc")

        mode_badge = "[AUTO-WANDER]" if self.mode == "AUTO" else "[MANUAL CONTROL]"
        badge_color = "#38bdf8" if self.mode == "AUTO" else "#fbbf24"

        # Draw Mode tag
        self.hud_turtle.pencolor(badge_color)
        self.hud_turtle.write(mode_badge, align="left", font=("Segoe UI", 11, "bold"))

        # Draw Activity Text
        self.hud_turtle.goto(banner_x + 165, banner_y - 26)
        self.hud_turtle.pencolor("#f8fafc")
        activity_str = f"{self.current_emoji}  {self.current_activity}"
        self.hud_turtle.write(activity_str, align="left", font=("Segoe UI", 11, "normal"))

        # Bottom line: Controls Help
        self.hud_turtle.goto(banner_x + 15, banner_y - 48)
        self.hud_turtle.pencolor("#94a3b8")
        help_text = "Controls: [Space] Toggle Auto/Manual  |  [WASD / Arrows] Walk  |  [Left Click] Go to point  |  [C] Clear Trails  |  [Esc] Quit"
        self.hud_turtle.write(help_text, align="left", font=("Segoe UI", 9, "normal"))

    def step(self):
        """Simulation tick update called every frame."""
        if not self.is_running:
            return

        if self.mode == "AUTO":
            self.step_auto_wander()
        elif self.mode == "MANUAL" and self.click_target:
            self.step_click_walk()

        self.screen.update()
        # Schedule next tick
        self.screen.ontimer(self.step, FPS_MS)

    def step_click_walk(self):
        """Move towards the user's clicked destination."""
        tx, ty = self.click_target
        sx, sy = self.shelly.position()
        dist = math.hypot(tx - sx, ty - sy)

        if dist < 6:
            # Reached clicked spot
            self.click_target = None
            self.check_nearby_landmarks()
            self.update_hud()
            return

        # Turn gradually towards target
        desired_angle = math.degrees(math.atan2(ty - sy, tx - sx)) % 360
        current_angle = self.shelly.heading() % 360
        angle_diff = (desired_angle - current_angle + 180) % 360 - 180

        turn_speed = min(12, abs(angle_diff))
        if angle_diff > 0:
            self.shelly.left(turn_speed)
        elif angle_diff < 0:
            self.shelly.right(turn_speed)

        # Move forward
        step_len = min(WALK_SPEED, dist)
        self.shelly.forward(step_len)
        self.constrain_bounds()
        self.leave_footprint()

    def step_auto_wander(self):
        """Autonomous state machine: wander, turn, arrive, enjoy landmark."""
        if self.pause_timer > 0:
            self.pause_timer -= 1
            # Gentle cute wiggle while enjoying landmark
            self.wiggle_counter += 1
            wiggle_offset = math.sin(self.wiggle_counter * 0.3) * 1.5
            self.shelly.setheading(self.shelly.heading() + wiggle_offset)
            if self.pause_timer == 0:
                self.pick_next_destination()
                self.update_hud()
            return

        # Navigate towards current target
        tx, ty = self.target_pos
        sx, sy = self.shelly.position()
        dist = math.hypot(tx - sx, ty - sy)

        if dist < 16:
            # Arrived at destination!
            lm = LANDMARKS[self.current_target_index]
            self.current_activity = lm["text"]
            self.current_emoji = lm["emoji"]
            self.update_hud()
            self.pause_timer = 90  # Pause for ~2.5 seconds to interact/enjoy
            return

        # Smooth steering towards target
        desired_angle = math.degrees(math.atan2(ty - sy, tx - sx)) % 360
        current_angle = self.shelly.heading() % 360
        angle_diff = (desired_angle - current_angle + 180) % 360 - 180

        # Turn smoothly
        turn_speed = min(8, abs(angle_diff))
        if angle_diff > 0:
            self.shelly.left(turn_speed)
        elif angle_diff < 0:
            self.shelly.right(turn_speed)

        # Walk forward
        self.shelly.forward(WALK_SPEED)
        self.constrain_bounds()
        self.leave_footprint()


# ==============================================================================
# ENTRY POINT
# ==============================================================================
def main():
    sim = GardenSimulation()
    sim.step()
    turtle.mainloop()


if __name__ == "__main__":
    main()
