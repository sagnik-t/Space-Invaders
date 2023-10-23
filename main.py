import pygame
import random
import math

# initialize pygame
pygame.init()
# width by height
screen = pygame.display.set_mode((800, 600))
running = True

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('Assets/spaceship.png')
pygame.display.set_icon(icon)

# player icon
player_img = pygame.image.load('Assets/playericon.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('Assets/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(30)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# bullet
bullet_img = pygame.image.load("Assets/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = -7
bullet_state = 'ready'


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fired'
    screen.blit(bullet_img, (x + 15, y + 10))


# colliosion detection
def is_Collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# game over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


# main game loop for display
while running:
    screen.fill((25, 25, 112))
    background = pygame.image.load('Assets/background.png')
    screen.blit(background, (0, 0))
    # sustaining the display
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
                right_key = True
                left_key = False
            elif event.key == pygame.K_LEFT:
                playerX_change = -4
                left_key = True
                right_key = False
            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Smoothening the motion
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if left_key == True:
                    playerX_change = -4
                else:
                    playerX_change = 0
                    right_key = False

            if event.key == pygame.K_LEFT:
                if right_key == True:
                    playerX_change = 4
                else:
                    playerX_change = 0
                    left_key = False
    # player boundaries
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    # enemy movement and boundaries
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i], i)

        # collision
        collison = is_Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison == True:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fired':
        bulletY += bulletY_change
        fire_bullet(bulletX, bulletY)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
