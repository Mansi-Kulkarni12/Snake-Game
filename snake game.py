import tkinter as tk
import random

# Game settings
WIDTH = 500
HEIGHT = 500
SEG_SIZE = 20 
INITIAL_LENGTH = 3 
LEVELS = {"Easy": 200, "Medium": 120, "Hard": 70} 
SNAKE_COLORS = ["limegreen", "cyan", "orange", "yellow", "magenta"]

class SnakeGame:
    def __init__(self, master): 
        self.master = master 
        self.master.title("Snake Game") 

        self.level = tk.StringVar(value="Medium")
        self.snake_color = random.choice(SNAKE_COLORS)
        self.score = 0
        self.paused = False

        self.setup_controls()

        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack()

        self.reset_game()
        self.master.bind("<Key>", self.keypress)

    def setup_controls(self):
        top_frame = tk.Frame(self.master)
        top_frame.pack()

        tk.Label(top_frame, text="Select Difficulty:").pack(side=tk.LEFT, padx=5)
        for lvl in LEVELS:
            tk.Radiobutton(top_frame, text=lvl, variable=self.level, value=lvl).pack(side=tk.LEFT)

        tk.Button(top_frame, text="New Game", command=self.reset_game).pack(side=tk.RIGHT, padx=10)

    def reset_game(self):
        self.snake_color = random.choice(SNAKE_COLORS)
        self.canvas.delete("all")
        self.snake_length = INITIAL_LENGTH
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        start_x = WIDTH // 2 - (WIDTH // 2) % SEG_SIZE
        start_y = HEIGHT // 2 - (HEIGHT // 2) % SEG_SIZE
        self.snake = [(start_x, start_y)]
        self.snake_direction = "Right"
        self.food = None
        self.running = True
        self.paused = False
        self.create_food()
        self.update_game()

    def create_food(self):
        cols = WIDTH // SEG_SIZE
        rows = HEIGHT // SEG_SIZE
        while True:
            x = random.randint(0, cols - 1) * SEG_SIZE
            y = random.randint(0, rows - 1) * SEG_SIZE
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def keypress(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            self.change_direction(event)
        elif event.char.lower() == "p":
            self.paused = not self.paused

    def change_direction(self, event):
        if not self.running or self.paused:
            return
        if event.keysym == "Left" and self.snake_direction != "Right":
            self.snake_direction = "Left"
        elif event.keysym == "Right" and self.snake_direction != "Left":
            self.snake_direction = "Right"
        elif event.keysym == "Up" and self.snake_direction != "Down":
            self.snake_direction = "Up"
        elif event.keysym == "Down" and self.snake_direction != "Up":
            self.snake_direction = "Down"

    def update_game(self):
        if not self.running or self.paused:
            self.master.after(100, self.update_game)
            return

        head_x, head_y = self.snake[0]

        if self.snake_direction == "Left":
            head_x -= SEG_SIZE
        elif self.snake_direction == "Right":
            head_x += SEG_SIZE
        elif self.snake_direction == "Up":
            head_y -= SEG_SIZE
        elif self.snake_direction == "Down":
            head_y += SEG_SIZE

        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            (head_x, head_y) in self.snake
        ):
            self.game_over()
            return

        self.snake = [(head_x, head_y)] + self.snake[:self.snake_length - 1]

        if (head_x, head_y) == self.food:
            self.snake_length += 1
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            self.create_food()

        self.canvas.delete("all")
        fx, fy = self.food
        self.canvas.create_rectangle(fx, fy, fx + SEG_SIZE, fy + SEG_SIZE, fill="red", outline="red")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE,
                                         fill=self.snake_color, outline="black")

        speed = LEVELS[self.level.get()]
        self.master.after(speed, self.update_game)

    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over!", fill="white", font=("Arial", 24))

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
