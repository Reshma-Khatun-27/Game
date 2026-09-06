"""
================================================================================
          🚚 STREET BITES: GOURMET FOOD TRUCK TYCOON & DRIVE 🍔
                     Python Turtle Interactive Experience
================================================================================
Controls:
    - [1] - [6]       : Cook & Serve Menu Items:
                        [1] 🍔 Classic Gourmet Burger ($8.50)
                        [2] 🌮 Spicy Street Taco      ($6.00)
                        [3] 🍕 Cheesy Pizza Slice     ($5.50)
                        [4] 🍟 Crispy Golden Fries    ($4.00)
                        [5] 🥤 Iced Boba Tea          ($4.50)
                        [6] 🍦 Swirl Soft Ice Cream   ($3.50)
    - [C]             : Customize Truck Paint Theme (4 Vibrant Styles)
    - [N]             : Toggle Night / Neon Underglow & Headlights Mode
    - [H]             : Honk Musical Horn (La Cucaracha notes! 🎵)
    - [D]             : Toggle Drive / Park Mode (Moving road & exhaust)
    - [Space]         : Chef Sizzle Special (Grill burst & sparkle tip)
    - [R]             : Reset Day & Start Fresh Shift
    - [Left Click]    : Tap anywhere for Confetti & Sparkles!
    - [Q] / [Escape]  : Quit Game
================================================================================
"""

import turtle
import time
import math
import random
import os

# ------------------------------------------------------------------------------
# Screen & World Dimensions
# ------------------------------------------------------------------------------
SCREEN_WIDTH = 980
SCREEN_HEIGHT = 740
FPS = 60
FRAME_DELAY = int(1000 / FPS)

# ------------------------------------------------------------------------------
# Menu & Recipe Items
# ------------------------------------------------------------------------------
MENU_ITEMS = [
    {"id": 1, "name": "Gourmet Burger", "price": 8.50, "icon": "🍔", "color": "#f59e0b"},
    {"id": 2, "name": "Spicy Street Taco", "price": 6.00, "icon": "🌮", "color": "#ef4444"},
    {"id": 3, "name": "Cheesy Pizza Slice", "price": 5.50, "icon": "🍕", "color": "#f97316"},
    {"id": 4, "name": "Crispy French Fries", "price": 4.00, "icon": "🍟", "color": "#eab308"},
    {"id": 5, "name": "Iced Boba Milk Tea", "price": 4.50, "icon": "🥤", "color": "#06b6d4"},
    {"id": 6, "name": "Swirl Ice Cream Cone", "price": 3.50, "icon": "🍦", "color": "#ec4899"},
]

# ------------------------------------------------------------------------------
# Color Palettes & Themes
# ------------------------------------------------------------------------------
THEMES = [
    {
        "name": "Vintage Mint & Cream",
        "primary": "#0d9488",       # Teal 600
        "primary_dark": "#115e59",  # Teal 800
        "primary_light": "#14b8a6", # Teal 500
        "secondary": "#fef08a",     # Yellow 200 (Cream)
        "accent": "#f43f5e",        # Rose 500
        "awning_1": "#0d9488",
        "awning_2": "#ffffff",
        "neon": "#2dd4bf",
        "underglow": "#14b8a6",
    },
    {
        "name": "Sunset Fiesta Orange",
        "primary": "#ea580c",       # Orange 600
        "primary_dark": "#9a3412",  # Orange 800
        "primary_light": "#fb923c", # Orange 400
        "secondary": "#fde047",     # Yellow 300
        "accent": "#dc2626",        # Red 600
        "awning_1": "#ea580c",
        "awning_2": "#fde047",
        "neon": "#fbbf24",
        "underglow": "#f97316",
    },
    {
        "name": "Midnight Cyber Neon",
        "primary": "#4c1d95",       # Violet 900
        "primary_dark": "#2e1065",  # Violet 950
        "primary_light": "#7c3aed", # Violet 600
        "secondary": "#06b6d4",     # Cyan 500
        "accent": "#f43f5e",        # Rose 500
        "awning_1": "#7c3aed",
        "awning_2": "#06b6d4",
        "neon": "#ec4899",
        "underglow": "#a855f7",
    },
    {
        "name": "Sweet Strawberry Pastel",
        "primary": "#f472b6",       # Pink 400
        "primary_dark": "#db2777",  # Pink 600
        "primary_light": "#fbcfe8", # Pink 200
        "secondary": "#a7f3d0",     # Emerald 200 (Mint)
        "accent": "#818cf8",        # Indigo 400
        "awning_1": "#f472b6",
        "awning_2": "#ffffff",
        "neon": "#f472b6",
        "underglow": "#f472b6",
    },
]

# Customer Characters presets
CUSTOMER_TYPES = [
    {"name": "Skater Sam", "body": "#3b82f6", "hair": "#78350f", "skin": "#ffdfc4", "hat": "#ef4444"},
    {"name": "Foodie Fiona", "body": "#ec4899", "hair": "#1f2937", "skin": "#fcd34d", "hat": None},
    {"name": "Chef Charlie", "body": "#10b981", "hair": "#f59e0b", "skin": "#ffedd5", "hat": "#ffffff"},
    {"name": "Gamer Gary", "body": "#8b5cf6", "hair": "#374151", "skin": "#fed7aa", "hat": "#06b6d4"},
    {"name": "Yoga Yasmine", "body": "#f97316", "hair": "#451a03", "skin": "#d97706", "hat": None},
    {"name": "Professor Pete", "body": "#64748b", "hair": "#94a3b8", "skin": "#ffdfc4", "hat": "#1e293b"},
]

# ------------------------------------------------------------------------------
# Geometry & Turtle Drawing Helpers
# ------------------------------------------------------------------------------
def jump(t, x, y):
    """Move turtle without drawing lines."""
    t.penup()
    t.goto(x, y)

def draw_rect(t, x, y, width, height, fill_color=None, outline_color=None, outline_width=1):
    """Draw a rectangle starting from bottom-left corner (x, y)."""
    jump(t, x, y)
    t.setheading(0)
    if outline_color:
        t.pencolor(outline_color)
        t.pensize(outline_width)
    else:
        t.pencolor(fill_color if fill_color else "#000000")
        t.pensize(1)
        
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
        
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
        
    if fill_color:
        t.end_fill()

def draw_rounded_rect(t, x, y, width, height, radius, fill_color=None, outline_color=None, outline_width=1):
    """Draw a rectangle with rounded corners starting from (x + radius, y)."""
    jump(t, x + radius, y)
    t.setheading(0)
    if outline_color:
        t.pencolor(outline_color)
        t.pensize(outline_width)
    else:
        t.pencolor(fill_color if fill_color else "#000000")
        t.pensize(1)
        
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
        
    t.forward(width - 2 * radius)
    t.circle(radius, 90)
    t.forward(height - 2 * radius)
    t.circle(radius, 90)
    t.forward(width - 2 * radius)
    t.circle(radius, 90)
    t.forward(height - 2 * radius)
    t.circle(radius, 90)
    
    if fill_color:
        t.end_fill()

