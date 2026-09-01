"""
================================================================================
                    NITRO RACER: SPORTS CAR HIGHWAY DRIVE
================================================================================
Controls:
    - Left / Right Arrow or A / D : Steer left / right
    - Up Arrow or W               : Accelerate (Throttle)
    - Down Arrow or S             : Brake / Reverse
    - Space or Shift              : NITRO TURBO BOOST 🔥
    - P                           : Pause / Resume game
    - R                           : Restart game after crash
    - Q / Escape                  : Quit game
================================================================================
"""

import turtle
import time
import random
import os
import math

# ------------------------------------------------------------------------------
# Game Configuration & Constants
# ------------------------------------------------------------------------------
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 760

ROAD_LEFT = -220
ROAD_RIGHT = 220
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT  # 440 px
LANE_CENTERS = [-165, -55, 55, 165]  # 4 Road Lanes

BASE_SPEED = 5.0
MAX_NORMAL_SPEED = 14.0
MAX_NITRO_SPEED = 22.0
ACCELERATION = 0.25
BRAKING = 0.4
FRICTION = 0.08
STEERING_SPEED = 7.5

FPS = 60
FRAME_DELAY = 1.0 / FPS

# Colors
BG_GRASS = "#064e3b"         # Dark Emerald roadside
ROAD_COLOR = "#0f172a"       # Deep slate asphalt
ROAD_BORDER = "#e2e8f0"      # White guardrail
LANE_MARKER = "#f8fafc"      # Crisp white dash
CURB_RED = "#ef4444"         # Red rumble strip
CURB_WHITE = "#ffffff"       # White rumble strip

PLAYER_CAR_COLOR = "#ef4444" # Crimson Red Supercar
PLAYER_ROOF_COLOR = "#0f172a"
PLAYER_WINDOW_COLOR = "#38bdf8"
NITRO_FLAME_COLOR = "#38bdf8"

TRAFFIC_COLORS = [
    ("#eab308", "#ca8a04"),  # Yellow taxi / sports
    ("#3b82f6", "#1d4ed8"),  # Blue coupe
    ("#a855f7", "#7e22ce"),  # Purple hypercar
    ("#10b981", "#047857"),  # Green muscle car
    ("#f97316", "#c2410c"),  # Orange racer
    ("#ec4899", "#be185d"),  # Pink roadster
    ("#64748b", "#334155")   # Silver sedan
]

COIN_COLOR = "#fbbf24"       # Gold coin
NITRO_PICKUP_COLOR = "#06b6d4"# Cyan nitro tank
SHIELD_COLOR = "#818cf8"     # Indigo shield
TEXT_COLOR = "#f8fafc"       # Slate 50
SUBTEXT_COLOR = "#94a3b8"    # Slate 400

HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "car_highscore.txt")

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def load_high_score():
    """Load high score from file."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            return 0
    return 0

def save_high_score(new_high):
    """Save high score to file."""
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(new_high))
    except IOError:
        pass


# ------------------------------------------------------------------------------
# Sports Car Game Class
# ------------------------------------------------------------------------------
class SportsCarGame:
    def __init__(self):
        # 1. Setup Screen
        self.win = turtle.Screen()
        self.win.title("Nitro Racer: Sports Car Driving | Python Turtle")
        self.win.bgcolor(BG_GRASS)
        self.win.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.win.tracer(0)

        # 2. Register Custom Vector Shapes
        self.register_shapes()

        # 3. Game State
        self.speed = BASE_SPEED
        self.distance = 0.0
        self.score = 0
        self.coins = 0
        self.high_score = load_high_score()
        self.nitro_fuel = 100.0  # 0 to 100%
        self.is_nitro_active = False
        self.has_shield = False
        self.is_paused = False
        self.is_game_over = False
        self.traffic_timer = 0
        self.item_timer = 0

        # Continuous Key State Tracking
        self.keys = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "nitro": False
        }

        # Track Collections
        self.lane_dashes = []
        self.curbs = []
        self.traffic_cars = []
        self.collectibles = []
        self.particles = []

        # 4. Build Environment & Entities
        self.draw_static_scenery()
        self.init_road_markings()
        self.init_player_car()
        self.init_hud()
        self.init_overlay()

        # 5. Bind Key Listeners
        self.setup_keybindings()

    # --------------------------------------------------------------------------
    # Custom Shapes Registration
    # --------------------------------------------------------------------------
    def register_shapes(self):
        """Registers sleek sports car and item vector shapes."""
        # Sleek Supercar Silhouette (Width ~28, Length ~56)
        car_points = (
            (-12, -26), (12, -26),     # Rear bumper
            (14, -20), (14, 12),       # Right side / rear fender
            (11, 22), (7, 27),         # Right front nose
            (0, 29),                   # Front hood tip
            (-7, 27), (-11, 22),       # Left front nose
            (-14, 12), (-14, -20)      # Left side / rear fender
        )
        self.win.register_shape("supercar", car_points)

        # Pickup Diamond Shape
        diamond = (
            (0, 12), (10, 0), (0, -12), (-10, 0)
        )
        self.win.register_shape("diamond", diamond)

    # --------------------------------------------------------------------------
    # Road Scenery & Animation Setup
    # --------------------------------------------------------------------------
    def draw_static_scenery(self):
        """Draws the asphalt highway bed and roadside borders."""
        bg = turtle.Turtle()
        bg.speed(0)
        bg.hideturtle()
        bg.penup()

        # Asphalt Road Rectangle
        bg.goto(ROAD_LEFT, SCREEN_HEIGHT // 2)
        bg.color(ROAD_COLOR, ROAD_COLOR)
        bg.begin_fill()
        for _ in range(2):
            bg.forward(ROAD_WIDTH)
            bg.right(90)
            bg.forward(SCREEN_HEIGHT)
            bg.right(90)
        bg.end_fill()

        # Road Outer Guardrails
        for x in [ROAD_LEFT, ROAD_RIGHT]:
            bg.goto(x, SCREEN_HEIGHT // 2)
            bg.color(ROAD_BORDER)
            bg.pensize(4)
            bg.pendown()
            bg.goto(x, -SCREEN_HEIGHT // 2)
            bg.penup()

    def init_road_markings(self):
        """Initializes animated lane dividers and rumble strip curbs."""
        # 3 Lane dividing lines (at x = -110, 0, 110)
        lane_x_positions = [-110, 0, 110]
        dash_spacing = 60
        num_dashes_per_lane = (SCREEN_HEIGHT // dash_spacing) + 3

        for lx in lane_x_positions:
            for i in range(num_dashes_per_lane):
                dash = turtle.Turtle()
                dash.speed(0)
                dash.shape("square")
                dash.shapesize(stretch_wid=1.4, stretch_len=0.25)
                dash.color(LANE_MARKER)
                dash.penup()
                y = (SCREEN_HEIGHT // 2) - (i * dash_spacing)
                dash.goto(lx, y)
                self.lane_dashes.append(dash)

        # Animated Curbs / Rumble strips on road edges
        curb_spacing = 35
        num_curbs = (SCREEN_HEIGHT // curb_spacing) + 2
        for side_x in [ROAD_LEFT - 6, ROAD_RIGHT + 6]:
            for i in range(num_curbs):
                curb = turtle.Turtle()
                curb.speed(0)
                curb.shape("square")
                curb.shapesize(stretch_wid=1.2, stretch_len=0.45)
                color = CURB_RED if i % 2 == 0 else CURB_WHITE
                curb.color(color)
                curb.penup()
                y = (SCREEN_HEIGHT // 2) - (i * curb_spacing)
                curb.goto(side_x, y)
                self.curbs.append((curb, i % 2 == 0))

    # --------------------------------------------------------------------------
    # Player Sports Car Setup
    # --------------------------------------------------------------------------
    def init_player_car(self):
        """Creates the player's sports car, roof, windshield, and headlights."""
        # 1. Main Car Body
        self.player = turtle.Turtle()
        self.player.speed(0)
        self.player.shape("supercar")
        self.player.color(PLAYER_CAR_COLOR)
        self.player.penup()
        self.player.goto(0, -220)

        # 2. Windshield / Cockpit
        self.player_cockpit = turtle.Turtle()
        self.player_cockpit.speed(0)
        self.player_cockpit.shape("square")
        self.player_cockpit.shapesize(stretch_wid=1.2, stretch_len=0.65)
        self.player_cockpit.color(PLAYER_WINDOW_COLOR)
        self.player_cockpit.penup()

        # 3. Roof & Spoiler
        self.player_roof = turtle.Turtle()
        self.player_roof.speed(0)
        self.player_roof.shape("square")
        self.player_roof.shapesize(stretch_wid=0.6, stretch_len=0.55)
        self.player_roof.color(PLAYER_ROOF_COLOR)
        self.player_roof.penup()

        # 4. Nitro Boost Exhaust Flame
        self.nitro_flame = turtle.Turtle()
        self.nitro_flame.speed(0)
        self.nitro_flame.shape("triangle")
        self.nitro_flame.shapesize(stretch_wid=0.7, stretch_len=1.2)
        self.nitro_flame.setheading(270)  # Point downward
        self.nitro_flame.color(NITRO_FLAME_COLOR)
        self.nitro_flame.penup()
        self.nitro_flame.hideturtle()

        # 5. Shield Bubble Aura
        self.shield_aura = turtle.Turtle()
        self.shield_aura.speed(0)
        self.shield_aura.shape("circle")
        self.shield_aura.shapesize(stretch_wid=3.2, stretch_len=2.2)
        self.shield_aura.color(SHIELD_COLOR)
        self.shield_aura.penup()
        self.shield_aura.hideturtle()

        self.sync_player_visuals()

    def sync_player_visuals(self):
        """Aligns child cockpit, roof, flame, and shield with the player's car."""
        px, py = self.player.xcor(), self.player.ycor()
        self.player_cockpit.goto(px, py + 2)
        self.player_roof.goto(px, py - 4)

        if self.is_nitro_active:
            self.nitro_flame.goto(px, py - 35)
            self.nitro_flame.showturtle()
        else:
            self.nitro_flame.hideturtle()

        if self.has_shield:
            self.shield_aura.goto(px, py)
            self.shield_aura.showturtle()
        else:
            self.shield_aura.hideturtle()

    # --------------------------------------------------------------------------
    # HUD / Dashboard
    # --------------------------------------------------------------------------
    def init_hud(self):
        """Creates on-screen heads up display."""
        self.hud_pen = turtle.Turtle()
        self.hud_pen.speed(0)
        self.hud_pen.penup()
        self.hud_pen.hideturtle()
        self.update_hud()

    def init_overlay(self):
        """Creates overlay pen for Game Over and Pause banner."""
        self.overlay_pen = turtle.Turtle()
        self.overlay_pen.speed(0)
        self.overlay_pen.penup()
        self.overlay_pen.hideturtle()

    def update_hud(self):
        """Draws dynamic speedometer, nitro bar, score, coins, and distance."""
        self.hud_pen.clear()

        mph = int(self.speed * 12.5)  # Realistic MPH conversion
        kmh = int(mph * 1.609)

        # Top Bar Background Panel
        self.hud_pen.goto(0, 330)
        self.hud_pen.color("#0284c7")
        self.hud_pen.write(
            f"🏎 SPEED: {mph} MPH ({kmh} KM/H)   ★ SCORE: {int(self.score)}   💰 COINS: {self.coins}   🏆 BEST: {self.high_score}",
            align="center",
            font=("Segoe UI", 13, "bold")
        )

        # Nitro Fuel Meter on Top Right
        nitro_bars = int(self.nitro_fuel // 10)
        bar_visual = "█" * nitro_bars + "░" * (10 - nitro_bars)
        flame_icon = "🔥 NITRO READY" if self.nitro_fuel >= 20 else "⚠️ LOW NITRO"
        nitro_color = "#38bdf8" if self.nitro_fuel >= 20 else "#f87171"

        self.hud_pen.goto(0, 305)
        self.hud_pen.color(nitro_color)
        shield_text = "   🛡 SHIELD ACTIVE!" if self.has_shield else ""
        self.hud_pen.write(
            f"BOOST [{bar_visual}] {int(self.nitro_fuel)}% - {flame_icon}{shield_text}",
            align="center",
            font=("Consolas", 11, "bold")
        )

    # --------------------------------------------------------------------------
    # Controls & Event Listeners
    # --------------------------------------------------------------------------
    def key_press_left(self): self.keys["left"] = True
    def key_release_left(self): self.keys["left"] = False

    def key_press_right(self): self.keys["right"] = True
    def key_release_right(self): self.keys["right"] = False

    def key_press_up(self): self.keys["up"] = True
    def key_release_up(self): self.keys["up"] = False

    def key_press_down(self): self.keys["down"] = True
    def key_release_down(self): self.keys["down"] = False

    def key_press_nitro(self): self.keys["nitro"] = True
    def key_release_nitro(self): self.keys["nitro"] = False

    def toggle_pause(self):
        """Pauses or resumes the game loop."""
        if self.is_game_over:
            return
        self.is_paused = not self.is_paused
        self.overlay_pen.clear()
        if self.is_paused:
            self.overlay_pen.goto(0, 40)
            self.overlay_pen.color("#facc15")
            self.overlay_pen.write("GAME PAUSED", align="center", font=("Segoe UI", 26, "bold"))
            self.overlay_pen.goto(0, 0)
            self.overlay_pen.color(SUBTEXT_COLOR)
            self.overlay_pen.write("Press Space or P to Resume", align="center", font=("Segoe UI", 14, "normal"))

    def setup_keybindings(self):
        """Binds responsive key press & release events."""
        self.win.listen()

        # Steering
        self.win.onkeypress(self.key_press_left, "Left")
        self.win.onkeyrelease(self.key_release_left, "Left")
        self.win.onkeypress(self.key_press_left, "a")
        self.win.onkeyrelease(self.key_release_left, "a")
        self.win.onkeypress(self.key_press_left, "A")
        self.win.onkeyrelease(self.key_release_left, "A")

        self.win.onkeypress(self.key_press_right, "Right")
        self.win.onkeyrelease(self.key_release_right, "Right")
        self.win.onkeypress(self.key_press_right, "d")
        self.win.onkeyrelease(self.key_release_right, "d")
        self.win.onkeypress(self.key_press_right, "D")
        self.win.onkeyrelease(self.key_release_right, "D")

        # Acceleration & Braking
        self.win.onkeypress(self.key_press_up, "Up")
        self.win.onkeyrelease(self.key_release_up, "Up")
        self.win.onkeypress(self.key_press_up, "w")
        self.win.onkeyrelease(self.key_release_up, "w")
        self.win.onkeypress(self.key_press_up, "W")
        self.win.onkeyrelease(self.key_release_up, "W")

        self.win.onkeypress(self.key_press_down, "Down")
        self.win.onkeyrelease(self.key_release_down, "Down")
        self.win.onkeypress(self.key_press_down, "s")
        self.win.onkeyrelease(self.key_release_down, "s")
        self.win.onkeypress(self.key_press_down, "S")
        self.win.onkeyrelease(self.key_release_down, "S")

        # Nitro
        self.win.onkeypress(self.key_press_nitro, "space")
        self.win.onkeyrelease(self.key_release_nitro, "space")
        self.win.onkeypress(self.key_press_nitro, "Shift_L")
        self.win.onkeyrelease(self.key_release_nitro, "Shift_L")
        self.win.onkeypress(self.key_press_nitro, "Shift_R")
        self.win.onkeyrelease(self.key_release_nitro, "Shift_R")

        # Menus
        self.win.onkeypress(self.toggle_pause, "p")
        self.win.onkeypress(self.toggle_pause, "P")
        self.win.onkeypress(self.restart_game, "r")
        self.win.onkeypress(self.restart_game, "R")
        self.win.onkeypress(self.quit_game, "Escape")
        self.win.onkeypress(self.quit_game, "q")
        self.win.onkeypress(self.quit_game, "Q")

    # --------------------------------------------------------------------------
    # Spawning Entities (Traffic, Coins, Powerups)
    # --------------------------------------------------------------------------
    def spawn_traffic(self):
        """Spawns an oncoming or cruising traffic car."""
        lane_x = random.choice(LANE_CENTERS)
        # Check if lane is currently blocked near top
        for car in self.traffic_cars:
            if abs(car["turtle"].xcor() - lane_x) < 25 and car["turtle"].ycor() > 260:
                return  # Avoid stacking cars directly on top of each other

        body_color, roof_color = random.choice(TRAFFIC_COLORS)

        # Traffic Car Body
        car_t = turtle.Turtle()
        car_t.speed(0)
        car_t.shape("supercar")
        car_t.color(body_color)
        car_t.penup()
        spawn_y = (SCREEN_HEIGHT // 2) + random.randint(30, 80)
        car_t.goto(lane_x, spawn_y)

        # Traffic Car Cockpit
        roof_t = turtle.Turtle()
        roof_t.speed(0)
        roof_t.shape("square")
        roof_t.shapesize(stretch_wid=1.0, stretch_len=0.55)
        roof_t.color(roof_color)
        roof_t.penup()
        roof_t.goto(lane_x, spawn_y - 2)

        speed_variation = random.uniform(2.5, 5.5)
        self.traffic_cars.append({
            "turtle": car_t,
            "roof": roof_t,
            "speed": speed_variation
        })

    def spawn_collectible(self):
        """Spawns coins, nitro canisters, or shield powerups."""
        lane_x = random.choice(LANE_CENTERS)
        spawn_y = (SCREEN_HEIGHT // 2) + 40

        # Roll type: 70% Coin, 20% Nitro, 10% Shield
        roll = random.random()
        item = turtle.Turtle()
        item.speed(0)
        item.penup()
        item.goto(lane_x, spawn_y)

        if roll < 0.70:
            kind = "coin"
            item.shape("circle")
            item.shapesize(0.7, 0.7)
            item.color(COIN_COLOR)
        elif roll < 0.90:
            kind = "nitro"
            item.shape("diamond")
            item.shapesize(0.8, 0.8)
            item.color(NITRO_PICKUP_COLOR)
        else:
            kind = "shield"
            item.shape("circle")
            item.shapesize(0.9, 0.9)
            item.color(SHIELD_COLOR)

        self.collectibles.append({
            "turtle": item,
            "type": kind
        })

    # --------------------------------------------------------------------------
    # Particle Explosion Effects
    # --------------------------------------------------------------------------
    def create_explosion(self, x, y, color="#f97316"):
        """Spawns an animated debris particle blast on impact."""
        for _ in range(16):
            p = turtle.Turtle()
            p.speed(0)
            p.shape("circle")
            p.shapesize(random.uniform(0.2, 0.5), random.uniform(0.2, 0.5))
            p.color(random.choice([color, "#ef4444", "#fbbf24", "#f8fafc"]))
            p.penup()
            p.goto(x, y)
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(3.0, 9.0)
            self.particles.append({
                "turtle": p,
                "vx": math.cos(angle) * spd,
                "vy": math.sin(angle) * spd,
                "life": random.randint(12, 24)
            })

    # --------------------------------------------------------------------------
    # Crash & Game Over
    # --------------------------------------------------------------------------
    def show_game_over(self, reason="CRASHED!"):
        """Displays arcade Game Over splash screen."""
        self.is_game_over = True
        self.create_explosion(self.player.xcor(), self.player.ycor())
        self.player.color("#475569")  # Wrecked dark grey

        # Save Highscore
        if int(self.score) > self.high_score:
            self.high_score = int(self.score)
            save_high_score(self.high_score)

        self.overlay_pen.clear()
        self.overlay_pen.goto(0, 70)
        self.overlay_pen.color("#ef4444")
        self.overlay_pen.write(f"💥 {reason}", align="center", font=("Segoe UI", 30, "bold"))

        self.overlay_pen.goto(0, 20)
        self.overlay_pen.color(TEXT_COLOR)
        self.overlay_pen.write(f"Final Score: {int(self.score)}   •   Coins: {self.coins}", align="center", font=("Segoe UI", 16, "bold"))

        self.overlay_pen.goto(0, -25)
        self.overlay_pen.color("#38bdf8")
        self.overlay_pen.write(f"Distance: {int(self.distance)} meters   •   Best: {self.high_score}", align="center", font=("Segoe UI", 14, "normal"))

        self.overlay_pen.goto(0, -75)
        self.overlay_pen.color(SUBTEXT_COLOR)
        self.overlay_pen.write("Press 'R' to Race Again   •   'Q' to Quit", align="center", font=("Segoe UI", 14, "bold"))

    def restart_game(self):
        """Cleans up board and restarts new race."""
        if not self.is_game_over:
            return

        self.overlay_pen.clear()

        # Clear Traffic
        for car in self.traffic_cars:
            car["turtle"].goto(1000, 1000)
            car["turtle"].hideturtle()
            car["roof"].goto(1000, 1000)
            car["roof"].hideturtle()
        self.traffic_cars.clear()

        # Clear Collectibles
        for item in self.collectibles:
            item["turtle"].goto(1000, 1000)
            item["turtle"].hideturtle()
        self.collectibles.clear()

        # Clear Particles
        for p in self.particles:
            p["turtle"].goto(1000, 1000)
            p["turtle"].hideturtle()
        self.particles.clear()

        # Reset Player
        self.player.goto(0, -220)
        self.player.color(PLAYER_CAR_COLOR)
        self.speed = BASE_SPEED
        self.distance = 0.0
        self.score = 0
        self.coins = 0
        self.nitro_fuel = 100.0
        self.has_shield = False
        self.is_nitro_active = False
        self.is_paused = False
        self.is_game_over = False
        self.traffic_timer = 0
        self.item_timer = 0

        self.sync_player_visuals()
        self.update_hud()

    def quit_game(self):
        """Closes window gracefully."""
        try:
            self.win.bye()
        except turtle.Terminator:
            pass

    # --------------------------------------------------------------------------
    # Main Loop
    # --------------------------------------------------------------------------
    def update_frame(self):
        """Executes one frame of physics and rendering."""
        if not self.is_paused and not self.is_game_over:
            # 1. Handle Nitro Boost & Speed Physics
            if self.keys["nitro"] and self.nitro_fuel > 2.0:
                self.is_nitro_active = True
                self.nitro_fuel = max(0.0, self.nitro_fuel - 0.75)
                self.speed = min(MAX_NITRO_SPEED, self.speed + ACCELERATION * 1.5)
            else:
                self.is_nitro_active = False
                # Slowly regenerate nitro when not boosting
                self.nitro_fuel = min(100.0, self.nitro_fuel + 0.06)

                # Standard Acceleration & Braking
                if self.keys["up"]:
                    self.speed = min(MAX_NORMAL_SPEED, self.speed + ACCELERATION)
                elif self.keys["down"]:
                    self.speed = max(BASE_SPEED * 0.6, self.speed - BRAKING)
                else:
                    # Natural deceleration to base cruise speed
                    if self.speed > BASE_SPEED:
                        self.speed = max(BASE_SPEED, self.speed - FRICTION)

            # 2. Player Steering
            px = self.player.xcor()
            if self.keys["left"]:
                px -= STEERING_SPEED
            if self.keys["right"]:
                px += STEERING_SPEED

            self.player.setx(px)
            self.sync_player_visuals()

            # 3. Guardrail / Road Boundary Collision Check
            if px < ROAD_LEFT + 18 or px > ROAD_RIGHT - 18:
                self.show_game_over("GUARDRAIL CRASH!")
                return

            # 4. Animate Road Markings & Curbs
            for dash in self.lane_dashes:
                dash.sety(dash.ycor() - self.speed)
                if dash.ycor() < -SCREEN_HEIGHT // 2:
                    dash.sety((SCREEN_HEIGHT // 2) + 20)

            for curb, is_red in self.curbs:
                curb.sety(curb.ycor() - self.speed)
                if curb.ycor() < -SCREEN_HEIGHT // 2:
                    curb.sety((SCREEN_HEIGHT // 2) + 20)

            # 5. Spawn Traffic & Collectibles
            self.traffic_timer += 1
            spawn_threshold = max(35, int(90 - (self.speed * 2.5)))
            if self.traffic_timer >= spawn_threshold:
                self.spawn_traffic()
                self.traffic_timer = 0

            self.item_timer += 1
            if self.item_timer >= 120:
                self.spawn_collectible()
                self.item_timer = 0

            # 6. Update Traffic Cars & Collisions
            for car in self.traffic_cars[:]:
                rel_dy = self.speed - car["speed"]
                car_y = car["turtle"].ycor() - rel_dy
                car_x = car["turtle"].xcor()

                car["turtle"].sety(car_y)
                car["roof"].sety(car_y - 2)

                # Player Collision Check (Bounding Box)
                if abs(px - car_x) < 24 and abs(self.player.ycor() - car_y) < 46:
                    if self.has_shield:
                        # Shield absorbs hit and destroys enemy car!
                        self.has_shield = False
                        self.create_explosion(car_x, car_y, "#38bdf8")
                        car["turtle"].goto(1000, 1000)
                        car["turtle"].hideturtle()
                        car["roof"].goto(1000, 1000)
                        car["roof"].hideturtle()
                        self.traffic_cars.remove(car)
                        self.score += 50
                        self.sync_player_visuals()
                        continue
                    else:
                        self.show_game_over("TRAFFIC COLLISION!")
                        break

                # Off-screen Removal
                if car_y < (-SCREEN_HEIGHT // 2) - 50:
                    car["turtle"].goto(1000, 1000)
                    car["turtle"].hideturtle()
                    car["roof"].goto(1000, 1000)
                    car["roof"].hideturtle()
                    self.traffic_cars.remove(car)
                    self.score += 15  # Overtake bonus!

            # 7. Update Collectibles & Pickups
            for item in self.collectibles[:]:
                item_y = item["turtle"].ycor() - self.speed
                item["turtle"].sety(item_y)

                # Pickup Collision Check
                if self.player.distance(item["turtle"]) < 28:
                    itype = item["type"]
                    if itype == "coin":
                        self.coins += 1
                        self.score += 30
                    elif itype == "nitro":
                        self.nitro_fuel = min(100.0, self.nitro_fuel + 45.0)
                        self.score += 20
                    elif itype == "shield":
                        self.has_shield = True
                        self.sync_player_visuals()
                        self.score += 25

                    item["turtle"].goto(1000, 1000)
                    item["turtle"].hideturtle()
                    self.collectibles.remove(item)
                    continue

                # Off-screen Removal
                if item_y < -SCREEN_HEIGHT // 2:
                    item["turtle"].goto(1000, 1000)
                    item["turtle"].hideturtle()
                    self.collectibles.remove(item)

            # 8. Update Particle Debris
            for p in self.particles[:]:
                p["turtle"].setx(p["turtle"].xcor() + p["vx"])
                p["turtle"].sety(p["turtle"].ycor() + p["vy"] - (self.speed * 0.5))
                p["life"] -= 1
                if p["life"] <= 0:
                    p["turtle"].goto(1000, 1000)
                    p["turtle"].hideturtle()
                    self.particles.remove(p)

            # 9. Distance & Score Tracking
            self.distance += (self.speed * 0.45)
            self.score += (self.speed * 0.08)
            self.update_hud()

    def run(self):
        """Executes the 60 FPS physics and rendering loop."""
        running = True
        while running:
            try:
                self.win.update()
                self.update_frame()
                time.sleep(FRAME_DELAY)
            except (turtle.Terminator, Exception):
                running = False
                break


# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    game = SportsCarGame()
    game.run()
