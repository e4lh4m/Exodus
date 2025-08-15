import math
import random
import sys
import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('Gemini_Generated_Image_dxio2bdxio2bdxio.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Exodus")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-ship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
player_health = 3
player_frozen = False
freeze_start_time = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ghost.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)  # slower speed
    enemyY_change.append(40)

# Bullet (Player)
bulletImg = pygame.image.load('fire.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Bullet (Enemy)
enemy_bulletImg = pygame.image.load('fire.png')  # reuse bullet image
enemy_bulletX = []
enemy_bulletY = []
enemy_bullet_change = 5
enemy_bullet_state = []  # "ready" or "fire"

for _ in range(num_of_enemies):
    enemy_bulletX.append(0)
    enemy_bulletY.append(0)
    enemy_bullet_state.append("ready")

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_health():
    health_text = font.render("Health : " + str(player_health), True, (255, 0, 0))
    screen.blit(health_text, (650, 10))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 10, y + 10))

def fire_enemy_bullet(i, x, y):
    enemy_bullet_state[i] = "fire"
    enemy_bulletX[i] = x
    enemy_bulletY[i] = y

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < 27

def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = (0, 128, 255) if x + width > mouse[0] > x and y + height > mouse[1] > y else (0, 100, 200)
    pygame.draw.rect(screen, color, (x, y, width, height))

    button_font = pygame.font.Font('freesansbold.ttf', 32)
    text_surface = button_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

    if click[0] == 1 and x + width > mouse[0] > x and y + height > mouse[1] > y:
        if action:
            action()

def restart_game():
    global playerX, playerY, playerX_change, playerY_change, bulletX, bulletY, bullet_state, score_value, player_health
    global enemyX, enemyY, enemy_bullet_state

    playerX = 370
    playerY = 480
    playerX_change = 0
    playerY_change = 0
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    score_value = 0
    player_health = 3

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemy_bullet_state[i] = "ready"

    main_game_loop()

def exit_game():
    pygame.quit()
    sys.exit()

def main_game_loop():
    global playerX, playerY, playerX_change, playerY_change, bulletX, bulletY, bullet_state, score_value
    global player_health, player_frozen, freeze_start_time

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Keyboard controls
            if event.type == pygame.KEYDOWN and not player_frozen:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    playerX_change = -5
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    playerX_change = 5
                if event.key in (pygame.K_UP, pygame.K_w):
                    playerY_change = -5
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    playerY_change = 5
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    playerX_change = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                    playerY_change = 0

        # Unfreeze player after 1 second
        if player_frozen and pygame.time.get_ticks() - freeze_start_time > 1000:
            player_frozen = False

        # Move Player
        playerX += playerX_change
        playerY += playerY_change
        playerX = max(0, min(playerX, 736))
        playerY = max(0, min(playerY, 536))

        # Move Enemies
        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                pygame.display.update()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    screen.blit(background, (0, 0))
                    game_over_text()
                    draw_button("Restart", 250, 350, 120, 50, restart_game)
                    draw_button("Exit", 430, 350, 120, 50, exit_game)
                    pygame.display.update()

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= 736:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]

            # Enemy shooting randomly
            if enemy_bullet_state[i] == "ready" and random.randint(0, 100) < 2:
                fire_enemy_bullet(i, enemyX[i], enemyY[i])

            # Enemy bullet movement
            if enemy_bullet_state[i] == "fire":
                screen.blit(enemy_bulletImg, (enemy_bulletX[i] + 10, enemy_bulletY[i] + 10))
                enemy_bulletY[i] += enemy_bullet_change
                if enemy_bulletY[i] > 600:
                    enemy_bullet_state[i] = "ready"

                # Check collision with player
                if isCollision(playerX, playerY, enemy_bulletX[i], enemy_bulletY[i]):
                    enemy_bullet_state[i] = "ready"
                    player_health -= 1
                    player_frozen = True
                    freeze_start_time = pygame.time.get_ticks()
                    if player_health <= 0:
                        for j in range(num_of_enemies):
                            enemyY[j] = 2000

            # Collision with player bullet
            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        show_health()
        pygame.display.update()

# Start the game
main_game_loop()
