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
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Car Driving Game')

# Load car image
car_image = pygame.image.load('C:/Users/Vaishu/Downloads/Untitled design.png')
car_width, car_height = car_image.get_size()

# Function to draw car
def draw_car(surface, x, y):
    surface.blit(car_image, (x, y))

# Player properties
car_x = (SCREEN_WIDTH - car_width) // 2
car_y = SCREEN_HEIGHT - car_height - 10
car_speed = 10
car_velocity = 0

# Obstacle properties
obstacle_width = 50
obstacle_height = 100
obstacles = [{'x': random.randint(0, SCREEN_WIDTH - obstacle_width), 'y': -obstacle_height}]

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
    title_text = menu_font.render('Car Driving Game', True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

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

obstacle_speed = difficulty_levels[selected_difficulty]

# Main game loop
running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Move car left or right
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < SCREEN_WIDTH - car_width:
            car_x += car_speed

        # Adjust car speed with brakes and acceleration
        if keys[pygame.K_UP]:
            car_velocity = min(car_velocity + 1, car_speed)
        elif keys[pygame.K_DOWN]:
            car_velocity = max(car_velocity - 1, -car_speed)
        else:
            car_velocity = max(0, car_velocity - 1)

        car_y -= car_velocity

        # Move the obstacles
        for obstacle in obstacles:
            obstacle['y'] += obstacle_speed

        # Check for collision
        for obstacle in obstacles:
            if (obstacle['y'] + obstacle_height >= car_y and
                car_x <= obstacle['x'] <= car_x + car_width) or \
               (obstacle['y'] + obstacle_height >= car_y and
                car_x <= obstacle['x'] + obstacle_width <= car_x + car_width):
                running = False

        # Check if the obstacles move off the screen
        for obstacle in obstacles:
            if obstacle['y'] > SCREEN_HEIGHT:
                score += 1
                obstacles.remove(obstacle)
                obstacles.append({'x': random.randint(0, SCREEN_WIDTH - obstacle_width), 'y': -obstacle_height})
                obstacle_speed += 0.5  # Increase speed slightly after each pass

        # Add more obstacles as score increases
        if score % 5 == 0 and len(obstacles) < score // 5 + 1:
            obstacles.append({'x': random.randint(0, SCREEN_WIDTH - obstacle_width), 'y': -obstacle_height})

        # Clear the screen
        screen.fill(SKY_BLUE)

        # Draw the road
        pygame.draw.rect(screen, ROAD_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(screen, LINE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)

        # Draw the car
        draw_car(screen, car_x, car_y)

        # Draw the obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, (obstacle['x'], obstacle['y'], obstacle_width, obstacle_height))

        # Draw the score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    else:
        # Pause screen
        screen.fill(SKY_BLUE)
        pause_text = font.render("Game Paused. Press 'P' to resume.", True, BLACK)
        screen.blit(pause_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        clock.tick(15)  # Lower frame rate while paused

# Game over screen
screen.fill(SKY_BLUE)
game_over_text = font.render(f'Game Over! Final Score: {score}', True, BLACK)
screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
pygame.display.flip()

# Wait for a few seconds before closing
pygame.time.wait(3000)

pygame.quit()
sys.exit()
