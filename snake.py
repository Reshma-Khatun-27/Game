"""
================================================================================
                    SNAKE GAME - TURTLE EDITION (WITH AI BOT)
================================================================================
Controls:
    - Arrow Keys or W / A / S / D : Change snake direction (Manual Mode)
    - Tab or T                    : Toggle AI Autoplay (Watch Snake Play Itself!)
    - Space or P                  : Pause / Resume game
    - R                           : Restart game after Game Over
    - Q / Escape                  : Quit game
================================================================================
"""

import turtle
import time
import random
import os
from collections import deque

# ------------------------------------------------------------------------------
# Game Configuration & Constants
# ------------------------------------------------------------------------------
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 740
PLAY_AREA_HALF = 280  # Playable boundary from -280 to +280 (560x560 box)
INITIAL_DELAY = 0.09
SPEEDUP_FACTOR = 0.0012
MIN_DELAY = 0.035
SEGMENT_SIZE = 20

# Colors (Modern Neon Arcade Palette)
BG_COLOR = "#0b0f19"          # Deep space dark
ARENA_BG = "#0f172a"          # Slate 900
BORDER_COLOR = "#38bdf8"      # Cyan 400
BORDER_GLOW = "#0284c7"       # Cyan 600

SNAKE_HEAD_COLOR = "#10b981"  # Emerald 500
SNAKE_EYE_COLOR = "#ffffff"   # White
SNAKE_PUPIL_COLOR = "#0f172a" # Dark pupil
SNAKE_BODY_1 = "#22c55e"      # Green 500
SNAKE_BODY_2 = "#4ade80"      # Green 400

FOOD_COLOR = "#f43f5e"        # Rose 500
BONUS_COLOR = "#facc15"       # Amber 400 (Golden Apple)
TEXT_COLOR = "#f8fafc"        # Slate 50
SUBTEXT_COLOR = "#94a3b8"     # Slate 400
AI_BADGE_COLOR = "#a855f7"    # Purple 500
HUMAN_BADGE_COLOR = "#38bdf8" # Cyan 400

# Highscore file location
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.txt")

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def load_high_score():
    """Load high score from file or default to 0."""
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

def round_grid(val):
    """Round a coordinate to nearest 20px grid point."""
    return round(val / SEGMENT_SIZE) * SEGMENT_SIZE

