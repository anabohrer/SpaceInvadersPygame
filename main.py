import math
import random

import pygame
from pygame import mixer
from pygame import time

# Initialize the pygame
pygame.init()


# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background sound
mixer.music.load('sounds/background.mp3')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# Player - Load the image and display the coordinates of the player on the screen
playerImage = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0


# Enemy - Load the image and display the coordinates of the enemy on the screen
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_num = 6

for i in range(enemies_num):
    enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# Laser - Load the image and display the coordinates of the laser on the screen
# Ready - You can't see the laser on the screen
# Fire - The laser is currently moving
laserImage = pygame.image.load("laser.png")
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 1
laser_state = "ready"

# Collision
collisionImage = pygame.image.load("collision.png")

# Score
score_value = 0
font = pygame.font.Font('fonts/ARCADE_I.TTF', 25)

textX = 10
textY = 10

# Game Over text
game_over_font = pygame.font.Font('fonts/ARCADE_I.TTF', 50)


def show_game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))
    mixer.music.stop()
    game_over_sound = mixer.Sound('sounds/game-over.wav')
    game_over_sound.play()


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # Draw the image on the screen
    screen.blit(playerImage, (x, y))


def enemy(x, y, index):
    # Draw the image on the screen
    screen.blit(enemyImage[index], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImage, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, laser_x, laser_y):
    distance = math.sqrt((math.pow(enemy_x - laser_x, 2)) + (math.pow(enemy_y - laser_y, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_collision(x, y):
    screen.blit(collisionImage, (x, y))
    collision_sound = mixer.Sound('sounds/explosion.wav')
    collision_sound.play()
    rect = pygame.Rect(x, y, collisionImage.get_width(), collisionImage.get_width())
    pygame.display.update(rect)
    time.wait(100)


# Game loop
running = True
while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laser_sound = mixer.Sound('sounds/laser.wav')
                    laser_sound.play()
                    # Get the current coordinate of the spaceship
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship, so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(enemies_num):

        # Game over
        if enemyY[i] > 200:
            for j in range(enemies_num):
                enemyY[j] = 2000
            show_game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            show_collision(enemyX[i], enemyY[i])
            laserY = 480
            laser_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement

    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
