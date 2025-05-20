import pygame

import random
import math
from pygame import mixer

pygame.init()

# Load the custom font
font_path = "font.ttf"  # Path to your .ttf font file
font = pygame.font.Font(font_path, 60)  # Load the font with a size of 60

# Set up the screen and other resources
background = pygame.image.load("background.png")
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Planet Spenzy")
icon = pygame.image.load("planet-ringed.png")
pygame.display.set_icon(icon)

# Load background music
mixer.music.load("background.wav")
mixer.music.play(-1)  # Play music in a loop

# Player setup
playerimg = pygame.image.load("spaceship.png")
playerimg = pygame.transform.scale(playerimg, (60, 60))
playerx = 370
playerY = 480
playerx_change = 0

# Initialize lists to hold enemy data
enemyimg = []
enemyx = []
enemyY = []
enemyx_change = []
enemyY_change = []
num_of_enemies = 6

# Bullet setup
bulletimg = pygame.image.load("bullet.png")
bulletimg = pygame.transform.scale(bulletimg, (20, 20))  # Ensure proper scaling
bulletx = 0
bulletY = 480
bulletx_change = 0
bulletY_change = 10
bullet_state = "ready"  # Bullet is not on the screen initially

# Score and level setup
score_value = 0
level = 1
textx = 10
textY = 10

# Game Over state
game_over = False  # Variable to track game over state

# Track level start time for displaying level message
level_start_time = 0  # Initialize the time variable

# High Score setup (persistent high score across sessions)
high_score = 0

def load_high_score():
    global high_score
    try:
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0

def save_high_score():
    global high_score
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))  # Render the score
    screen.blit(score, (x, y))  # Display it on the screen

def show_high_score(x, y):
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))  # Render high score
    screen.blit(high_score_text, (x, y))  # Display it on the screen

def show_level(x, y):
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))  # Render the level
    screen.blit(level_text, (x, y))  # Display it on the screen

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(i):  # Pass index to handle multiple enemies
    screen.blit(enemyimg[i], (enemyx[i], enemyY[i]))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y - 20))  # Adjust the bullet position slightly above the player

def isCollision(enemyx, enemyY, bulletx, bulletY):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def game_over_screen():
    # Display Game Over screen
    game_over_font = pygame.font.Font(font_path, 64)  # Use the custom font here
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    restart_text = game_over_font.render("Press R to Restart", True, (255, 0, 0))

    # Display "GAME OVER" text
    screen.blit(game_over_text, (310, 250))

    # Display "Press R to Restart" on the next line
    screen.blit(restart_text, (280, 350))  # Adjust y position to place it below the "GAME OVER" text

    # Display score and high score
    score_font = pygame.font.Font(font_path, 60)  # Use the custom font for score
    score_text = score_font.render(f"Your Score: {score_value}", True, (255, 255, 255))
    screen.blit(score_text, (320, 300))

    show_high_score(10, 60)  # Display the high score at the top-left corner

def restart_game():
    global playerx, playerY, playerx_change, bullet_state, bulletY, score_value, level, enemyx, enemyY, enemyx_change, enemyY_change, enemyimg
    playerx = 370
    playerY = 480
    playerx_change = 0
    bullet_state = "ready"
    bulletY = 480
    score_value = 0
    level = 1
    num_of_enemies = 6
    
    # Clear existing enemies before restarting
    enemyx = []
    enemyY = []
    enemyx_change = []
    enemyY_change = []
    enemyimg = []  # Reset the list to avoid multiple instances

    # Reinitialize the enemies for the new game
    initialize_enemies()

def next_level():
    global level, num_of_enemies, enemyx_change, enemyY_change, enemyimg, enemyx, enemyY, level_start_time

    level += 1
    level_start_time = pygame.time.get_ticks()  # Store the time when the level changes

    # Calculate the max number of enemies for the current level
    max_enemies = 6 + level  # Max number of enemies based on the level

    # If the current number of enemies is less than the max, spawn more
    while len(enemyx) < max_enemies:
        enemyimg.append(pygame.image.load("play1.png"))
        enemyimg[len(enemyimg) - 1] = pygame.transform.scale(enemyimg[len(enemyimg) - 1], (50, 50))
        enemyx.append(random.randint(0, 750))
        enemyY.append(random.randint(50, 150))
        enemyx_change.append(random.randint(3, 7))  # Random speed for each new enemy
        enemyY_change.append(0.1 * level)  # Increase speed as the level increases