# ------------------------------------------------------------------------------
# Game Class
# ------------------------------------------------------------------------------
class SnakeGame:
    def __init__(self):
        # Window setup
        self.win = turtle.Screen()
        self.win.title("Neon Snake Game | Python Turtle")
        self.win.bgcolor(BG_COLOR)
        self.win.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.win.tracer(0)  # Turn off auto-updates for silky smooth animation

        # Game State Variables
        self.score = 0
        self.high_score = load_high_score()
        self.delay = INITIAL_DELAY
        self.is_paused = False
        self.is_game_over = False
        self.ai_mode = False  # False = Human player, True = AI Autoplay Bot
        self.bonus_timer = 0
        self.bonus_active = False
        self.segments = []

        # Setup Visual Elements
        self.draw_arena()
        self.create_scoreboard()
        self.create_snake_head()
        self.create_eyes()
        self.create_food()
        self.create_bonus_food()
        self.create_overlay_pen()

        # Build initial snake with 3 body segments
        self.build_initial_snake()

        # Controls
        self.setup_keybindings()

        # Update initial scoreboard
        self.update_scoreboard()

    def draw_arena(self):
        """Draws the border and decorative arena frame."""
        border = turtle.Turtle()
        border.speed(0)
        border.penup()
        border.hideturtle()

        # Draw filled arena background
        limit = PLAY_AREA_HALF + 10
        border.goto(-limit, limit)
        border.color(BORDER_COLOR, ARENA_BG)
        border.pensize(3)
        border.begin_fill()
        for _ in range(4):
            border.forward(limit * 2)
            border.right(90)
        border.end_fill()

    def create_scoreboard(self):
        """Creates scoreboard turtle."""
        self.score_pen = turtle.Turtle()
        self.score_pen.speed(0)
        self.score_pen.color(TEXT_COLOR)
        self.score_pen.penup()
        self.score_pen.hideturtle()
        self.score_pen.goto(0, 310)

    def create_overlay_pen(self):
        """Turtle for displaying Game Over and Pause messages."""
        self.overlay_pen = turtle.Turtle()
        self.overlay_pen.speed(0)
        self.overlay_pen.penup()
        self.overlay_pen.hideturtle()

    def update_scoreboard(self):
        """Refreshes the score, high score, and mode badges."""
        self.score_pen.clear()
        mode_text = "[AI AUTOPLAY]" if self.ai_mode else "[HUMAN]"
        mode_color = AI_BADGE_COLOR if self.ai_mode else HUMAN_BADGE_COLOR

        self.score_pen.goto(0, 310)
        self.score_pen.color(TEXT_COLOR)
        self.score_pen.write(
            f"Score: {self.score}    ★ High Score: {self.high_score}    ",
            align="right",
            font=("Segoe UI", 14, "bold")
        )

        self.score_pen.goto(10, 310)
        self.score_pen.color(mode_color)
        self.score_pen.write(
            f"{mode_text} (Press Tab to switch)",
            align="left",
            font=("Segoe UI", 12, "bold")
        )

    def create_snake_head(self):
        """Initializes the snake head."""
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(SNAKE_HEAD_COLOR)
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "right"  # Start moving right

    def create_eyes(self):
        """Creates two eye turtles to give the snake an expressive face."""
        self.eye_left = turtle.Turtle()
        self.eye_left.speed(0)
        self.eye_left.shape("circle")
        self.eye_left.shapesize(0.35, 0.35)
        self.eye_left.color(SNAKE_EYE_COLOR)
        self.eye_left.penup()

        self.eye_right = turtle.Turtle()
        self.eye_right.speed(0)
        self.eye_right.shape("circle")
        self.eye_right.shapesize(0.35, 0.35)
        self.eye_right.color(SNAKE_EYE_COLOR)
        self.eye_right.penup()

        self.pupil_left = turtle.Turtle()
        self.pupil_left.speed(0)
        self.pupil_left.shape("circle")
        self.pupil_left.shapesize(0.18, 0.18)
        self.pupil_left.color(SNAKE_PUPIL_COLOR)
        self.pupil_left.penup()

        self.pupil_right = turtle.Turtle()
        self.pupil_right.speed(0)
        self.pupil_right.shape("circle")
        self.pupil_right.shapesize(0.18, 0.18)
        self.pupil_right.color(SNAKE_PUPIL_COLOR)
        self.pupil_right.penup()

        self.update_eyes()

    def update_eyes(self):
        """Positions eyes according to snake movement direction."""
        hx, hy = self.head.xcor(), self.head.ycor()
        d = self.head.direction

        if d == "up":
            l_pos, r_pos = (hx - 5, hy + 5), (hx + 5, hy + 5)
            p_offset = (0, 2)
        elif d == "down":
            l_pos, r_pos = (hx + 5, hy - 5), (hx - 5, hy - 5)
            p_offset = (0, -2)
        elif d == "left":
            l_pos, r_pos = (hx - 5, hy - 5), (hx - 5, hy + 5)
            p_offset = (-2, 0)
        else:  # right or stop
            l_pos, r_pos = (hx + 5, hy + 5), (hx + 5, hy - 5)
            p_offset = (2, 0)

        self.eye_left.goto(l_pos)
        self.eye_right.goto(r_pos)
        self.pupil_left.goto(l_pos[0] + p_offset[0], l_pos[1] + p_offset[1])
        self.pupil_right.goto(r_pos[0] + p_offset[0], r_pos[1] + p_offset[1])

    def create_food(self):
        """Initializes regular food item."""
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.shapesize(0.85, 0.85)
        self.food.color(FOOD_COLOR)
        self.food.penup()
        self.relocate_food(self.food)

    def create_bonus_food(self):
        """Initializes bonus golden apple."""
        self.bonus_food = turtle.Turtle()
        self.bonus_food.speed(0)
        self.bonus_food.shape("turtle")
        self.bonus_food.color(BONUS_COLOR)
        self.bonus_food.penup()
        self.bonus_food.goto(1000, 1000)  # Off-screen
        self.bonus_active = False

    def build_initial_snake(self):
        """Constructs an initial 3-segment snake body behind the head."""
        for i in range(1, 4):
            segment = turtle.Turtle()
            segment.speed(0)
            segment.shape("square")
            color = SNAKE_BODY_1 if i % 2 == 1 else SNAKE_BODY_2
            segment.color(color)
            segment.penup()
            segment.goto(-i * SEGMENT_SIZE, 0)
            self.segments.append(segment)

    def get_random_grid_pos(self):
        """Generate a random coordinate aligned to segment grid."""
        max_step = PLAY_AREA_HALF // SEGMENT_SIZE
        x = random.randint(-max_step + 1, max_step - 1) * SEGMENT_SIZE
        y = random.randint(-max_step + 1, max_step - 1) * SEGMENT_SIZE
        return x, y

    def relocate_food(self, food_turtle):
        """Places food in a random open position."""
        while True:
            x, y = self.get_random_grid_pos()
            if self.head.distance(x, y) < 18:
                continue
            if any(segment.distance(x, y) < 18 for segment in self.segments):
                continue
            food_turtle.goto(x, y)
            break

    # --------------------------------------------------------------------------
    # Movement Controls
    # --------------------------------------------------------------------------
    def go_up(self):
        if not self.ai_mode and self.head.direction != "down" and not self.is_paused and not self.is_game_over:
            self.head.direction = "up"

    def go_down(self):
        if not self.ai_mode and self.head.direction != "up" and not self.is_paused and not self.is_game_over:
            self.head.direction = "down"

    def go_left(self):
        if not self.ai_mode and self.head.direction != "right" and not self.is_paused and not self.is_game_over:
            self.head.direction = "left"

    def go_right(self):
        if not self.ai_mode and self.head.direction != "left" and not self.is_paused and not self.is_game_over:
            self.head.direction = "right"

    def toggle_ai(self):
        """Toggle AI autoplay mode."""
        self.ai_mode = not self.ai_mode
        self.update_scoreboard()

    def toggle_pause(self):
        """Pause or unpause the game."""
        if self.is_game_over:
            return
        self.is_paused = not self.is_paused
        self.overlay_pen.clear()
        if self.is_paused:
            self.overlay_pen.goto(0, 30)
            self.overlay_pen.color("#facc15")
            self.overlay_pen.write("GAME PAUSED", align="center", font=("Segoe UI", 24, "bold"))
            self.overlay_pen.goto(0, -10)
            self.overlay_pen.color(SUBTEXT_COLOR)
            self.overlay_pen.write("Press Space or P to resume", align="center", font=("Segoe UI", 13, "normal"))

    def setup_keybindings(self):
        """Bind keyboard inputs."""
        self.win.listen()
        # Arrow keys
        self.win.onkeypress(self.go_up, "Up")
        self.win.onkeypress(self.go_down, "Down")
        self.win.onkeypress(self.go_left, "Left")
        self.win.onkeypress(self.go_right, "Right")
        # WASD keys
        self.win.onkeypress(self.go_up, "w")
        self.win.onkeypress(self.go_up, "W")
        self.win.onkeypress(self.go_down, "s")
        self.win.onkeypress(self.go_down, "S")
        self.win.onkeypress(self.go_left, "a")
        self.win.onkeypress(self.go_left, "A")
        self.win.onkeypress(self.go_right, "d")
        self.win.onkeypress(self.go_right, "D")
        # Mode & Utility
        self.win.onkeypress(self.toggle_ai, "Tab")
        self.win.onkeypress(self.toggle_ai, "t")
        self.win.onkeypress(self.toggle_ai, "T")
        self.win.onkeypress(self.toggle_pause, "space")
        self.win.onkeypress(self.toggle_pause, "p")
        self.win.onkeypress(self.toggle_pause, "P")
        self.win.onkeypress(self.restart_game, "r")
        self.win.onkeypress(self.restart_game, "R")
        self.win.onkeypress(self.quit_game, "Escape")
        self.win.onkeypress(self.quit_game, "q")
        self.win.onkeypress(self.quit_game, "Q")

    def move(self):
        """Moves head according to current direction."""
        if self.head.direction == "up":
            self.head.sety(self.head.ycor() + SEGMENT_SIZE)
        elif self.head.direction == "down":
            self.head.sety(self.head.ycor() - SEGMENT_SIZE)
        elif self.head.direction == "left":
            self.head.setx(self.head.xcor() - SEGMENT_SIZE)
        elif self.head.direction == "right":
            self.head.setx(self.head.xcor() + SEGMENT_SIZE)

        self.update_eyes()

    def add_segment(self):
        """Appends a new tail segment to the snake."""
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        color = SNAKE_BODY_1 if len(self.segments) % 2 == 0 else SNAKE_BODY_2
        new_segment.color(color)
        new_segment.penup()
        # Place behind current last segment
        if self.segments:
            new_segment.goto(self.segments[-1].xcor(), self.segments[-1].ycor())
        else:
            new_segment.goto(self.head.xcor(), self.head.ycor())
        self.segments.append(new_segment)

    # --------------------------------------------------------------------------
    # AI Autoplay Pathfinding
    # --------------------------------------------------------------------------
    def get_ai_next_direction(self):
        """Calculates optimal move using BFS pathfinding and space safety."""
        start = (round_grid(self.head.xcor()), round_grid(self.head.ycor()))
        target_food = self.bonus_food if self.bonus_active else self.food
        target = (round_grid(target_food.xcor()), round_grid(target_food.ycor()))

        # Body obstacles (excluding tail tip because it moves)
        obstacles = set()
        for seg in self.segments[:-1]:
            obstacles.add((round_grid(seg.xcor()), round_grid(seg.ycor())))

        # Directions: (dx, dy, dir_name, opposite)
        moves = [
            (0, SEGMENT_SIZE, "up", "down"),
            (0, -SEGMENT_SIZE, "down", "up"),
            (-SEGMENT_SIZE, 0, "left", "right"),
            (SEGMENT_SIZE, 0, "right", "left"),
        ]

        def is_safe(pos):
            x, y = pos
            return abs(x) <= PLAY_AREA_HALF and abs(y) <= PLAY_AREA_HALF and pos not in obstacles

        # 1. BFS to find shortest path to food
        queue = deque([(start, [])])
        visited = {start}
        best_path = None

        while queue:
            current, path = queue.popleft()
            if current == target:
                best_path = path
                break

            for dx, dy, dname, opp in moves:
                next_pos = (current[0] + dx, current[1] + dy)
                if is_safe(next_pos) and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [dname]))

        if best_path and len(best_path) > 0:
            chosen_dir = best_path[0]
            # Safety check: avoid instant 180 reverse
            for dx, dy, dname, opp in moves:
                if dname == chosen_dir and self.head.direction != opp:
                    return chosen_dir

        # 2. Fallback: Choose safest neighboring move with maximum open space
        best_dir = None
        max_open_space = -1

        for dx, dy, dname, opp in moves:
            if self.head.direction == opp:
                continue
            next_pos = (start[0] + dx, start[1] + dy)
            if is_safe(next_pos):
                # Flood fill count from next_pos
                open_count = self.count_free_space(next_pos, obstacles)
                if open_count > max_open_space:
                    max_open_space = open_count
                    best_dir = dname

        return best_dir if best_dir else self.head.direction

    def count_free_space(self, start_pos, obstacles):
        """Counts reachable tiles using BFS flood fill."""
        queue = deque([start_pos])
        visited = {start_pos}
        count = 0
        limit = 60  # Depth limit for fast execution

        while queue and count < limit:
            curr = queue.popleft()
            count += 1
            for dx, dy in [(0, 20), (0, -20), (20, 0), (-20, 0)]:
                nxt = (curr[0] + dx, curr[1] + dy)
                if abs(nxt[0]) <= PLAY_AREA_HALF and abs(nxt[1]) <= PLAY_AREA_HALF:
                    if nxt not in obstacles and nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
        return count

    # --------------------------------------------------------------------------
    # Game Over & Restart
    # --------------------------------------------------------------------------
    def show_game_over(self):
        """Displays Game Over UI."""
        self.is_game_over = True
        self.head.color("#ef4444")  # Flash red
        self.overlay_pen.clear()
        self.overlay_pen.goto(0, 40)
        self.overlay_pen.color("#ef4444")
        self.overlay_pen.write("GAME OVER", align="center", font=("Segoe UI", 28, "bold"))

        self.overlay_pen.goto(0, 0)
        self.overlay_pen.color(TEXT_COLOR)
        self.overlay_pen.write(f"Final Score: {self.score}", align="center", font=("Segoe UI", 16, "bold"))

        self.overlay_pen.goto(0, -40)
        self.overlay_pen.color(SUBTEXT_COLOR)
        self.overlay_pen.write("Press 'R' to Play Again  •  'Q' to Quit", align="center", font=("Segoe UI", 13, "normal"))

    def restart_game(self):
        """Resets the game state to start a new round."""
        if not self.is_game_over:
            return

        self.overlay_pen.clear()

        # Hide old segments
        for seg in self.segments:
            seg.goto(1000, 1000)
            seg.hideturtle()
        self.segments.clear()

        # Reset snake head & eyes
        self.head.goto(0, 0)
        self.head.direction = "right"
        self.head.color(SNAKE_HEAD_COLOR)
        self.update_eyes()

        # Rebuild initial 3 segments
        self.build_initial_snake()

        # Reset bonus food
        self.bonus_food.goto(1000, 1000)
        self.bonus_active = False

        # Reset state
        self.score = 0
        self.delay = INITIAL_DELAY
        self.is_paused = False
        self.is_game_over = False
        self.relocate_food(self.food)
        self.update_scoreboard()

    def quit_game(self):
        """Closes the game window cleanly."""
        try:
            self.win.bye()
        except turtle.Terminator:
            pass

    # --------------------------------------------------------------------------
    # Main Loop
    # --------------------------------------------------------------------------
    def run(self):
        """Main game loop."""
        running = True
        while running:
            try:
                self.win.update()

                if not self.is_paused and not self.is_game_over:
                    # AI Autopilot Move Decision
                    if self.ai_mode:
                        next_dir = self.get_ai_next_direction()
                        if next_dir:
                            self.head.direction = next_dir

                    # 1. Check for wall collision
                    x = self.head.xcor()
                    y = self.head.ycor()
                    if abs(x) > PLAY_AREA_HALF or abs(y) > PLAY_AREA_HALF:
                        self.show_game_over()
                        continue

                    # 2. Check collision with regular food
                    if self.head.distance(self.food) < 18:
                        self.score += 10
                        if self.score > self.high_score:
                            self.high_score = self.score
                            save_high_score(self.high_score)

                        self.update_scoreboard()
                        self.relocate_food(self.food)
                        self.add_segment()

                        # Speed up slightly with each food
                        self.delay = max(MIN_DELAY, self.delay - SPEEDUP_FACTOR)

                        # 25% chance to spawn special golden food
                        if not self.bonus_active and random.random() < 0.25:
                            self.relocate_food(self.bonus_food)
                            self.bonus_active = True
                            self.bonus_timer = 50

                    # 3. Handle bonus golden food
                    if self.bonus_active:
                        self.bonus_timer -= 1
                        if self.head.distance(self.bonus_food) < 18:
                            self.score += 30  # Bonus +30 points!
                            if self.score > self.high_score:
                                self.high_score = self.score
                                save_high_score(self.high_score)
                            self.update_scoreboard()
                            self.bonus_food.goto(1000, 1000)
                            self.bonus_active = False
                            self.add_segment()
                        elif self.bonus_timer <= 0:
                            self.bonus_food.goto(1000, 1000)
                            self.bonus_active = False

                    # 4. Move body segments to follow previous positions
                    for i in range(len(self.segments) - 1, 0, -1):
                        x_prev = self.segments[i - 1].xcor()
                        y_prev = self.segments[i - 1].ycor()
                        self.segments[i].goto(x_prev, y_prev)

                    # Move first segment to head's position
                    if len(self.segments) > 0:
                        self.segments[0].goto(self.head.xcor(), self.head.ycor())

                    # 5. Move head forward
                    self.move()

                    # 6. Check for self-collision (head hitting body)
                    for segment in self.segments:
                        if segment.distance(self.head) < 15 and self.head.direction != "stop":
                            self.show_game_over()
                            break

                time.sleep(self.delay)

            except (turtle.Terminator, Exception):
                # Window closed or game terminated
                running = False
                break


# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