def draw_circle(t, x, y, radius, fill_color=None, outline_color=None, outline_width=1):
    """Draw a circle centered at (x, y)."""
    jump(t, x, y - radius)
    t.setheading(0)
    if outline_color:
        t.pencolor(outline_color)
        t.pensize(outline_width)
    else:
        t.pencolor(fill_color if fill_color else "#000000")
        t.pensize(1)
        
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
        
    t.circle(radius)
    
    if fill_color:
        t.end_fill()

def draw_polygon(t, points, fill_color=None, outline_color=None, outline_width=1):
    """Draw a closed polygon from list of (x, y) tuples."""
    if not points:
        return
    jump(t, points[0][0], points[0][1])
    if outline_color:
        t.pencolor(outline_color)
        t.pensize(outline_width)
    else:
        t.pencolor(fill_color if fill_color else "#000000")
        t.pensize(1)
        
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
        
    for p in points[1:]:
        t.goto(p[0], p[1])
    t.goto(points[0][0], points[0][1])
    
    if fill_color:
        t.end_fill()


# ------------------------------------------------------------------------------
# Food Truck Game & Simulation Class
# ------------------------------------------------------------------------------
class FoodTruckSimulation:
    def __init__(self):
        # Setup Main Turtle Window
        self.screen = turtle.Screen()
        self.screen.title("🚚 STREET BITES: GOURMET FOOD TRUCK TYCOON 🍔")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor("#090d16")
        self.screen.tracer(0)
        
        # Dedicated Turtle Layers
        self.t_bg = turtle.Turtle()
        self.t_truck = turtle.Turtle()
        self.t_glow = turtle.Turtle()
        self.t_customer = turtle.Turtle()
        self.t_particles = turtle.Turtle()
        self.t_ui = turtle.Turtle()
        
        for t in [self.t_bg, self.t_truck, self.t_glow, self.t_customer, self.t_particles, self.t_ui]:
            t.hideturtle()
            t.speed(0)
            t.penup()
            
        # State Variables
        self.theme_idx = 0
        self.night_mode = True
        self.driving_mode = False
        self.road_scroll_offset = 0.0
        self.truck_bounce_y = 0.0
        self.wheel_rotation = 0.0
        
        # Tycoon Gameplay State
        self.cash = 45.00
        self.day = 1
        self.orders_served = 0
        self.rating = 5.0
        self.combo_streak = 0
        self.combo_timer = 0.0
        self.feedback_msg = "Welcome to Chef's Street Food Truck! Press [1-6] to serve customers!"
        self.feedback_color = "#38bdf8"
        self.feedback_timer = 3.0
        
        # Customer Queue
        self.customer = None
        self.customer_x = -450
        self.customer_target_x = 100 # In front of serving window
        self.customer_state = "walking_in" # "walking_in", "waiting_order", "happy_leaving", "sad_leaving"
        self.customer_patience = 1.0       # 1.0 down to 0.0
        self.customer_order = None
        self.customer_profile = None
        self.spawn_new_customer()
        
        # Dynamic Particles (Steam, Sizzle Sparks, Horn Notes, Confetti)
        self.particles = []
        self.fairy_lights_phase = 0.0
        self.exhaust_timer = 0.0
        
        # Register Key & Mouse Events
        self.bind_controls()
        
        # Initial Render of Static Layers
        self.redraw_environment()
        self.redraw_truck()
        self.redraw_night_glow()
        
        # Start Master Game Loop
        self.is_running = True
        self.last_time = time.time()
        self.game_loop()
        
    def bind_controls(self):
        """Bind keyboard shortcuts and mouse clicks."""
        self.screen.listen()
        
        # Serving Menu Keys (1 through 6)
        for i in range(1, 7):
            self.screen.onkey(lambda item_id=i: self.serve_order(item_id), str(i))
            
        # Features & Mode Keys
        self.screen.onkey(self.cycle_theme, "c")
        self.screen.onkey(self.cycle_theme, "C")
        self.screen.onkey(self.toggle_night_mode, "n")
        self.screen.onkey(self.toggle_night_mode, "N")
        self.screen.onkey(self.honk_horn, "h")
        self.screen.onkey(self.honk_horn, "H")
        self.screen.onkey(self.toggle_drive_mode, "d")
        self.screen.onkey(self.toggle_drive_mode, "D")
        self.screen.onkey(self.chef_sizzle_special, "space")
        self.screen.onkey(self.reset_day, "r")
        self.screen.onkey(self.reset_day, "R")
        self.screen.onkey(self.quit_app, "q")
        self.screen.onkey(self.quit_app, "Q")
        self.screen.onkey(self.quit_app, "Escape")
        
        # Mouse Interaction
        self.screen.onscreenclick(self.on_mouse_click)
        
    def get_current_theme(self):
        return THEMES[self.theme_idx % len(THEMES)]

    # --------------------------------------------------------------------------
    # Environment & Scenery Drawing
    # --------------------------------------------------------------------------
    def redraw_environment(self):
        """Draw background sky, distant skyline, sidewalk, and road."""
        t = self.t_bg
        t.clear()
        
        # 1. Sky Gradient
        if self.night_mode:
            # Twilight / Deep Midnight Sky
            sky_colors = ["#090d16", "#0f172a", "#1e1b4b", "#311042", "#4a044e"]
        else:
            # Golden Sunset / Warm Afternoon Sky
            sky_colors = ["#0284c7", "#38bdf8", "#fed7aa", "#fba779", "#f43f5e"]
            
        band_h = 90
        for idx, col in enumerate(sky_colors):
            y_pos = 370 - (idx * band_h)
            draw_rect(t, -500, y_pos - band_h, 1000, band_h + 2, fill_color=col)
            
        # Distant Twinkling Stars (if night)
        if self.night_mode:
            random.seed(42) # Consistent star positions
            for _ in range(45):
                sx = random.randint(-480, 480)
                sy = random.randint(120, 360)
                sz = random.uniform(1.0, 2.5)
                draw_circle(t, sx, sy, sz, fill_color="#ffffff")
            random.seed()
            
            # Glowing Crescent Moon
            draw_circle(t, 380, 290, 32, fill_color="#fef08a")
            draw_circle(t, 368, 298, 28, fill_color="#0f172a")
        else:
            # Warm Glowing Sun
            draw_circle(t, 370, 260, 45, fill_color="#fed7aa")
            draw_circle(t, 370, 260, 36, fill_color="#fef08a")

        # 2. Distant City Skyline Silhouettes
        skyline_col = "#090d16" if self.night_mode else "#2e1065"
        window_col = "#fef08a" if self.night_mode else "#fed7aa"
        
        building_widths = [60, 45, 75, 50, 80, 55, 70, 90, 60, 85, 65, 95, 70, 80]
        cur_x = -490
        random.seed(101)
        for bw in building_widths:
            bh = random.randint(120, 240)
            draw_rect(t, cur_x, 20, bw, bh, fill_color=skyline_col)
            
            # Rooftop antennas or spires
            if random.random() > 0.4:
                spire_x = cur_x + bw // 2
                draw_rect(t, spire_x - 2, 20 + bh, 4, 25, fill_color=skyline_col)
                draw_circle(t, spire_x, 20 + bh + 25, 3, fill_color="#ef4444" if self.night_mode else "#fbbf24")
                
            # Illuminated Windows
            if self.night_mode:
                for wy in range(40, 20 + bh - 15, 22):
                    for wx in range(cur_x + 8, cur_x + bw - 8, 14):
                        if random.random() > 0.45:
                            draw_rect(t, wx, wy, 6, 9, fill_color=window_col)
            cur_x += bw + random.randint(4, 12)
        random.seed()

        # 3. Sidewalk / Pavement Plaza
        draw_rect(t, -500, -80, 1000, 100, fill_color="#334155", outline_color="#1e293b", outline_width=2)
        # Sidewalk Cobblestone / Paver Tiles
        for px in range(-500, 500, 50):
            jump(t, px, -80)
            t.pencolor("#475569")
            t.pensize(2)
            t.pendown()
            t.goto(px, 20)
            t.penup()
        draw_rect(t, -500, -84, 1000, 6, fill_color="#64748b") # Curb Edge

        # 4. Asphalt Road
        draw_rect(t, -500, -370, 1000, 290, fill_color="#0f172a")
        
        # 5. Street Lamp on Right
        lamp_x = 410
        # Lamp pole
        draw_rect(t, lamp_x - 4, -80, 8, 320, fill_color="#1e293b", outline_color="#0f172a")
        # Lamp curved arm & fixture
        draw_rect(t, lamp_x - 30, 230, 34, 10, fill_color="#1e293b")
        draw_rounded_rect(t, lamp_x - 42, 220, 24, 14, 4, fill_color="#334155")
        # Lamp bulb
        draw_circle(t, lamp_x - 30, 220, 9, fill_color="#fef08a")
        
        # 6. Bistro String Lights across top
        wire_points = []
        for x in range(-450, 460, 20):
            # Drooping catenary curve
            y = 280 - 25 * math.sin((x + 450) / 900 * math.pi)
            wire_points.append((x, y))
        jump(t, wire_points[0][0], wire_points[0][1])
        t.pencolor("#475569")
        t.pensize(2)
        t.pendown()
        for pt in wire_points[1:]:
            t.goto(pt[0], pt[1])
        t.penup()

    # --------------------------------------------------------------------------
    # Food Truck Vector Drawing
    # --------------------------------------------------------------------------
    def redraw_truck(self):
        """Draw the entire high-detail food truck."""
        t = self.t_truck
        t.clear()
        
        theme = self.get_current_theme()
        base_x = -240
        base_y = -190 + self.truck_bounce_y
        
        # ----------------------------------------------------------------------
        # A. Truck Undercarriage Shadow & Exhaust
        # ----------------------------------------------------------------------
        draw_rounded_rect(t, base_x - 20, base_y - 30, 480, 36, 16, fill_color="#020617")
        
        # Exhaust pipe
        draw_rect(t, base_x - 32, base_y + 12, 22, 10, fill_color="#475569", outline_color="#1e293b")
        
        # ----------------------------------------------------------------------
        # B. Main Truck Chassis & Body
        # ----------------------------------------------------------------------
        # Main Body (Rear & Middle Kitchen)
        body_w = 420
        body_h = 240
        draw_rounded_rect(t, base_x, base_y, body_w, body_h, 24, 
                          fill_color=theme["primary"], outline_color=theme["primary_dark"], outline_width=3)
        
        # Dual-Tone Lower Accent Stripe
        stripe_h = 60
        draw_rounded_rect(t, base_x, base_y, body_w, stripe_h, 14, 
                          fill_color=theme["secondary"], outline_color=theme["primary_dark"], outline_width=2)
        
        # Thin Divider Trim Strip (Glossy Chrome)
        draw_rect(t, base_x, base_y + stripe_h, body_w, 6, fill_color="#f8fafc", outline_color="#cbd5e1")
        
        # Front Cab Nose (Curved aerodynamic front)
        cab_points = [
            (base_x + body_w - 20, base_y),
            (base_x + body_w + 65, base_y + 5),
            (base_x + body_w + 70, base_y + 70),
            (base_x + body_w + 45, base_y + 150),
            (base_x + body_w - 10, base_y + 200),
            (base_x + body_w - 20, base_y + 200),
        ]
        draw_polygon(t, cab_points, fill_color=theme["primary"], outline_color=theme["primary_dark"], outline_width=2)
        
        # Cab Lower Bumper & Grille
        draw_rounded_rect(t, base_x + body_w + 35, base_y + 10, 38, 48, 8, 
                          fill_color="#334155", outline_color="#1e293b", outline_width=2)
        # Chrome Grille Slats
        for gy in range(int(base_y) + 18, int(base_y) + 54, 10):
            draw_rect(t, base_x + body_w + 38, gy, 32, 4, fill_color="#e2e8f0")
            
        # Front Headlight (Round Vintage Chrome Bezel)
        hl_x = base_x + body_w + 52
        hl_y = base_y + 75
        draw_circle(t, hl_x, hl_y, 14, fill_color="#cbd5e1", outline_color="#475569", outline_width=2)
        draw_circle(t, hl_x, hl_y, 10, fill_color="#fef08a" if self.night_mode else "#ffffff")
        
        # Rear Vintage Taillight
        draw_rounded_rect(t, base_x - 6, base_y + 40, 10, 24, 4, fill_color="#ef4444", outline_color="#991b1b")
        draw_rounded_rect(t, base_x - 6, base_y + 68, 10, 14, 3, fill_color="#f59e0b", outline_color="#b45309")
        
        # Front Heavy Chrome Bumper
        draw_rounded_rect(t, base_x + body_w + 50, base_y - 4, 30, 20, 6, 
                          fill_color="#e2e8f0", outline_color="#94a3b8", outline_width=2)
        # Rear Bumper
        draw_rounded_rect(t, base_x - 14, base_y - 4, 20, 20, 6, 
                          fill_color="#e2e8f0", outline_color="#94a3b8", outline_width=2)

        # ----------------------------------------------------------------------
        # C. Driver Windshield & Cab Window
        # ----------------------------------------------------------------------
        windshield_points = [
            (base_x + body_w - 5, base_y + 130),
            (base_x + body_w + 32, base_y + 130),
            (base_x + body_w + 24, base_y + 185),
            (base_x + body_w - 5, base_y + 195),
        ]
        draw_polygon(t, windshield_points, fill_color="#38bdf8", outline_color="#0284c7", outline_width=2)
        # Windshield Glass Highlight Shimmer
        jump(t, base_x + body_w + 8, base_y + 140)
        t.pencolor("#e0f2fe")
        t.pensize(3)
        t.pendown()
        t.goto(base_x + body_w + 20, base_y + 180)
        t.penup()
        
        # Chef Cap in Driver Seat (Cute Silhouette)
        draw_circle(t, base_x + body_w + 6, base_y + 155, 8, fill_color="#ffffff")
        draw_rect(t, base_x + body_w + 2, base_y + 145, 12, 6, fill_color="#ffffff")
        
        # Side Mirror
        draw_rounded_rect(t, base_x + body_w + 38, base_y + 150, 12, 22, 4, 
                          fill_color="#1e293b", outline_color="#cbd5e1", outline_width=2)
        draw_rect(t, base_x + body_w + 28, base_y + 158, 10, 4, fill_color="#1e293b")

        # ----------------------------------------------------------------------
        # D. Large Serving Window & Kitchen Interior
        # ----------------------------------------------------------------------
        win_x = base_x + 60
        win_y = base_y + 65
        win_w = 230
        win_h = 135
        
        # Outer Window Frame
        draw_rounded_rect(t, win_x - 6, win_y - 6, win_w + 12, win_h + 12, 10, 
                          fill_color="#1e293b", outline_color="#0f172a", outline_width=2)
        # Warm Illuminated Kitchen Interior
        draw_rect(t, win_x, win_y, win_w, win_h, fill_color="#451a03")
        
        # Kitchen Backwall Tile Pattern
        for tx in range(int(win_x), int(win_x + win_w), 20):
            for ty in range(int(win_y) + 35, int(win_y + win_h), 16):
                draw_rect(t, tx, ty, 18, 14, fill_color="#78350f" if (tx+ty)%40==0 else "#92400e")
                
        # Kitchen Stainless Steel Serving Counter
        draw_rect(t, win_x, win_y, win_w, 35, fill_color="#94a3b8", outline_color="#64748b")
        draw_rect(t, win_x, win_y + 32, win_w, 5, fill_color="#f1f5f9") # Countertop gloss
        
        # Sizzling Grill on Counter (Left side)
        draw_rect(t, win_x + 12, win_y + 14, 65, 20, fill_color="#18181b", outline_color="#27272a")
        # Glowing Grill Burners
        for gx in range(int(win_x) + 18, int(win_x) + 70, 14):
            draw_circle(t, gx, win_y + 24, 4, fill_color="#f97316")
            draw_circle(t, gx, win_y + 24, 2, fill_color="#fef08a")
            
        # Burger Patties / Buns on Grill
        draw_rounded_rect(t, win_x + 16, win_y + 26, 18, 8, 3, fill_color="#713f12")
        draw_rounded_rect(t, win_x + 40, win_y + 26, 18, 8, 3, fill_color="#ca8a04")

        # Cash Register / POS Touchscreen (Right side)
        draw_rect(t, win_x + win_w - 55, win_y + 14, 38, 24, fill_color="#1e293b", outline_color="#334155")
        draw_rect(t, win_x + win_w - 52, win_y + 20, 32, 16, fill_color="#0284c7")
        draw_rect(t, win_x + win_w - 40, win_y + 6, 12, 8, fill_color="#475569")
        
        # Hanging Order Tickets on Top Window Rail
        draw_rect(t, win_x, win_y + win_h - 10, win_w, 8, fill_color="#334155")
        ticket_colors = ["#fef08a", "#fbcfe8", "#bbf7d0", "#bae6fd"]
        for idx, tk_x in enumerate(range(int(win_x) + 35, int(win_x + win_w) - 30, 42)):
            draw_rect(t, tk_x, win_y + win_h - 26, 24, 20, fill_color=ticket_colors[idx % len(ticket_colors)])

        # Serving Shelf / Outer Counter Ledge
        draw_rounded_rect(t, win_x - 12, win_y - 2, win_w + 24, 12, 4, 
                          fill_color="#cbd5e1", outline_color="#64748b", outline_width=2)
        # Condiment Squeeze Bottles (Ketchup & Mustard)
        draw_rounded_rect(t, win_x + win_w - 20, win_y + 6, 8, 16, 2, fill_color="#ef4444") # Ketchup
        draw_rounded_rect(t, win_x + win_w - 9, win_y + 6, 8, 16, 2, fill_color="#eab308")  # Mustard

        # ----------------------------------------------------------------------
        # E. Striped Canopy Awning over Serving Window
        # ----------------------------------------------------------------------
        awn_x = win_x - 24
        awn_y = win_y + win_h - 12
        awn_w = win_w + 48
        awn_h = 55
        
        # Awning Main Slanted Shading Box
        stripe_count = 10
        stripe_w = awn_w / stripe_count
        
        for s in range(stripe_count):
            sx = awn_x + s * stripe_w
            col = theme["awning_1"] if s % 2 == 0 else theme["awning_2"]
            
            # 3D Perspective Slanted Stripe Polygon
            p_stripe = [
                (sx, awn_y + awn_h),
                (sx + stripe_w, awn_y + awn_h),
                (sx + stripe_w - 4, awn_y),
                (sx - 4, awn_y),
            ]
            draw_polygon(t, p_stripe, fill_color=col, outline_color="#334155", outline_width=1)
            
            # Scalloped Frill / Fringe at Bottom
            draw_circle(t, sx + stripe_w / 2 - 2, awn_y, stripe_w / 2 + 0.5, fill_color=col, outline_color="#334155")
            
        # Awning Metal Support Arms
        jump(t, awn_x, awn_y + 8)
        t.pencolor("#64748b")
        t.pensize(3)
        t.pendown()
        t.goto(awn_x - 10, awn_y - 35)
        t.penup()
        jump(t, awn_x + awn_w - 8, awn_y + 8)
        t.pendown()
        t.goto(awn_x + awn_w + 2, awn_y - 35)
        t.penup()

        # ----------------------------------------------------------------------
        # F. Rooftop Exhaust Chimney & Signage
        # ----------------------------------------------------------------------
        # Kitchen Roof Exhaust Hood / Vent
        vent_x = base_x + 95
        vent_y = base_y + body_h
        draw_rect(t, vent_x - 4, vent_y, 28, 22, fill_color="#64748b", outline_color="#334155", outline_width=2)
        draw_rounded_rect(t, vent_x - 12, vent_y + 20, 44, 12, 4, fill_color="#94a3b8", outline_color="#475569")
        
        # Rooftop Marquee Billboard / Giant Neon Sign
        sign_x = base_x + 155
        sign_y = base_y + body_h + 6
        sign_w = 210
        sign_h = 58
        
        # Sign Sturdy Steel Brackets
        draw_rect(t, sign_x + 25, vent_y, 10, 16, fill_color="#334155")
        draw_rect(t, sign_x + sign_w - 35, vent_y, 10, 16, fill_color="#334155")
        
        # Sign Lightbox Frame
        draw_rounded_rect(t, sign_x, sign_y, sign_w, sign_h, 14, 
                          fill_color="#0f172a", outline_color=theme["neon"], outline_width=3)
        
        # Sign Inner Glow Plate
        draw_rounded_rect(t, sign_x + 6, sign_y + 6, sign_w - 12, sign_h - 12, 10, 
                          fill_color="#1e1b4b" if self.night_mode else "#fef08a")
        
        # 3D Burger Icon on Left of Sign
        b_cx = sign_x + 35
        b_cy = sign_y + sign_h / 2
        # Bun Top
        draw_circle(t, b_cx, b_cy + 2, 14, fill_color="#ca8a04")
        draw_rect(t, b_cx - 14, b_cy - 10, 28, 12, fill_color="#1e1b4b" if self.night_mode else "#fef08a")
        # Lettuce & Tomato
        draw_rect(t, b_cx - 14, b_cy + 1, 28, 4, fill_color="#22c55e")
        draw_rect(t, b_cx - 12, b_cy - 3, 24, 4, fill_color="#ef4444")
        # Patty
        draw_rounded_rect(t, b_cx - 13, b_cy - 8, 26, 6, 2, fill_color="#713f12")
        # Bun Bottom
        draw_rounded_rect(t, b_cx - 13, b_cy - 14, 26, 6, 2, fill_color="#ca8a04")
        
        # Text on Sign: "STREET BITES"
        jump(t, sign_x + 120, sign_y + 15)
        t.pencolor(theme["neon"] if self.night_mode else "#b45309")
        t.write("STREET BITES", align="center", font=("Impact", 19, "bold"))

        # ----------------------------------------------------------------------
        # G. Sidewalk Chalkboard Menu Stand
        # ----------------------------------------------------------------------
        menu_x = base_x - 140
        menu_y = -85
        menu_w = 90
        menu_h = 135
        
        # A-Frame Wooden Legs
        draw_polygon(t, [(menu_x - 8, menu_y), (menu_x + 8, menu_y + menu_h + 10), (menu_x + 18, menu_y + menu_h + 10), (menu_x + 2, menu_y)], fill_color="#78350f")
        draw_polygon(t, [(menu_x + menu_w + 8, menu_y), (menu_x + menu_w - 8, menu_y + menu_h + 10), (menu_x + menu_w - 18, menu_y + menu_h + 10), (menu_x + menu_w - 2, menu_y)], fill_color="#78350f")
        
        # Chalkboard Frame & Slate
        draw_rounded_rect(t, menu_x, menu_y + 12, menu_w, menu_h, 8, fill_color="#5c2b0e", outline_color="#3e1a05", outline_width=2)
        draw_rect(t, menu_x + 6, menu_y + 18, menu_w - 12, menu_h - 12, fill_color="#0f172a")
        
        # Menu Header
        jump(t, menu_x + menu_w / 2, menu_y + menu_h - 6)
        t.pencolor("#fef08a")
        t.write("~ MENU ~", align="center", font=("Arial", 9, "bold"))
        
        # Compact Menu Lines
        dish_previews = ["1:Burger $8.5", "2:Taco $6.0", "3:Pizza $5.5", "4:Fries $4.0", "5:Boba $4.5", "6:IceCream $3.5"]
        for idx, line in enumerate(dish_previews):
            jump(t, menu_x + menu_w / 2, menu_y + menu_h - 24 - idx * 16)
            t.pencolor("#f8fafc" if idx % 2 == 0 else "#38bdf8")
            t.write(line, align="center", font=("Arial", 8, "normal"))

        # ----------------------------------------------------------------------
        # H. Heavy Duty Wheels & Hubcaps
        # ----------------------------------------------------------------------
        wheel_radius = 42
        wheel_positions = [base_x + 80, base_x + body_w - 30]
        
        for wx in wheel_positions:
            wy = base_y
            
            # Wheel Arch Cutout in Body
            draw_circle(t, wx, wy + 8, wheel_radius + 10, fill_color="#020617")
            
            # Rubber Tire
            draw_circle(t, wx, wy, wheel_radius, fill_color="#18181b", outline_color="#27272a", outline_width=3)
            # Tire Tread Ring
            draw_circle(t, wx, wy, wheel_radius - 6, outline_color="#3f3f46", outline_width=2)
            
            # Steel Rim
            draw_circle(t, wx, wy, wheel_radius - 14, fill_color="#94a3b8", outline_color="#64748b", outline_width=2)
            # Chrome Center Hubcap
            draw_circle(t, wx, wy, 14, fill_color="#e2e8f0", outline_color="#475569", outline_width=2)
            
            # Rotating Lug Nuts / Spokes
            for spoke_angle in range(0, 360, 60):
                rad = math.radians(spoke_angle + self.wheel_rotation)
                lx = wx + math.cos(rad) * 20
                ly = wy + math.sin(rad) * 20
                draw_circle(t, lx, ly, 3, fill_color="#334155")
                
        # ----------------------------------------------------------------------
        # I. Hanging Bistro Party Lights on Truck Roof
        # ----------------------------------------------------------------------
        bulb_colors = ["#fbbf24", "#ef4444", "#38bdf8", "#a855f7", "#22c55e", "#ec4899"]
        for idx, bx in enumerate(range(int(base_x) + 10, int(base_x + body_w) + 30, 40)):
            by = base_y + body_h - 4
            # Tiny cord
            draw_rect(t, bx - 1, by - 8, 2, 8, fill_color="#1e293b")
            # Glowing Bulb
            bcol = bulb_colors[(idx + int(self.fairy_lights_phase)) % len(bulb_colors)]
            draw_circle(t, bx, by - 12, 5, fill_color=bcol if self.night_mode else "#fed7aa")

    # --------------------------------------------------------------------------
    # Dynamic Glow / Night Lighting Layer
    # --------------------------------------------------------------------------
    def redraw_night_glow(self):
        """Draw illuminated headlight beam cones, underglow, and neon halo."""
        t = self.t_glow
        t.clear()
        
        if not self.night_mode:
            return
            
        theme = self.get_current_theme()
        base_x = -240
        base_y = -190 + self.truck_bounce_y
        body_w = 420
        
        # 1. Vibrant Underglow Neon Light Strip
        underglow_points = [
            (base_x + 20, base_y - 20),
            (base_x + body_w + 10, base_y - 20),
            (base_x + body_w + 35, base_y - 36),
            (base_x - 5, base_y - 36),
        ]
        draw_polygon(t, underglow_points, fill_color=theme["underglow"])
        
        # 2. Glowing Headlight Beam Cone Lines
        hl_x = base_x + body_w + 52
        hl_y = base_y + 75
        
        # Headlight projection lines
        t.pencolor("#fef08a")
        for dy in range(-80, 50, 20):
            jump(t, hl_x, hl_y)
            t.pensize(2)
            t.pendown()
            t.goto(hl_x + 260, hl_y + dy)
            t.penup()

    # --------------------------------------------------------------------------
    # Customer Character & Thought Bubble Rendering
    # --------------------------------------------------------------------------
    def spawn_new_customer(self):
        """Spawn a random new hungry customer."""
        self.customer_profile = random.choice(CUSTOMER_TYPES)
        self.customer_order = random.choice(MENU_ITEMS)
        self.customer_x = -480
        self.customer_state = "walking_in"
        self.customer_patience = 1.0

    def update_and_draw_customer(self, dt):
        """Update customer animation and render."""
        t = self.t_customer
        t.clear()
        
        # Customer Physics / State Machine
        walk_speed = 175.0 * dt
        
        if self.customer_state == "walking_in":
            if self.customer_x < self.customer_target_x:
                self.customer_x += walk_speed
            else:
                self.customer_x = self.customer_target_x
                self.customer_state = "waiting_order"
                
        elif self.customer_state == "waiting_order":
            # Patience countdown
            self.customer_patience -= 0.045 * dt
            if self.customer_patience <= 0:
                self.customer_patience = 0
                self.customer_state = "sad_leaving"
                self.combo_streak = 0
                self.rating = max(1.0, round(self.rating - 0.2, 1))
                self.feedback_msg = f"{self.customer_profile['name']} got tired of waiting and left! (Sad)"
                self.feedback_color = "#ef4444"
                self.feedback_timer = 2.5
                
        elif self.customer_state in ["happy_leaving", "sad_leaving"]:
            self.customer_x += walk_speed * 1.3
            if self.customer_x > 490:
                # Customer exited screen, spawn next
                self.spawn_new_customer()

        # Render Customer Vector Figure
        cx = self.customer_x
        cy = -95
        prof = self.customer_profile
        if not prof:
            return
            
        # Walking Bobbing Motion
        bob = math.sin(time.time() * 12) * 5 if self.customer_state != "waiting_order" else 0
        cy += bob
        
        # Feet / Shoes
        draw_rounded_rect(t, cx - 14, cy, 12, 8, 3, fill_color="#1e293b")
        draw_rounded_rect(t, cx + 2, cy, 12, 8, 3, fill_color="#1e293b")
        
        # Legs / Pants
        draw_rect(t, cx - 12, cy + 6, 10, 24, fill_color="#334155")
        draw_rect(t, cx + 2, cy + 6, 10, 24, fill_color="#334155")
        
        # Torso / Outfit
        draw_rounded_rect(t, cx - 18, cy + 28, 36, 42, 8, fill_color=prof["body"], outline_color="#0f172a", outline_width=2)
        
        # Head / Neck / Face
        draw_circle(t, cx, cy + 86, 16, fill_color=prof["skin"], outline_color="#0f172a", outline_width=2)
        
        # Eyes
        if self.customer_state == "sad_leaving":
            # Sad squinting eyes
            jump(t, cx - 7, cy + 85)
            t.pencolor("#0f172a")
            t.pensize(2)
            t.pendown()
            t.goto(cx - 3, cy + 88)
            t.penup()
            jump(t, cx + 3, cy + 88)
            t.pendown()
            t.goto(cx + 7, cy + 85)
            t.penup()
        else:
            # Happy round eyes
            draw_circle(t, cx - 5, cy + 87, 2.5, fill_color="#0f172a")
            draw_circle(t, cx + 5, cy + 87, 2.5, fill_color="#0f172a")
            # Cute smile
            jump(t, cx - 6, cy + 78)
            t.pencolor("#ef4444")
            t.pensize(2)
            t.pendown()
            t.circle(6, 180)
            t.penup()
            
        # Hair
        draw_circle(t, cx, cy + 96, 14, fill_color=prof["hair"])
        
        # Hat (if any)
        if prof.get("hat"):
            draw_rounded_rect(t, cx - 20, cy + 94, 40, 10, 3, fill_color=prof["hat"])
            draw_circle(t, cx, cy + 98, 12, fill_color=prof["hat"])

        # ----------------------------------------------------------------------
        # Order Speech Bubble & Patience Bar
        # ----------------------------------------------------------------------
        if self.customer_state == "waiting_order" and self.customer_order:
            bx = cx - 55
            by = cy + 120
            bw = 110
            bh = 65
            
            # Speech Bubble Tail
            draw_polygon(t, [(cx, by), (cx - 10, by + 12), (cx + 10, by + 12)], fill_color="#ffffff", outline_color="#94a3b8", outline_width=1)
            # Speech Bubble Main Rounded Box
            draw_rounded_rect(t, bx, by + 10, bw, bh, 14, fill_color="#ffffff", outline_color="#64748b", outline_width=2)
            
            # Requested Food Icon & Number Hotkey Hint
            item = self.customer_order
            jump(t, cx, by + 42)
            t.pencolor("#0f172a")
            t.write(f"{item['icon']} {item['name'][:7]}", align="center", font=("Arial", 11, "bold"))
            
            jump(t, cx, by + 24)
            t.pencolor("#64748b")
            t.write(f"Press [{item['id']}] (${item['price']:.2f})", align="center", font=("Arial", 8, "bold"))
            
            # Patience Timer Bar
            bar_w = 80
            bar_h = 6
            bar_x = cx - bar_w / 2
            bar_y = by + 14
            draw_rounded_rect(t, bar_x, bar_y, bar_w, bar_h, 3, fill_color="#e2e8f0")
            
            p_color = "#22c55e" if self.customer_patience > 0.5 else "#f59e0b" if self.customer_patience > 0.25 else "#ef4444"
            fill_w = max(4, bar_w * self.customer_patience)
            draw_rounded_rect(t, bar_x, bar_y, fill_w, bar_h, 3, fill_color=p_color)

    # --------------------------------------------------------------------------
    # Particle System (Steam, Sizzle, Horn Notes, Confetti)
    # --------------------------------------------------------------------------
    def add_particle(self, p_type, x, y, vx=0, vy=0, color="#ffffff", size=5, life=1.0, text=None):
        self.particles.append({
            "type": p_type,
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "color": color,
            "size": size,
            "life": life,
            "max_life": life,
            "text": text,
        })

    def update_and_draw_particles(self, dt):
        """Update and draw all dynamic particles."""
        t = self.t_particles
        t.clear()
        
        # 1. Continual Kitchen Chimney Smoke / Steam Puff
        self.exhaust_timer += dt
        if self.exhaust_timer > 0.12:
            self.exhaust_timer = 0
            base_x = -240
            base_y = -190 + self.truck_bounce_y
            vent_x = base_x + 109
            vent_y = base_y + 240 + 30
            self.add_particle("smoke", vent_x + random.uniform(-4, 4), vent_y, 
                              vx=random.uniform(-0.6, 0.4) if not self.driving_mode else random.uniform(-4.0, -1.5),
                              vy=random.uniform(1.2, 2.5),
                              color="#f1f5f9", size=random.uniform(7, 14), life=random.uniform(1.2, 2.0))
            
            # Driving road exhaust
            if self.driving_mode:
                pipe_x = base_x - 30
                pipe_y = base_y + 15
                self.add_particle("smoke", pipe_x, pipe_y, 
                                  vx=random.uniform(-5.0, -2.5), vy=random.uniform(0.5, 1.8),
                                  color="#94a3b8", size=random.uniform(8, 16), life=0.9)
                                  
        # 2. Update existing particles
        surviving_particles = []
        for p in self.particles:
            p["life"] -= dt
            if p["life"] <= 0:
                continue
                
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            
            # Fade or grow based on type
            life_ratio = p["life"] / p["max_life"]
            
            if p["type"] == "smoke":
                p["size"] += 0.35
                draw_circle(t, p["x"], p["y"], p["size"], fill_color=p["color"])
                
            elif p["type"] == "spark":
                p["vy"] -= 0.15 # gravity
                draw_circle(t, p["x"], p["y"], max(1.5, p["size"] * life_ratio), fill_color=p["color"])
                
            elif p["type"] == "note":
                jump(t, p["x"], p["y"])
                t.pencolor(p["color"])
                t.write(p["text"] or "♪", align="center", font=("Arial", int(14 * life_ratio + 6), "bold"))
                
            elif p["type"] == "text":
                jump(t, p["x"], p["y"])
                t.pencolor(p["color"])
                t.write(p["text"], align="center", font=("Arial", 14, "bold"))
                
            surviving_particles.append(p)
            
        self.particles = surviving_particles

    # --------------------------------------------------------------------------
    # HUD & UI Overlay Rendering
    # --------------------------------------------------------------------------
    def redraw_ui(self):
        """Draw modern game HUD, earnings, rating, combo, and hotkeys guide."""
        t = self.t_ui
        t.clear()
        
        # 1. Top HUD Glassmorphism Bar
        draw_rounded_rect(t, -460, 310, 920, 48, 12, fill_color="#0f172a", outline_color="#334155", outline_width=2)
        
        # Daily Cash
        jump(t, -430, 324)
        t.pencolor("#22c55e")
        t.write(f"💵 Cash: ${self.cash:.2f}", align="left", font=("Arial", 14, "bold"))
        
        # Orders Served
        jump(t, -220, 324)
        t.pencolor("#38bdf8")
        t.write(f"🍽️ Orders: {self.orders_served}", align="left", font=("Arial", 13, "bold"))
        
        # Customer Rating Stars
        jump(t, -30, 324)
        t.pencolor("#fbbf24")
        stars_str = "⭐" * max(1, int(round(self.rating)))
        t.write(f"Rating: {self.rating:.1f} {stars_str}", align="left", font=("Arial", 13, "bold"))
        
        # Combo Streak Badge
        if self.combo_streak >= 2:
            jump(t, 220, 324)
            t.pencolor("#ec4899")
            t.write(f"🔥 STREAK x{self.combo_streak}!", align="left", font=("Arial", 13, "bold"))
            
        # Day / Theme indicator
        jump(t, 430, 324)
        t.pencolor("#a855f7")
        mode_tag = "🚀 CRUISE" if self.driving_mode else "🌙 NIGHT" if self.night_mode else "☀️ DAY"
        t.write(f"[{mode_tag}]", align="right", font=("Arial", 12, "bold"))

        # 2. Feedback Notification Toast (if active)
        if self.feedback_timer > 0:
            draw_rounded_rect(t, -320, 255, 640, 36, 8, fill_color="#0f172a", outline_color=self.feedback_color, outline_width=2)
            jump(t, 0, 263)
            t.pencolor(self.feedback_color)
            t.write(self.feedback_msg, align="center", font=("Arial", 12, "bold"))

        # 3. Bottom Hotkey Help Banner
        draw_rounded_rect(t, -480, -355, 960, 42, 8, fill_color="#020617", outline_color="#1e293b", outline_width=2)
        jump(t, 0, -342)
        t.pencolor("#94a3b8")
        t.write("[1-6] Serve Dish  |  [C] Paint Theme  |  [N] Night Mode  |  [H] Honk Horn  |  [D] Cruise  |  [Space] Sizzle  |  [R] Reset",
                align="center", font=("Arial", 10, "bold"))

    # --------------------------------------------------------------------------
    # Interactive Actions & Hotkey Handlers
    # --------------------------------------------------------------------------
    def serve_order(self, item_id):
        """Cook and serve food item to waiting customer."""
        if not self.customer_profile or self.customer_state != "waiting_order":
            self.feedback_msg = "No customer ready at the counter! Wait for someone to step up!"
            self.feedback_color = "#f59e0b"
            self.feedback_timer = 2.0
            return
            
        target_item = self.customer_order
        served_item = next((item for item in MENU_ITEMS if item["id"] == item_id), None)
        
        if not served_item:
            return
            
        if served_item["id"] == target_item["id"]:
            # CORRECT ORDER!
            tip = 2.00 if self.customer_patience > 0.6 else 0.50
            total_earned = served_item["price"] + tip
            self.cash += total_earned
            self.orders_served += 1
            self.combo_streak += 1
            self.rating = min(5.0, round(self.rating + 0.1, 1))
            
            # Sizzle Spark Particles & Floating Earning Text
            win_x = -240 + 60
            win_y = -190 + 65
            for _ in range(16):
                self.add_particle("spark", win_x + 40, win_y + 40, 
                                  vx=random.uniform(-3, 3), vy=random.uniform(2, 6),
                                  color=random.choice(["#fbbf24", "#f97316", "#22c55e", "#fef08a"]),
                                  size=random.uniform(3, 6), life=0.8)
                                  
            self.add_particle("text", self.customer_x, win_y + 110, vy=1.2, color="#22c55e", text=f"+${total_earned:.2f} :)", life=1.5)
            
            self.customer_state = "happy_leaving"
            self.feedback_msg = f"Served delicious {served_item['name']}! (+${total_earned:.2f} with tip ⭐)"
            self.feedback_color = "#22c55e"
            self.feedback_timer = 2.5
        else:
            # WRONG ORDER!
            self.combo_streak = 0
            self.rating = max(1.0, round(self.rating - 0.1, 1))
            self.feedback_msg = f"Oops! {self.customer_profile['name']} wanted {target_item['name']}, not {served_item['name']}!"
            self.feedback_color = "#ef4444"
            self.feedback_timer = 2.5
            self.add_particle("text", self.customer_x, -95 + 110, vy=1.0, color="#ef4444", text="Wrong Order!", life=1.5)

    def cycle_theme(self):
        """Cycle through paint and awning themes."""
        self.theme_idx = (self.theme_idx + 1) % len(THEMES)
        curr = self.get_current_theme()
        self.feedback_msg = f"Switched Paint Theme to: {curr['name']}!"
        self.feedback_color = curr["neon"]
        self.feedback_timer = 2.5
        self.redraw_truck()
        self.redraw_night_glow()

    def toggle_night_mode(self):
        """Toggle Day/Night mode and glowing neon effects."""
        self.night_mode = not self.night_mode
        state_str = "Night Mode (Neons & Headlights ON)" if self.night_mode else "Day Mode (Sunshine & Warm Sky)"
        self.feedback_msg = f"Lighting Mode: {state_str}"
        self.feedback_color = "#fbbf24"
        self.feedback_timer = 2.5
        self.redraw_environment()
        self.redraw_truck()
        self.redraw_night_glow()

    def honk_horn(self):
        """Honk truck horn and spawn musical note particles."""
        self.feedback_msg = "HONK HONK! *La Cucaracha* 🎵🚚"
        self.feedback_color = "#f43f5e"
        self.feedback_timer = 2.0
        
        base_x = -240
        base_y = -190
        grille_x = base_x + 420 + 55
        grille_y = base_y + 80
        
        music_notes = ["♪", "♫", "♬", "♩", "🚚💨", "✨"]
        for _ in range(8):
            self.add_particle("note", grille_x + random.uniform(-10, 20), grille_y + random.uniform(-10, 20),
                              vx=random.uniform(2.0, 5.5), vy=random.uniform(-1.0, 3.5),
                              color=random.choice(["#f43f5e", "#fbbf24", "#06b6d4", "#a855f7"]),
                              life=1.4, text=random.choice(music_notes))

    def toggle_drive_mode(self):
        """Toggle drive cruise mode with road parallax & engine bounce."""
        self.driving_mode = not self.driving_mode
        state = "CRUISING DOWN HIGHWAY 🛣️" if self.driving_mode else "PARKED & READY TO SERVE 🅿️"
        self.feedback_msg = f"Truck Status: {state}"
        self.feedback_color = "#38bdf8"
        self.feedback_timer = 2.5

    def chef_sizzle_special(self):
        """Chef grill sizzle special trick for bonus tip particles."""
        self.cash += 1.00
        self.feedback_msg = "CHEF SIZZLE SPECIAL! Grill blazing hot! (+$1.00 Tip)"
        self.feedback_color = "#f97316"
        self.feedback_timer = 2.0
        
        win_x = -240 + 60
        win_y = -190 + 65
        for _ in range(25):
            self.add_particle("spark", win_x + 40 + random.uniform(-20, 20), win_y + 35,
                              vx=random.uniform(-4, 4), vy=random.uniform(3, 8),
                              color=random.choice(["#f97316", "#ef4444", "#fef08a", "#fbbf24"]),
                              size=random.uniform(4, 7), life=0.9)

    def reset_day(self):
        """Reset score and start fresh day."""
        self.cash = 45.00
        self.orders_served = 0
        self.rating = 5.0
        self.combo_streak = 0
        self.spawn_new_customer()
        self.feedback_msg = "New Shift Started! Let's cook up some magic!"
        self.feedback_color = "#38bdf8"
        self.feedback_timer = 3.0

    def on_mouse_click(self, x, y):
        """Interactive click anywhere on screen for confetti & sparkle effects."""
        colors = ["#f43f5e", "#fbbf24", "#38bdf8", "#4ade80", "#a855f7", "#ffffff"]
        for _ in range(15):
            self.add_particle("spark", x, y,
                              vx=random.uniform(-4, 4), vy=random.uniform(-2, 5),
                              color=random.choice(colors), size=random.uniform(3, 6), life=0.8)

    def quit_app(self):
        """Quit the simulation cleanly."""
        self.is_running = False
        try:
            self.screen.bye()
        except turtle.Terminator:
            pass

    # --------------------------------------------------------------------------
    # Main Game & Animation Loop
    # --------------------------------------------------------------------------
    def game_loop(self):
        """Master 60 FPS update loop."""
        if not self.is_running:
            return
            
        now = time.time()
        dt = min(0.1, now - self.last_time)
        self.last_time = now
        
        # 1. Update Timer & Fairy Lights
        self.fairy_lights_phase = (self.fairy_lights_phase + dt * 3) % 6
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            
        # 2. Driving Animation Dynamics
        if self.driving_mode:
            self.wheel_rotation = (self.wheel_rotation - 720 * dt) % 360
            self.truck_bounce_y = math.sin(time.time() * 24) * 2.5
            self.redraw_truck()
            self.redraw_night_glow()
        else:
            if self.truck_bounce_y != 0.0:
                self.truck_bounce_y = 0.0
                self.redraw_truck()
                self.redraw_night_glow()
                
        # 3. Update Customer & Particles
        self.update_and_draw_customer(dt)
        self.update_and_draw_particles(dt)
        
        # 4. Update HUD
        self.redraw_ui()
        
        # 5. Flush frame to screen
        try:
            self.screen.update()
        except (turtle.Terminator, Exception):
            return
            
        # Schedule Next Frame
        if self.is_running:
            self.screen.ontimer(self.game_loop, FRAME_DELAY)


# ------------------------------------------------------------------------------
# Application Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = FoodTruckSimulation()
    turtle.mainloop()
