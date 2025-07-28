# ================================
# IMPORTS AND INITIALIZATION
# ================================
import pygame
import random
import math

pygame.init()




# ================================
# SCREEN SETUP
# ================================
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EXODUS")
icon = pygame.image.load('spacecraft.png')
pygame.display.set_icon(icon)




# ================================
# ASSET LOADING
# ================================
background = pygame.transform.scale(pygame.image.load('bg3.png'), (WIDTH, HEIGHT))
player_img = pygame.transform.scale(pygame.image.load('jet.png'), (60, 60))
bullet_img = pygame.transform.scale(pygame.image.load('bullet.png'), (20, 40))
alien_img = pygame.transform.scale(pygame.image.load('alien.png'), (60, 60))




# ================================
# PLAYER SETUP
# ================================
playerX = WIDTH // 2
playerY = HEIGHT - 150
playerX_change = 0
playerY_change = 0
player_speed = 5
player_hits = 0
player_damaged = False
damage_timer = 0




# ================================
# BULLET SETUP
# ================================
bulletX = 0
bulletY = playerY
bulletY_change = 70
bullet_state = "ready"
bullet_delay = 50
last_bullet_time = 0




# ================================
# ALIEN SETUP
# ================================
alien_width, alien_height = 60, 60
alienX = []
alienY = []
alienX_change = []
alienY_change = 100




# ================================
# SCORE AND LIVES
# ================================
score = 0
high_score = 0
lives = 3
font = pygame.font.Font(pygame.font.get_default_font(), 25)




# ================================
# GAME STATE SETUP
# ================================
START, PLAYING, GAME_OVER = 0, 1, 2
game_state = START




# ================================
# DIFFICULTY SETTINGS
# ================================
difficulty = "Medium"
difficulty_settings = {
    "Easy": 30,
    "Medium": 60,
    "Hard": 100
}




# ================================
# UTILITY FUNCTIONS
# ================================
def is_collision(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1) < 40



def player(x, y):
    screen.blit(player_img, (x, y))



def alien(x, y):
    screen.blit(alien_img, (x, y))



def fire_bullet(x, y):
    global bullet_state, last_bullet_time
    bullet_state = "fire"
    last_bullet_time = pygame.time.get_ticks()
    bullet_x_pos = x + player_img.get_width()//2 - bullet_img.get_width()//2
    bullet_y_pos = y - bullet_img.get_height()
    screen.blit(bullet_img, (bullet_x_pos, bullet_y_pos))



def show_info():
    pygame.draw.rect(screen, (10, 10, 10), (0, 0, WIDTH, 40))
    pygame.draw.line(screen, (255, 255, 255), (0, 40), (WIDTH, 40), 2)
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (30, 10))
    screen.blit(font.render(f"High Score: {high_score}", True, (255, 215, 0)), (WIDTH // 2 - 100, 10))
    screen.blit(font.render(f"Lives: {lives}", True, (0, 255, 0)), (WIDTH - 180, 10))

def show_start_screen():
    title_font = pygame.font.Font(pygame.font.get_default_font(), 100)
    subtitle_font = pygame.font.Font(pygame.font.get_default_font(), 40)
    easy = subtitle_font.render("1 - Easy", True, (255, 255, 255))
    medium = subtitle_font.render("2 - Medium", True, (255, 255, 255))
    hard = subtitle_font.render("3 - Hard", True, (255, 255, 255))
    title = title_font.render("EXODUS", True, (0, 255, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150))
    screen.blit(easy, (WIDTH // 2 - easy.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(medium, (WIDTH // 2 - medium.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(hard, (WIDTH // 2 - hard.get_width() // 2, HEIGHT // 2 + 80))

def show_game_over():
    game_over_font = pygame.font.Font(pygame.font.get_default_font(), 70)
    over_text = game_over_font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))

# ================================
# MAIN GAME LOOP
# ================================
running = True
while running:
    screen.blit(background, (0, 0))

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == START:
                if event.key == pygame.K_1:
                    difficulty = "Easy"
                    num_aliens = difficulty_settings[difficulty]
                    game_state = PLAYING
                if event.key == pygame.K_2:
                    difficulty = "Medium"
                    num_aliens = difficulty_settings[difficulty]
                    game_state = PLAYING
                if event.key == pygame.K_3:
                    difficulty = "Hard"
                    num_aliens = difficulty_settings[difficulty]
                    game_state = PLAYING

                alienX = [random.randint(0, WIDTH - alien_width) for _ in range(num_aliens)]
                alienY = [random.randint(50, 300) for _ in range(num_aliens)]
                alienX_change = [random.choice([-6, 6]) for _ in range(num_aliens)]

            if game_state == GAME_OVER and event.key == pygame.K_r:
                game_state = START
                score = 0
                lives = 3
                player_hits = 0

            if game_state == PLAYING:
                if event.key == pygame.K_LEFT:
                    playerX_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    playerX_change = player_speed
                if event.key == pygame.K_UP:
                    playerY_change = -player_speed
                if event.key == pygame.K_DOWN:
                    playerY_change = player_speed

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                playerY_change = 0

    # Game States
    if game_state == START:
        show_start_screen()

    elif game_state == PLAYING:
        # Update Player
        playerX += playerX_change
        playerY += playerY_change
        playerX = max(0, min(playerX, WIDTH - 60))
        playerY = max(0, min(playerY, HEIGHT - 60))
        player(playerX, playerY)

        # Damage Effect
        if player_damaged:
            if pygame.time.get_ticks() - damage_timer < 300:
                pygame.draw.rect(screen, (255, 0, 0), (playerX, playerY, 60, 60), 3)
            else:
                player_damaged = False

        # Bullet Movement
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and bullet_state == "ready" and pygame.time.get_ticks() - last_bullet_time > bullet_delay:
            bulletX = playerX
            bulletY = playerY
            fire_bullet(bulletX, bulletY)

        # Alien Movement and Collision
        for i in range(num_aliens):
            alienX[i] += alienX_change[i]

            if alienX[i] <= 0 or alienX[i] >= WIDTH - alien_width:
                alienX_change[i] *= -1
                alienY[i] += alienY_change

            if is_collision(alienX[i], alienY[i], bulletX, bulletY):
                bulletY = playerY
                bullet_state = "ready"
                score += 1
                alienX[i] = random.randint(0, WIDTH - alien_width)
                alienY[i] = random.randint(50, 300)

            if is_collision(alienX[i], alienY[i], playerX, playerY):
                if not player_damaged:
                    player_hits += 1
                    alienX[i] = random.randint(0, WIDTH - alien_width)
                    alienY[i] = random.randint(50, 300)
                    player_damaged = True
                    damage_timer = pygame.time.get_ticks()

                    if player_hits >= 3:
                        lives -= 1
                        player_hits = 0

            alien(alienX[i], alienY[i])

        if lives <= 0:
            if score > high_score:
                high_score = score
            game_state = GAME_OVER

        show_info()

    elif game_state == GAME_OVER:
        show_game_over()

    # Display Update
    pygame.display.update()
