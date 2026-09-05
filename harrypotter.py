
"""
================================================================================
                    ⚡ HARRY POTTER - THE BOY WHO LIVED ⚡
                   Python Turtle Magical Art & Spell System
================================================================================
Controls:
    - [1] or [L]       : Cast 'LUMOS MAXIMA' (Radiant Golden Light)
    - [2] or [E]       : Cast 'EXPECTO PATRONUM' (Silver-Cyan Patronus Aura)
    - [3] or [X]       : Cast 'EXPELLIARMUS' (Scarlet Shockwave Beam)
    - [4] or [W]       : Cast 'WINGARDIUM LEVIOSA' (Golden Levitation Swirl)
    - [Space]          : Magic Surge (Random Spell Burst)
    - Left Click       : Aim & Shoot Magic Sparks from Wand Tip
    - [S]              : Toggle Golden Snitch Flying Animation
    - [R]              : Redraw / Reset Scene
    - [Q] / [Escape]   : Quit
================================================================================
"""
import turtle
import math
import random
import time

# ------------------------------------------------------------------------------
# Configuration & Color Palette
# ------------------------------------------------------------------------------
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 820

# Palette - Hogwarts & Character Colors
COLOR_BG_DARK = "#0a0b1a"       # Deep Midnight Blue
COLOR_BG_GRAD = "#131633"       # Upper Atmosphere
COLOR_GOLD = "#ffd700"          # Warm Bright Gold
COLOR_GRYFF_GOLD = "#eeba30"    # Gryffindor Gold
COLOR_GRYFF_RED = "#740001"     # Gryffindor Crimson
COLOR_GRYFF_DARKRED = "#4a0000" # Gryffindor Deep Wine
COLOR_ROBE_BLACK = "#15151e"    # Wizard Robe Dark
COLOR_ROBE_GRAY = "#282a36"     # Robe Highlights
COLOR_SKIN = "#ffdfc4"          # Skin Base
COLOR_SKIN_SHADOW = "#f0be9b"   # Skin Shading
COLOR_BLUSH = "#ffb0a0"         # Cheeks Blush
COLOR_HAIR_BLACK = "#10121a"    # Jet Black Hair
COLOR_HAIR_HIGHLIGHT = "#24293d"# Hair Soft Highlight
COLOR_EYE_GREEN = "#10b981"     # Bright Emerald Green
COLOR_EYE_DARK = "#064e3b"      # Deep Forest Pupil
COLOR_GLASSES = "#1f2421"       # Round Glass Frames
COLOR_SCAR = "#ef4444"          # Lightning Bolt Scar
COLOR_SCAR_GLOW = "#fca5a5"     # Scar Glow
COLOR_WAND_WOOD = "#5c3317"     # Holly Wand Brown
COLOR_WAND_TIP = "#8b5a2b"      # Wand Grip

# Global State
screen = None
t_bg = None
t_char = None
t_snitch = None
t_spells = None
t_ui = None
t_particles = None

snitch_animating = True
snitch_angle = 0.0
snitch_base_x = 240
snitch_base_y = 170

particles = []
active_spell_text = ""
spell_text_timer = 0
is_running = True

# ------------------------------------------------------------------------------
# Turtle Geometry & Drawing Utilities
# ------------------------------------------------------------------------------
def create_turtle(visible=False, speed=0):
    """Factory to create and configure a turtle instance."""
    t = turtle.Turtle()
    t.hideturtle()
    if visible:
        t.showturtle()
    t.speed(speed)
    t.penup()
    return t

def jump(t, x, y):
    """Move turtle to (x, y) without drawing."""
    t.penup()
    t.goto(x, y)

def draw_circle(t, x, y, radius, fill_color=None, outline_color=None, outline_width=1):
    """Draw a circle centered at (x, y). If fill_color is None, draws only outline."""
    jump(t, x, y - radius)
    t.setheading(0)
    if outline_color:
        t.pencolor(outline_color)
        t.pensize(outline_width)
    elif fill_color and fill_color != "none":
        t.pencolor(fill_color)
        t.pensize(1)
        
    if fill_color and fill_color != "none":
        t.fillcolor(fill_color)
        t.begin_fill()
        t.circle(radius)
        t.end_fill()
        if outline_color:
            t.pendown()
            t.circle(radius)
            t.penup()
    elif outline_color:
        t.pendown()
        t.circle(radius)
        t.penup()

def draw_ellipse(t, x, y, rx, ry, fill_color=None, outline_color=None, outline_width=1, angle=0):
    """Draw an ellipse centered at (x, y)."""
    rad_angle = math.radians(angle)
    steps = 48
    points = []
    for i in range(steps + 1):
        theta = 2 * math.pi * i / steps
        ex = rx * math.cos(theta)
        ey = ry * math.sin(theta)
        # Rotate by angle
        rx_rot = ex * math.cos(rad_angle) - ey * math.sin(rad_angle)
        ry_rot = ex * math.sin(rad_angle) + ey * math.cos(rad_angle)
        points.append((x + rx_rot, y + ry_rot))

    if outline_color:
        t.pencolor(outline_color)
        t.pensize(outline_width)
    elif fill_color and fill_color != "none":
        t.pencolor(fill_color)
        t.pensize(1)

    if fill_color and fill_color != "none":
        t.fillcolor(fill_color)
        jump(t, points[0][0], points[0][1])
        t.begin_fill()
        for pt in points[1:]:
            t.goto(pt[0], pt[1])
        t.end_fill()
        if outline_color:
            jump(t, points[0][0], points[0][1])
            t.pendown()
            for pt in points[1:]:
                t.goto(pt[0], pt[1])
            t.penup()
    elif outline_color:
        jump(t, points[0][0], points[0][1])
        t.pendown()
        for pt in points[1:]:
            t.goto(pt[0], pt[1])
        t.penup()

