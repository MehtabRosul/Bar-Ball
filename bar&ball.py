import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pong with Level Progression")

# Set up the colors
COLORS = [(255, 255, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0), (0, 0, 255), (128, 0, 128)]
LEVEL_COLORS = ['White', 'Green', 'Yellow', 'Red', 'Blue', 'Purple']

# Set up the game objects
ball_radius = 10
ball_x = window_width // 2
ball_y = window_height // 2
ball_speed_x = random.choice([-2, 2])
ball_speed_y = random.choice([-2, 2])
current_color_index = 0  # Index for current ball color
current_level = 1
level_change_time = time.time() + 60  # 1 minute from now

board_width = 10
board_height = 80
board_speed = 5

board1_x = 10
board1_y = window_height // 2 - board_height // 2

board2_x = window_width - board_width - 10
board2_y = window_height // 2 - board_height // 2

score1 = 0
score2 = 0

# Function to handle level change
def increase_level():
    global current_level, ball_speed_x, ball_speed_y, current_color_index
    if current_level < 6:
        current_level += 1
        ball_speed_x *= 1.5  # Increase ball speed
        ball_speed_y *= 1.5
        current_color_index = current_level - 1  # Change ball color
        print(f"Level {current_level}: {LEVEL_COLORS[current_color_index]}")

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for level change
    if time.time() > level_change_time:
        increase_level()
        level_change_time = time.time() + 60  # Set the next level change time

    # Move the boards
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and board1_y > 0:
        board1_y -= board_speed
    if keys[pygame.K_DOWN] and board1_y < window_height - board_height:
        board1_y += board_speed

    # Move the automatic board with a chance to miss the ball
    if random.random() > 0.1:  # 90% chance to follow the ball
        if ball_y < board2_y + board_height // 2:
            board2_y -= board_speed
        elif ball_y > board2_y + board_height // 2:
            board2_y += board_speed
    else:  # 10% chance to not move
        pass

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collisions with the boards
    if ball_x <= board1_x + board_width and board1_y <= ball_y <= board1_y + board_height:
        ball_speed_x *= -1
    if ball_x >= board2_x - ball_radius and board2_y <= ball_y <= board2_y + board_height:
        ball_speed_x *= -1

    # Check for collisions with the walls
    if ball_y <= 0 or ball_y >= window_height - ball_radius:
        ball_speed_y *= -1

    # Check for scoring
    if ball_x < 0:
        score2 += 1
        ball_x = window_width // 2
        ball_y = window_height // 2
        ball_speed_x = random.choice([-2, 2])
        ball_speed_y = random.choice([-2, 2])
    elif ball_x > window_width:
        score1 += 1
        ball_x = window_width // 2
        ball_y = window_height // 2
        ball_speed_x = random.choice([-2, 2])
        ball_speed_y = random.choice([-2, 2])

    # Clear the screen
    window.fill((0, 0, 0))

    # Draw the boards
    pygame.draw.rect(window, COLORS[0], (board1_x, board1_y, board_width, board_height))
    pygame.draw.rect(window, COLORS[0], (board2_x, board2_y, board_width, board_height))

    # Draw the ball
    pygame.draw.circle(window, COLORS[current_color_index], (ball_x, ball_y), ball_radius)

    # Draw the score board
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Player 1: {score1}  Player 2: {score2}", True, (255, 255, 255))
    window.blit(score_text, (window_width // 2 - score_text.get_width() // 2, 10))

    # Draw the current level text
    level_text = font.render(f"Level {current_level}: {LEVEL_COLORS[current_color_index]}", True, (255, 255, 255))
    window.blit(level_text, (window_width // 2 - level_text.get_width() // 2, 50))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
