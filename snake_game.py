import turtle as t
import random

w = 500  # Width of box
h = 600  # Height of box, increased to add a scoreboard section
game_h = 500  # Height of the game area
food_size = 10  # Size of food
initial_delay = 100  # initial delay in milliseconds

# Values by which snake will move in direction when given direction
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

global SCORE, delay
SCORE = 0
delay = initial_delay

# Default position of game scene
def reset():
    global snake, snake_dir, food_position, pen, SCORE, delay
    SCORE = 0
    delay = initial_delay
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"  # default snake direction
    food_position = get_random_food_position()
    food.goto(food_position)  # render food on scene
    update_scoreboard()
    move_snake()

def move_snake():
    global snake_dir, SCORE, delay

    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_dir][0]
    new_head[1] = snake[-1][1] + offsets[snake_dir][1]

    if new_head in snake[:-1]:  # Check for collision with itself
        game_over()
    else:
        snake.append(new_head)

        if not food_collision():
            snake.pop(0)

        if snake[-1][0] > w / 2:
            snake[-1][0] -= w
        elif snake[-1][0] < -w / 2:
            snake[-1][0] += w
        elif snake[-1][1] > game_h / 2:
            snake[-1][1] -= game_h
        elif snake[-1][1] < -game_h / 2:
            snake[-1][1] += game_h

        pen.clearstamps()

        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()

        screen.update()

        # Increase speed gradually as score increases
        delay = initial_delay - (SCORE // 10)
        delay = max(20, delay)  # Ensure the minimum delay is 20 milliseconds

        t.ontimer(move_snake, delay)

def game_over():
    global SCORE
    pen.goto(0, 0)
    pen.color("black")
    pen.write(f"Game Over! Score: {SCORE}", align="center", font=("Arial", 24, "normal"))
    screen.update()
    t.done()  # Stop the turtle graphics loop

# If snake collides with food
def food_collision():
    global food_position, SCORE
    if get_distance(snake[-1], food_position) < 20:
        SCORE += 10
        update_scoreboard()
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False

# Random position for food
def get_random_food_position():
    x = random.randint(-w / 2 + food_size, w / 2 - food_size)
    y = random.randint(-game_h / 2 + food_size, game_h / 2 - food_size)
    return (x, y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance

# Control
def go_up():
    global snake_dir
    if snake_dir != "down":
        snake_dir = "up"

def go_down():
    global snake_dir
    if snake_dir != "up":
        snake_dir = "down"

def go_left():
    global snake_dir
    if snake_dir != "right":
        snake_dir = "left"

def go_right():
    global snake_dir
    if snake_dir != "left":
        snake_dir = "right"

# Function to update the scoreboard
def update_scoreboard():
    scoreboard.clear()
    scoreboard.write(f"Score: {SCORE}", align="center", font=("Arial", 24, "normal"))

# Define screen setup
screen = t.Screen()
screen.setup(w, h)
screen.title("Snake Game")
screen.bgcolor("lightgrey")
screen.tracer(0)

# Define snake setup
pen = t.Turtle("square")
pen.penup()

# Define food setup
food = t.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(food_size / 20)
food.penup()

# Define scoreboard setup
scoreboard = t.Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.goto(0, game_h / 2 + 20)
scoreboard.color("black")
update_scoreboard()

# Define control setup
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

reset()
t.mainloop()