def draw_polygon(t, points, fill_color=None, outline_color=None, outline_width=1):
    """Draw a polygon given a list of (x, y) tuples."""
    if not points:
        return
    jump(t, points[0][0], points[0][1])
    if outline_color:
        t.pencolor(outline_color)
        t.pensize(outline_width)
    elif fill_color and fill_color != "none":
        t.pencolor(fill_color)
        t.pensize(1)
        
    if fill_color and fill_color != "none":
        t.fillcolor(fill_color)
        t.begin_fill()
        for pt in points[1:]:
            t.goto(pt[0], pt[1])
        t.goto(points[0][0], points[0][1])
        t.end_fill()
        if outline_color:
            t.pendown()
            for pt in points[1:]:
                t.goto(pt[0], pt[1])
            t.goto(points[0][0], points[0][1])
            t.penup()
    elif outline_color:
        t.pendown()
        for pt in points[1:]:
            t.goto(pt[0], pt[1])
        t.goto(points[0][0], points[0][1])
        t.penup()

def draw_star(t, x, y, size, color="#ffd700", points=5):
    """Draw a magical sparkling star."""
    jump(t, x, y)
    t.setheading(90)
    t.pencolor(color)
    t.fillcolor(color)
    t.begin_fill()
    if points == 4:
        for _ in range(4):
            t.forward(size)
            t.right(135)
            t.forward(size * 0.35)
            t.left(45)
    else:
        for _ in range(5):
            t.forward(size)
            t.right(144)
            t.forward(size)
            t.left(72)
    t.end_fill()