def initialize_enemies():
    global enemyx, enemyY, enemyx_change, enemyY_change, enemyimg
    for i in range(num_of_enemies):
        enemyimg.append(pygame.image.load("play1.png"))
        enemyimg[i] = pygame.transform.scale(enemyimg[i], (50, 50))
        enemyx.append(random.randint(0, 750))
        enemyY.append(random.randint(50, 150))
        enemyx_change.append(0.1)
        enemyY_change.append(0.2)

running = True

# Load the high score from the file
load_high_score()

# Initialize enemies at the start
initialize_enemies()

while running:
    screen.fill((36, 108, 202))  # Background color
    screen.blit(background, (0, 0))  # Draw the background

    if game_over:  # Show game over screen
        game_over_screen()

        # Update high score if necessary
        if score_value > high_score:
            high_score = score_value
            save_high_score()

        # Check for restart input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to restart
                    restart_game()
                    game_over = False  # Reset game over state
                elif event.key == pygame.K_q:  # Press 'Q' to quit
                    running = False

    else:
        player(playerx, playerY)  # Draw the player

        # Display the level for 1 second after level increase
        if pygame.time.get_ticks() - level_start_time < 1000:  # 1000 milliseconds = 1 second
            level_text = font.render(f"LEVEL: {level}", True, (255, 255, 255))
            screen.blit(level_text, (350, 300))

        # Update enemy positions and draw them
        for i in range(len(enemyx)):
            enemy(i)  # Display the enemy at its current position

            if enemyY[i] > 420:  # Game over condition
                game_over = True 
                break

            enemyx[i] += enemyx_change[i]
            enemyY[i] += enemyY_change[i]

            # Enemy movement logic
            if enemyx[i] <= 0:
                enemyx_change[i] = 2
                enemyY_change[i] = 0.1 * level  # Increase speed with level
            elif enemyx[i] >= 750:
                enemyx_change[i] = -5

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerx_change = -5
                if event.key == pygame.K_RIGHT:
                    playerx_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":  # Only fire the bullet if it is ready
                        bulletx = playerx  # Set bullet position to the player position
                        fire_bullet(bulletx, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    playerx_change = 0
                if event.key == pygame.K_RIGHT:
                    playerx_change = 0

        # Update player position
        if not game_over:
            playerx += playerx_change

            # Prevent the player from moving off the screen
            if playerx <= 0:
                playerx = 0
            elif playerx >= 750:
                playerx = 750

            # Bullet movement logic
            if bullet_state == "fire":
                fire_bullet(bulletx, bulletY)
                bulletY -= bulletY_change  # Move the bullet upwards

                # Reset bullet when it goes off-screen
                if bulletY <= 0:
                    bullet_state = "ready"
                    bulletY = 480  # Reset bullet to initial position below the player

            # Collision detection for multiple enemies
            for i in range(len(enemyx)):
                collision = isCollision(enemyx[i], enemyY[i], bulletx, bulletY)
                if collision:
                    explosion_sound = mixer.Sound('explosion.wav')  # Play explosion sound
                    explosion_sound.play()
                    bulletY = 480
                    bullet_state = "ready"
                    bullet_sound = mixer.Sound('laser.wav')  # Play laser sound
                    bullet_sound.play() 
                    score_value += 1
                    print(f"Score: {score_value}")
                    import os  # For checking file existence

                    import os  # For checking file existence

                    # Reset enemy position after being hit
                    enemyx[i] = random.randint(0, 750)  # Ensuring the enemy is within screen bounds
                    enemyY[i] = random.randint(50, 150)  # Random vertical position within range

                    # Check if level should increase
                    if score_value % 10== 0 and score_value != 0:  # Increase level after every 10 points
                        next_level()

        # Calling show_score function to display the score
        if not game_over:
            show_score(textx, textY)
            show_level(700, 10)  # Display level at the top-right corner

    pygame.display.update()  # Refresh the screen

pygame.quit()
