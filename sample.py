import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Falling Objects')

# Function to draw avatar
def draw_avatar(surface, x, y):
    # Draw head
    pygame.draw.circle(surface, BLACK, (x + 50, y + 50), 30)
    # Draw body
    pygame.draw.rect(surface, BLACK, (x + 35, y + 80, 30, 50))
    # Draw arms
    pygame.draw.line(surface, BLACK, (x + 15, y + 100), (x + 85, y + 100), 5)
    # Draw legs
    pygame.draw.line(surface, BLACK, (x + 45, y + 130), (x + 30, y + 160), 5)
    pygame.draw.line(surface, BLACK, (x + 55, y + 130), (x + 70, y + 160), 5)

# Player properties
player_width = 100
player_height = 160
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 10

# Falling object properties
object_width = 20
object_height = 20
object_x = random.randint(0, SCREEN_WIDTH - object_width)
object_y = 0

# Game variables
score = 0
missed = 0

# Font setup
font = pygame.font.Font(None, 36)

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Difficulty levels
difficulty_levels = {
    'easy': 3,
    'medium': 5,
    'hard': 8
}

# Function to show the main menu
def show_menu():
    screen.fill(SKY_BLUE)
    menu_font = pygame.font.Font(None, 48)
    title_text = menu_font.render('Catch the Falling Objects', True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4))

    easy_text = menu_font.render('1. Easy', True, BLACK)
    medium_text = menu_font.render('2. Medium', True, BLACK)
    hard_text = menu_font.render('3. Hard', True, BLACK)

    screen.blit(easy_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    screen.blit(medium_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 50))
    screen.blit(hard_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 100))

    pygame.display.flip()

# Main menu loop
selected_difficulty = None
while selected_difficulty is None:
    show_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_difficulty = 'easy'
            elif event.key == pygame.K_2:
                selected_difficulty = 'medium'
            elif event.key == pygame.K_3:
                selected_difficulty = 'hard'

object_speed = difficulty_levels[selected_difficulty]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Move player left or right
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # Move the falling object
    object_y += object_speed

    # Check for collision
    if (object_y + object_height >= player_y and
        player_x <= object_x <= player_x + player_width):
        score += 1
        object_x = random.randint(0, SCREEN_WIDTH - object_width)
        object_y = 0
        object_speed += 0.5  # Increase speed slightly after each catch

    # Check if the object falls off the screen
    if object_y > SCREEN_HEIGHT:
        missed += 1
        running = False

    # Clear the screen
    screen.fill(SKY_BLUE)

    # Draw the player
    draw_avatar(screen, player_x, player_y)

    # Draw the falling object
    pygame.draw.circle(screen, RED, (object_x, object_y), 10)

    # Draw the score
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over screen
screen.fill(SKY_BLUE)
game_over_text = font.render(f'Game Over! Final Score: {score}', True, BLACK)
screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
pygame.display.flip()

# Wait for a few seconds before closing
pygame.time.wait(3000)

pygame.quit()
sys.exit()