# ------------------------------------------------------------------------------
# Background & Celestial Magical Night
# ------------------------------------------------------------------------------
def draw_background():
    """Draw the starry night sky, celestial glow, and Hogwarts castle silhouette."""
    t_bg.clear()
    
    # 1. Gradient Sky Canvas
    stripe_height = 20
    num_stripes = int(SCREEN_HEIGHT / stripe_height) + 2
    for i in range(num_stripes):
        y = -SCREEN_HEIGHT // 2 + i * stripe_height
        factor = i / num_stripes
        # Interpolate color from bottom #080914 to top #181a3d
        r = int(8 + factor * 16)
        g = int(9 + factor * 17)
        b = int(20 + factor * 45)
        color = f"#{r:02x}{g:02x}{b:02x}"
        draw_polygon(t_bg, [
            (-SCREEN_WIDTH//2, y),
            (SCREEN_WIDTH//2, y),
            (SCREEN_WIDTH//2, y + stripe_height + 2),
            (-SCREEN_WIDTH//2, y + stripe_height + 2)
        ], color)

    # 2. Glowing Moon Crescent & Nebula Aura
    draw_circle(t_bg, -280, 240, 110, "#19224d") # Soft ambient halo
    draw_circle(t_bg, -280, 240, 80, "#28376e")  # Inner halo
    draw_circle(t_bg, -280, 240, 55, "#fff8db")  # Full moon base
    draw_circle(t_bg, -260, 255, 50, "#131633")  # Moon shadow to make crescent

    # 3. Hogwarts Castle Silhouette in the Distance
    castle_color = "#070814"
    castle_pts = [
        (-SCREEN_WIDTH//2, -380),
        (-SCREEN_WIDTH//2, -180),
        (-420, -170), (-400, -130), (-390, -130), (-370, -170), # Turret 1
        (-350, -160), (-330, -100), (-320, -90), (-310, -100), (-290, -160), # Great Tower
        (-270, -150), (-250, -120), (-230, -150),
        (-210, -170), (-160, -160), (-140, -190),
        # Spire ridge behind Harry
        (100, -190), (140, -160), (180, -140), (200, -90), (210, -80), (220, -90), (240, -150), # Right Spire
        (260, -130), (290, -100), (300, -100), (320, -140),
        (350, -130), (390, -80), (410, -80), (430, -140),
        (SCREEN_WIDTH//2, -150),
        (SCREEN_WIDTH//2, -380)
    ]
    draw_polygon(t_bg, castle_pts, castle_color)

    # Castle window tiny glowing lights
    window_lights = [
        (-330, -120), (-320, -130), (-315, -115),
        (-395, -150), (-250, -135), (210, -110),
        (295, -120), (405, -100), (400, -115)
    ]
    for wx, wy in window_lights:
        draw_circle(t_bg, wx, wy, 2.5, "#ffea78")

    # 4. Twinkling Stars Pattern
    random.seed(42) # Consistent starry map
    for _ in range(95):
        sx = random.randint(-SCREEN_WIDTH//2 + 20, SCREEN_WIDTH//2 - 20)
        sy = random.randint(-80, SCREEN_HEIGHT//2 - 20)
        # Avoid drawing right behind Harry's central face
        if -140 < sx < 140 and -100 < sy < 220:
            continue
        size = random.choice([1.2, 1.8, 2.5, 3.5])
        stype = random.choice([4, 5, 0])
        star_color = random.choice(["#ffffff", "#fff3b0", "#ffd700", "#cce7ff", "#fbcfe8"])
        if stype == 0:
            draw_circle(t_bg, sx, sy, size, star_color)
        else:
            draw_star(t_bg, sx, sy, size * 2, star_color, points=stype)
    random.seed() # Reset seed

    # 5. Magical Hogwarts Crest / Golden Rune Aura
    draw_circle(t_bg, -10, 50, 185, "#181d3d", "#d4af37", outline_width=2)
    draw_circle(t_bg, -10, 50, 175, "#12152e", "#740001", outline_width=1)

# ------------------------------------------------------------------------------
# Character Drawing: Harry Potter
# ------------------------------------------------------------------------------
def draw_harry_potter():
    """Draw the complete Harry Potter character with robes, scarf, wand, and facial details."""
    t_char.clear()

    # Center offsets for Harry
    CX = -10
    CY = 45

    # --------------------------------------------------------------------------
    # 1. Back Layer: Robe & Shoulders & Uniform
    # --------------------------------------------------------------------------
    # Outer Black Robe Shoulders
    robe_pts = [
        (CX - 165, CY - 240),  # Bottom Left
        (CX - 150, CY - 180),
        (CX - 110, CY - 90),   # Left Shoulder
        (CX - 60,  CY - 70),   # Left Neck
        (CX + 60,  CY - 70),   # Right Neck
        (CX + 115, CY - 90),   # Right Shoulder
        (CX + 155, CY - 180),
        (CX + 175, CY - 240),  # Bottom Right
        (CX + 130, CY - 260),
        (CX,       CY - 250),
        (CX - 130, CY - 260)
    ]
    draw_polygon(t_char, robe_pts, COLOR_ROBE_BLACK, "#000000", outline_width=3)

    # Robe Interior Gryffindor Scarlet Lining (Lapels)
    lapel_left = [
        (CX - 60, CY - 70),
        (CX - 25, CY - 180),
        (CX - 5, CY - 240),
        (CX - 45, CY - 230),
        (CX - 85, CY - 150),
        (CX - 75, CY - 85)
    ]
    draw_polygon(t_char, lapel_left, COLOR_GRYFF_RED)

    lapel_right = [
        (CX + 60, CY - 70),
        (CX + 25, CY - 180),
        (CX + 5, CY - 240),
        (CX + 45, CY - 230),
        (CX + 85, CY - 150),
        (CX + 75, CY - 85)
    ]
    draw_polygon(t_char, lapel_right, COLOR_GRYFF_RED)

    # White Collared School Shirt (V-neck area)
    shirt_pts = [
        (CX - 35, CY - 75),
        (CX + 35, CY - 75),
        (CX + 20, CY - 145),
        (CX,      CY - 165),
        (CX - 20, CY - 145)
    ]
    draw_polygon(t_char, shirt_pts, "#ffffff", "#d0d4dc", outline_width=1)

    # Charcoal V-Neck Sweater
    sweater_pts = [
        (CX - 30, CY - 100),
        (CX + 30, CY - 100),
        (CX + 22, CY - 155),
        (CX,      CY - 180),
        (CX - 22, CY - 155)
    ]
    draw_polygon(t_char, sweater_pts, "#333742")

    # Gryffindor Striped School Tie
    tie_pts = [
        (CX - 8, CY - 110),
        (CX + 8, CY - 110),
        (CX + 12, CY - 170),
        (CX,      CY - 195),
        (CX - 12, CY - 170)
    ]
    draw_polygon(t_char, tie_pts, COLOR_GRYFF_RED)
    
    # Tie Diagonal Gold Stripes
    tie_stripes = [
        [(CX - 9, CY - 122), (CX + 9, CY - 127), (CX + 10, CY - 134), (CX - 10, CY - 129)],
        [(CX - 10, CY - 142), (CX + 10, CY - 148), (CX + 11, CY - 155), (CX - 11, CY - 149)],
        [(CX - 8, CY - 168), (CX + 8, CY - 173), (CX + 5, CY - 180), (CX - 6, CY - 175)]
    ]
    for st in tie_stripes:
        draw_polygon(t_char, st, COLOR_GRYFF_GOLD)

    # --------------------------------------------------------------------------
    # 2. Gryffindor Scarf (Wrapped cozy layers with tassels)
    # --------------------------------------------------------------------------
    # Scarf Neck Loop (Alternating blocks of Scarlet and Gold)
    scarf_blocks = [
        ([(CX - 78, CY - 75), (CX - 50, CY - 72), (CX - 52, CY - 112), (CX - 82, CY - 110)], COLOR_GRYFF_RED),
        ([(CX - 50, CY - 72), (CX - 22, CY - 70), (CX - 24, CY - 115), (CX - 52, CY - 112)], COLOR_GRYFF_GOLD),
        ([(CX - 22, CY - 70), (CX + 8,  CY - 70), (CX + 6,  CY - 116), (CX - 24, CY - 115)], COLOR_GRYFF_RED),
        ([(CX + 8,  CY - 70), (CX + 40, CY - 72), (CX + 38, CY - 114), (CX + 6,  CY - 116)], COLOR_GRYFF_GOLD),
        ([(CX + 40, CY - 72), (CX + 78, CY - 75), (CX + 76, CY - 110), (CX + 38, CY - 114)], COLOR_GRYFF_RED),
    ]
    for pts, col in scarf_blocks:
        draw_polygon(t_char, pts, col, "#3a0000", outline_width=2)

    # Scarf Hanging Tail (Dangling down the left chest)
    scarf_tail_segments = [
        ([(CX - 72, CY - 110), (CX - 38, CY - 112), (CX - 40, CY - 142), (CX - 74, CY - 140)], COLOR_GRYFF_GOLD),
        ([(CX - 74, CY - 140), (CX - 40, CY - 142), (CX - 42, CY - 172), (CX - 76, CY - 170)], COLOR_GRYFF_RED),
        ([(CX - 76, CY - 170), (CX - 42, CY - 172), (CX - 44, CY - 202), (CX - 78, CY - 200)], COLOR_GRYFF_GOLD),
        ([(CX - 78, CY - 200), (CX - 44, CY - 202), (CX - 46, CY - 232), (CX - 80, CY - 230)], COLOR_GRYFF_RED),
    ]
    for pts, col in scarf_tail_segments:
        draw_polygon(t_char, pts, col, "#2a0000", outline_width=2)

    # Scarf Golden Tassels / Fringe at bottom
    tassel_y = CY - 232
    for tx in range(int(CX - 78), int(CX - 44), 6):
        draw_polygon(t_char, [
            (tx, tassel_y),
            (tx + 3, tassel_y),
            (tx + 2, tassel_y - 18),
            (tx - 1, tassel_y - 18)
        ], COLOR_GRYFF_GOLD)

    # --------------------------------------------------------------------------
    # 3. Head & Face
    # --------------------------------------------------------------------------
    # Ears
    draw_ellipse(t_char, CX - 88, CY + 10, 14, 22, COLOR_SKIN, COLOR_SKIN_SHADOW, outline_width=2, angle=10)
    draw_ellipse(t_char, CX + 88, CY + 10, 14, 22, COLOR_SKIN, COLOR_SKIN_SHADOW, outline_width=2, angle=-10)
    draw_ellipse(t_char, CX - 88, CY + 10, 8, 13, COLOR_SKIN_SHADOW)
    draw_ellipse(t_char, CX + 88, CY + 10, 8, 13, COLOR_SKIN_SHADOW)

    # Head / Face Oval Base
    draw_ellipse(t_char, CX, CY + 25, 88, 80, COLOR_SKIN, "#d8a483", outline_width=2)

    # Cute Cheeks Blush
    draw_circle(t_char, CX - 50, CY - 5, 14, COLOR_BLUSH)
    draw_circle(t_char, CX + 50, CY - 5, 14, COLOR_BLUSH)

    # Cute Smile & Lip
    jump(t_char, CX - 18, CY - 18)
    t_char.setheading(-50)
    t_char.pencolor("#7c2d12")
    t_char.pensize(3)
    t_char.pendown()
    t_char.circle(24, 100)
    t_char.penup()

    # Subtle Nose
    jump(t_char, CX - 2, CY + 6)
    t_char.setheading(-40)
    t_char.pencolor(COLOR_SKIN_SHADOW)
    t_char.pensize(2.5)
    t_char.pendown()
    t_char.circle(6, 90)
    t_char.penup()

    # --------------------------------------------------------------------------
    # 4. Expressive Bright Eyes
    # --------------------------------------------------------------------------
    eye_offset_x = 42
    eye_y = CY + 22

    for side in [-1, 1]:
        ex = CX + side * eye_offset_x
        # White Sclera
        draw_ellipse(t_char, ex, eye_y, 22, 20, "#ffffff", "#4b5563", outline_width=2)
        # Emerald Green Iris
        draw_circle(t_char, ex + side * 2, eye_y, 14, COLOR_EYE_GREEN)
        # Deep Forest Inner Shadow
        draw_circle(t_char, ex + side * 2, eye_y, 11, COLOR_EYE_DARK)
        # Black Pupil
        draw_circle(t_char, ex + side * 2, eye_y, 7, "#05130b")
        # Cute White Glint / Highlights
        draw_circle(t_char, ex + side * 2 - 4, eye_y + 4, 4.5, "#ffffff")
        draw_circle(t_char, ex + side * 2 + 3, eye_y - 3, 2.2, "#ffffff")

    # Upper Eyelashes / Eyelid lines
    for side in [-1, 1]:
        ex = CX + side * eye_offset_x
        jump(t_char, ex - 24, eye_y + 16)
        t_char.setheading(15 if side == 1 else -15)
        t_char.pencolor("#1f2937")
        t_char.pensize(2.5)
        t_char.pendown()
        t_char.circle(-26 if side == 1 else 26, 60)
        t_char.penup()

    # Eyebrows
    jump(t_char, CX - 64, CY + 60)
    t_char.setheading(25)
    t_char.pencolor(COLOR_HAIR_BLACK)
    t_char.pensize(4)
    t_char.pendown()
    t_char.circle(-45, 45)
    t_char.penup()

    jump(t_char, CX + 22, CY + 68)
    t_char.setheading(-10)
    t_char.pencolor(COLOR_HAIR_BLACK)
    t_char.pensize(4)
    t_char.pendown()
    t_char.circle(-45, 45)
    t_char.penup()

    # --------------------------------------------------------------------------
    # 5. Round Glasses (Outline only, transparent lens)
    # --------------------------------------------------------------------------
    glass_radius = 29
    # Left Frame
    draw_circle(t_char, CX - eye_offset_x, eye_y, glass_radius, fill_color=None, outline_color=COLOR_GLASSES, outline_width=5)
    # Right Frame
    draw_circle(t_char, CX + eye_offset_x, eye_y, glass_radius, fill_color=None, outline_color=COLOR_GLASSES, outline_width=5)

    # Glasses Bridge
    jump(t_char, CX - 13, eye_y + 4)
    t_char.setheading(30)
    t_char.pencolor(COLOR_GLASSES)
    t_char.pensize(5)
    t_char.pendown()
    t_char.circle(-26, 60)
    t_char.penup()

    # Glasses Side Arms (Temple)
    jump(t_char, CX - eye_offset_x - glass_radius + 2, eye_y + 4)
    t_char.setheading(165)
    t_char.pencolor(COLOR_GLASSES)
    t_char.pensize(4)
    t_char.pendown()
    t_char.forward(22)
    t_char.penup()

    jump(t_char, CX + eye_offset_x + glass_radius - 2, eye_y + 4)
    t_char.setheading(15)
    t_char.pencolor(COLOR_GLASSES)
    t_char.pensize(4)
    t_char.pendown()
    t_char.forward(22)
    t_char.penup()

    # Subtle Glass Lens Glint / Sheen
    for side in [-1, 1]:
        gx = CX + side * eye_offset_x
        draw_polygon(t_char, [
            (gx - 16, eye_y + 12),
            (gx - 10, eye_y + 18),
            (gx - 4, eye_y + 10),
            (gx - 10, eye_y + 4)
        ], "#ffffff")

    # --------------------------------------------------------------------------
    # 6. Iconic Lightning Bolt Scar
    # --------------------------------------------------------------------------
    # Located on Harry's right forehead (viewer's upper right)
    scar_origin_x = CX + 28
    scar_origin_y = CY + 84

    scar_pts = [
        (scar_origin_x, scar_origin_y),
        (scar_origin_x - 12, scar_origin_y - 18),
        (scar_origin_x - 3,  scar_origin_y - 17),
        (scar_origin_x - 14, scar_origin_y - 34),
        (scar_origin_x - 2,  scar_origin_y - 32),
        (scar_origin_x - 10, scar_origin_y - 48), # Sharp tip
        (scar_origin_x - 5,  scar_origin_y - 38),
        (scar_origin_x + 5,  scar_origin_y - 22),
        (scar_origin_x - 4,  scar_origin_y - 23),
        (scar_origin_x + 6,  scar_origin_y - 8),
        (scar_origin_x + 4,  scar_origin_y)
    ]
    # Glow outline
    draw_polygon(t_char, scar_pts, COLOR_SCAR, COLOR_GOLD, outline_width=2)

    # --------------------------------------------------------------------------
    # 7. Messy Signature Wizard Hair
    # --------------------------------------------------------------------------
    # Back Hair Silhouette
    back_hair = [
        (CX - 92, CY + 20),
        (CX - 108, CY + 55),
        (CX - 118, CY + 95),
        (CX - 98,  CY + 130),
        (CX - 70,  CY + 152),
        (CX - 30,  CY + 165),
        (CX + 20,  CY + 168),
        (CX + 75,  CY + 155),
        (CX + 110, CY + 125),
        (CX + 118, CY + 80),
        (CX + 105, CY + 40),
        (CX + 90,  CY + 15),
        (CX + 80,  CY + 60),
        (CX - 80,  CY + 60)
    ]
    draw_polygon(t_char, back_hair, COLOR_HAIR_BLACK, "#05060a", outline_width=2)

    # Front Spiky Tufted Bangs (Overlapping Harry's forehead playfully)
    bangs = [
        # Left Side Tufts
        [(CX - 100, CY + 50), (CX - 115, CY + 75), (CX - 85, CY + 70)],
        [(CX - 95, CY + 75), (CX - 110, CY + 115), (CX - 75, CY + 105)],
        [(CX - 85, CY + 105), (CX - 85, CY + 145), (CX - 50, CY + 125)],
        # Top High Messy Spikes
        [(CX - 60, CY + 130), (CX - 40, CY + 172), (CX - 15, CY + 140)],
        [(CX - 25, CY + 140), (CX + 10, CY + 178), (CX + 30, CY + 145)],
        [(CX + 20, CY + 145), (CX + 60, CY + 170), (CX + 65, CY + 135)],
        [(CX + 55, CY + 135), (CX + 95, CY + 150), (CX + 85, CY + 110)],
        [(CX + 80, CY + 110), (CX + 115, CY + 115), (CX + 95, CY + 75)],
        [(CX + 90, CY + 75), (CX + 110, CY + 55), (CX + 85, CY + 45)],
        # Forehead Bangs (Parted nicely to reveal lightning scar)
        [(CX - 88, CY + 75), (CX - 55, CY + 45), (CX - 45, CY + 78)],
        [(CX - 50, CY + 78), (CX - 20, CY + 50), (CX - 10, CY + 80)],
        [(CX - 15, CY + 80), (CX + 15, CY + 60), (CX + 25, CY + 82)], # Parting
        [(CX + 35, CY + 84), (CX + 60, CY + 55), (CX + 72, CY + 80)],
        [(CX + 68, CY + 80), (CX + 86, CY + 52), (CX + 90, CY + 78)],
    ]
    for bg_pts in bangs:
        draw_polygon(t_char, bg_pts, COLOR_HAIR_BLACK, "#000000", outline_width=1.5)

    # Hair Soft Texture Highlights (Deep Charcoal / Slate Blue)
    highlights = [
        [(CX - 35, CY + 158), (CX - 25, CY + 138), (CX - 20, CY + 145)],
        [(CX + 12, CY + 162), (CX + 18, CY + 144), (CX + 25, CY + 148)],
        [(CX - 70, CY + 120), (CX - 60, CY + 105), (CX - 55, CY + 112)],
        [(CX + 65, CY + 140), (CX + 68, CY + 120), (CX + 75, CY + 125)]
    ]
    for hl in highlights:
        draw_polygon(t_char, hl, COLOR_HAIR_HIGHLIGHT)

    # --------------------------------------------------------------------------
    # 8. Magic Wand & Hand
    # --------------------------------------------------------------------------
    # Raised Wizard Hand / Sleeve
    sleeve_pts = [
        (CX + 115, CY - 110),
        (CX + 160, CY - 75),
        (CX + 185, CY - 90),
        (CX + 140, CY - 145)
    ]
    draw_polygon(t_char, sleeve_pts, COLOR_ROBE_BLACK, "#000000", outline_width=2)
    # Scarlet Cuff Trim
    draw_polygon(t_char, [
        (CX + 160, CY - 75),
        (CX + 185, CY - 90),
        (CX + 180, CY - 100),
        (CX + 155, CY - 85)
    ], COLOR_GRYFF_RED)

    # Hand holding wand
    draw_circle(t_char, CX + 175, CY - 75, 15, COLOR_SKIN, COLOR_SKIN_SHADOW, outline_width=2)
    draw_circle(t_char, CX + 182, CY - 68, 7, COLOR_SKIN)

    # 11-inch Holly Wand pointing upwards to the sky
    wand_pts = [
        (CX + 175, CY - 75),  # Wand Handle Base
        (CX + 185, CY - 65),
        (CX + 270, CY + 25),  # Wand Tip
        (CX + 265, CY + 30)
    ]
    draw_polygon(t_char, wand_pts, COLOR_WAND_WOOD, "#2b1406", outline_width=2)
    # Handle Grip details
    draw_polygon(t_char, [
        (CX + 175, CY - 75),
        (CX + 185, CY - 65),
        (CX + 205, CY - 45),
        (CX + 195, CY - 55)
    ], COLOR_WAND_TIP)

    # Wand Tip Ambient Magical Glow
    wand_tip_x = CX + 268
    wand_tip_y = CY + 28
    draw_circle(t_char, wand_tip_x, wand_tip_y, 16, "#38bdf8")
    draw_circle(t_char, wand_tip_x, wand_tip_y, 9, "#ffffff")
    draw_star(t_char, wand_tip_x, wand_tip_y, 14, "#ffffff", points=4)

# ------------------------------------------------------------------------------
# Golden Snitch (Dynamic & Animated)
# ------------------------------------------------------------------------------
def draw_golden_snitch(x, y, wing_offset=0):
    """Draw the Golden Snitch with flapping magical wings at (x, y)."""
    t_snitch.clear()

    # Wing flap angle calculation
    wing_lift = math.sin(wing_offset) * 14

    # Left Wing
    left_wing_pts = [
        (x - 8, y + 4),
        (x - 35, y + 22 + wing_lift),
        (x - 70, y + 36 + wing_lift * 1.5),
        (x - 85, y + 25 + wing_lift),
        (x - 55, y + 10 + wing_lift * 0.5),
        (x - 25, y + 2)
    ]
    draw_polygon(t_snitch, left_wing_pts, "#e0f2fe", "#93c5fd", outline_width=1.5)

    # Right Wing
    right_wing_pts = [
        (x + 8, y + 4),
        (x + 35, y + 22 - wing_lift),
        (x + 70, y + 36 - wing_lift * 1.5),
        (x + 85, y + 25 - wing_lift),
        (x + 55, y + 10 - wing_lift * 0.5),
        (x + 25, y + 2)
    ]
    draw_polygon(t_snitch, right_wing_pts, "#e0f2fe", "#93c5fd", outline_width=1.5)

    # Golden Sphere Body
    draw_circle(t_snitch, x, y, 14, COLOR_GOLD, "#b45309", outline_width=2)
    # Surface Engravings / Seams
    jump(t_snitch, x - 10, y + 2)
    t_snitch.setheading(-30)
    t_snitch.pencolor("#d97706")
    t_snitch.pensize(1.5)
    t_snitch.pendown()
    t_snitch.circle(12, 60)
    t_snitch.penup()

    # Snitch Specular Light Highlight
    draw_circle(t_snitch, x - 4, y + 5, 3.5, "#ffffff")
    draw_star(t_snitch, x, y, 6, "#ffffff", points=4)

# ------------------------------------------------------------------------------
# UI Title, Banners & Instructions
# ------------------------------------------------------------------------------
def draw_ui():
    """Draw title banner, Gryffindor badge, and interactive spell control bar."""
    t_ui.clear()

    # Top Title Banner
    jump(t_ui, 0, SCREEN_HEIGHT // 2 - 52)
    t_ui.pencolor(COLOR_GOLD)
    t_ui.write("⚡  H A R R Y   P O T T E R  ⚡", align="center", font=("Georgia", 24, "bold"))

    jump(t_ui, 0, SCREEN_HEIGHT // 2 - 76)
    t_ui.pencolor("#cbd5e1")
    t_ui.write("THE BOY WHO LIVED  •  GRYFFINDOR HOUSE", align="center", font=("Arial", 11, "italic"))

    # Bottom Control Bar Box
    bar_y = -SCREEN_HEIGHT // 2 + 10
    draw_polygon(t_ui, [
        (-SCREEN_WIDTH//2 + 20, bar_y),
        (SCREEN_WIDTH//2 - 20, bar_y),
        (SCREEN_WIDTH//2 - 20, bar_y + 44),
        (-SCREEN_WIDTH//2 + 20, bar_y + 44)
    ], "#0d1127", COLOR_GRYFF_GOLD, outline_width=2)

    # Spell Instructions Text
    jump(t_ui, 0, bar_y + 12)
    t_ui.pencolor("#ffffff")
    controls_text = "[1/L] Lumos   [2/E] Expecto Patronum   [3/X] Expelliarmus   [4/W] Wingardium   [Click] Aim Wand   [S] Snitch   [Q] Quit"
    t_ui.write(controls_text, align="center", font=("Consolas", 10, "bold"))

def show_spell_banner(spell_name, subtext, color):
    """Display an on-screen magical spell announcement banner."""
    global active_spell_text, spell_text_timer
    active_spell_text = spell_name
    spell_text_timer = time.time() + 2.5

    t_ui.penup()
    # Erase previous banner space
    jump(t_ui, -250, 180)
    t_ui.fillcolor("#0a0b1a")
    t_ui.pencolor(color)
    t_ui.pensize(2)
    t_ui.begin_fill()
    for _ in range(2):
        t_ui.forward(500)
        t_ui.left(90)
        t_ui.forward(65)
        t_ui.left(90)
    t_ui.end_fill()

    # Spell Title
    jump(t_ui, 0, 215)
    t_ui.pencolor(color)
    t_ui.write(f"✨ {spell_name} ✨", align="center", font=("Georgia", 18, "bold"))

    # Subtext / Incantation Info
    jump(t_ui, 0, 190)
    t_ui.pencolor("#f8fafc")
    t_ui.write(subtext, align="center", font=("Arial", 11, "italic"))

# ------------------------------------------------------------------------------
# Spell Casting & Magic Visual FX System
# ------------------------------------------------------------------------------
class MagicParticle:
    """Individual particle for sparkles, energy trails, and magical bursts."""
    def __init__(self, x, y, vx, vy, color, radius, decay=0.04, shape="circle"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.decay = decay
        self.alpha = 1.0
        self.shape = shape

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.radius *= (1.0 - self.decay)
        self.alpha -= self.decay
        return self.alpha > 0.05 and self.radius > 0.5

    def draw(self, t):
        if self.shape == "star":
            draw_star(t, self.x, self.y, max(2, self.radius * 2), self.color, points=4)
        else:
            draw_circle(t, self.x, self.y, max(1, self.radius), self.color)

def get_wand_tip_pos():
    """Return the absolute screen coordinates of Harry's wand tip."""
    CX = -10
    CY = 45
    return CX + 268, CY + 28

def cast_lumos():
    """Cast Lumos Maxima: Brilliant expanding golden sunburst and light beams."""
    wx, wy = get_wand_tip_pos()
    show_spell_banner("LUMOS MAXIMA!", "A blinding brilliant sphere of pure golden illumination", "#fef08a")

    # Spawn radiant golden particles
    for _ in range(70):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2.5, 9.5)
        color = random.choice(["#ffffff", "#fef08a", "#fde047", "#eab308", "#fef9c3"])
        p = MagicParticle(
            wx, wy,
            math.cos(angle) * speed,
            math.sin(angle) * speed,
            color,
            random.uniform(4.0, 9.0),
            decay=random.uniform(0.03, 0.06),
            shape=random.choice(["circle", "star"])
        )
        particles.append(p)

def cast_expecto_patronum():
    """Cast Expecto Patronum: Ethereal silver-cyan patronus cosmic energy waves."""
    wx, wy = get_wand_tip_pos()
    show_spell_banner("EXPECTO PATRONUM!", "Ethereal silver stag guardian repels all darkness", "#38bdf8")

    # Concentric silver rings & spiraling cosmic motes
    for i in range(90):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3.0, 11.0)
        color = random.choice(["#ffffff", "#e0f2fe", "#bae6fd", "#7dd3fc", "#38bdf8", "#0284c7"])
        p = MagicParticle(
            wx, wy,
            math.cos(angle) * speed,
            math.sin(angle) * speed + random.uniform(-0.5, 1.5),
            color,
            random.uniform(3.5, 8.5),
            decay=random.uniform(0.02, 0.045),
            shape="star" if i % 2 == 0 else "circle"
        )
        particles.append(p)

def cast_expelliarmus():
    """Cast Expelliarmus: Fierce scarlet disarming shockwave beam and sparks."""
    wx, wy = get_wand_tip_pos()
    show_spell_banner("EXPELLIARMUS!", "Harry's signature scarlet disarming shockwave", "#f87171")

    # Directional scarlet energy beam exploding outwards
    for _ in range(85):
        # Beam biased to the upper-right trajectory
        angle = random.uniform(math.pi * 0.05, math.pi * 0.45)
        speed = random.uniform(5.0, 15.0)
        color = random.choice(["#ffffff", "#fca5a5", "#ef4444", "#dc2626", "#ffd700"])
        p = MagicParticle(
            wx, wy,
            math.cos(angle) * speed,
            math.sin(angle) * speed,
            color,
            random.uniform(3.0, 7.5),
            decay=random.uniform(0.03, 0.07),
            shape="circle"
        )
        particles.append(p)

def cast_wingardium_leviosa():
    """Cast Wingardium Leviosa: Golden swish-and-flick levitation swirls around the Snitch."""
    show_spell_banner("WINGARDIUM LEVIOSA!", "Swish and flick! Feather-light levitation enchantment", "#facc15")

    # Create swirls around snitch position
    for _ in range(65):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(10, 60)
        px = snitch_base_x + math.cos(angle) * dist
        py = snitch_base_y + math.sin(angle) * dist
        color = random.choice(["#ffffff", "#fef08a", "#facc15", "#eab308", "#a855f7"])
        p = MagicParticle(
            px, py,
            -math.sin(angle) * 3.5,
            math.cos(angle) * 3.5 + random.uniform(0.5, 2.0),
            color,
            random.uniform(3.0, 6.0),
            decay=0.035,
            shape="star"
        )
        particles.append(p)

def cast_custom_spell(target_x, target_y):
    """Shoot a magical spellstream from Harry's wand directly toward clicked (target_x, target_y)."""
    wx, wy = get_wand_tip_pos()
    dx = target_x - wx
    dy = target_y - wy
    dist = math.hypot(dx, dy)
    if dist == 0:
        return

    ux = dx / dist
    uy = dy / dist

    spell_colors = random.choice([
        ["#ffffff", "#38bdf8", "#818cf8"],
        ["#ffffff", "#f87171", "#fbbf24"],
        ["#ffffff", "#34d399", "#10b981"],
        ["#ffffff", "#c084fc", "#e879f9"]
    ])

    # Beam particles along path
    steps = int(dist / 14)
    for i in range(steps):
        t_factor = i / max(1, steps)
        px = wx + ux * dist * t_factor + random.uniform(-4, 4)
        py = wy + uy * dist * t_factor + random.uniform(-4, 4)
        p = MagicParticle(
            px, py,
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.choice(spell_colors),
            random.uniform(3.0, 6.0),
            decay=0.06
        )
        particles.append(p)

    # Impact explosion at target
    for _ in range(35):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2.0, 7.0)
        p = MagicParticle(
            target_x, target_y,
            math.cos(angle) * speed,
            math.sin(angle) * speed,
            random.choice(spell_colors),
            random.uniform(3.5, 7.0),
            decay=0.045,
            shape=random.choice(["circle", "star"])
        )
        particles.append(p)

def cast_random_spell():
    """Trigger a random grand magical incantation."""
    spells = [cast_lumos, cast_expecto_patronum, cast_expelliarmus, cast_wingardium_leviosa]
    random.choice(spells)()

def toggle_snitch():
    """Toggle Golden Snitch orbiting animation."""
    global snitch_animating
    snitch_animating = not snitch_animating

def on_click(x, y):
    """Handle mouse click to cast target spell."""
    cast_custom_spell(x, y)

def redraw_all():
    """Clear and redraw the full static & character scene."""
    draw_background()
    draw_harry_potter()
    draw_ui()

def quit_game():
    """Close the window gracefully."""
    global is_running
    is_running = False
    try:
        turtle.bye()
    except Exception:
        pass

# ------------------------------------------------------------------------------
# Main Animation Loop
# ------------------------------------------------------------------------------
def animation_frame():
    """Update dynamic elements, particles, snitch, and refresh screen."""
    global snitch_angle, particles, active_spell_text

    if not is_running:
        return

    try:
        # 1. Ambient Wand Sparkles
        wx, wy = get_wand_tip_pos()
        if random.random() < 0.65:
            p = MagicParticle(
                wx + random.uniform(-3, 3),
                wy + random.uniform(-3, 3),
                random.uniform(-0.8, 1.2),
                random.uniform(0.5, 2.2),
                random.choice(["#ffffff", "#e0f2fe", "#7dd3fc", "#ffd700"]),
                random.uniform(2.0, 4.5),
                decay=0.04,
                shape=random.choice(["circle", "star"])
            )
            particles.append(p)

        # 2. Golden Snitch Orbit & Wing Flap
        if snitch_animating:
            snitch_angle += 0.08
            cur_snitch_x = snitch_base_x + math.cos(snitch_angle * 0.6) * 35
            cur_snitch_y = snitch_base_y + math.sin(snitch_angle) * 22
            draw_golden_snitch(cur_snitch_x, cur_snitch_y, wing_offset=snitch_angle * 3.0)
        else:
            draw_golden_snitch(snitch_base_x, snitch_base_y, wing_offset=0)

        # 3. Particle System Update & Draw
        t_particles.clear()
        alive_particles = []
        for p in particles:
            if p.update():
                p.draw(t_particles)
                alive_particles.append(p)
        particles = alive_particles

        # 4. Clear expired spell banner
        if active_spell_text and time.time() > spell_text_timer:
            active_spell_text = ""
            # Clear banner area smoothly
            jump(t_ui, -255, 175)
            t_ui.fillcolor("#0a0b1a")
            t_ui.pencolor("#0a0b1a")
            t_ui.begin_fill()
            for _ in range(2):
                t_ui.forward(510)
                t_ui.left(90)
                t_ui.forward(75)
                t_ui.left(90)
            t_ui.end_fill()

        # Refresh canvas
        screen.update()

        # Next frame (~60 FPS)
        screen.ontimer(animation_frame, 20)
    except (turtle.Terminator, Exception):
        return

# ------------------------------------------------------------------------------
# Main Setup & Launch
# ------------------------------------------------------------------------------
def main():
    global screen, t_bg, t_char, t_snitch, t_spells, t_ui, t_particles, is_running
    is_running = True

    # Initialize Turtle Screen
    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("⚡ Harry Potter: The Boy Who Lived - Python Turtle Magic ⚡")
    screen.bgcolor(COLOR_BG_DARK)
    screen.tracer(0)  # High performance instant rendering for ultra-smooth graphics

    # Initialize Layered Turtles
    t_bg = create_turtle()
    t_char = create_turtle()
    t_snitch = create_turtle()
    t_spells = create_turtle()
    t_ui = create_turtle()
    t_particles = create_turtle()

    # Draw Initial Scene
    redraw_all()
    cast_lumos()  # Welcome greeting spell burst!

    # Register Keyboard Controls
    screen.listen()
    screen.onkey(cast_lumos, "1")
    screen.onkey(cast_lumos, "l")
    screen.onkey(cast_lumos, "L")

    screen.onkey(cast_expecto_patronum, "2")
    screen.onkey(cast_expecto_patronum, "e")
    screen.onkey(cast_expecto_patronum, "E")

    screen.onkey(cast_expelliarmus, "3")
    screen.onkey(cast_expelliarmus, "x")
    screen.onkey(cast_expelliarmus, "X")

    screen.onkey(cast_wingardium_leviosa, "4")
    screen.onkey(cast_wingardium_leviosa, "w")
    screen.onkey(cast_wingardium_leviosa, "W")

    screen.onkey(cast_random_spell, "space")
    screen.onkey(toggle_snitch, "s")
    screen.onkey(toggle_snitch, "S")
    screen.onkey(redraw_all, "r")
    screen.onkey(redraw_all, "R")
    screen.onkey(quit_game, "q")
    screen.onkey(quit_game, "Q")
    screen.onkey(quit_game, "Escape")

    # Register Mouse Click
    screen.onscreenclick(on_click)

    # Start Main Animation Loop
    animation_frame()

    # Keep window active
    try:
        turtle.mainloop()
    except (turtle.Terminator, Exception):
        pass

if __name__ == "__main__":
    main()
