import pygame
import random
import math
from pygame import mixer

# init pygame
pygame.init()

# CREATE SCREEN
screen = pygame.display.set_mode((800, 600))

# title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('images/logo.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('images/background.png')
# background sound
mixer.music.load('music/background.wav')
mixer.music.play(-1)
# player
playerImg = pygame.image.load('images/player.png')
playerX = 360
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemy = 6
for i in range(number_of_enemy):
    enemyImg.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# ready -cant see the bullet
# fire - bullet is moving
# bullet
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y))


# collision
def iscollision(enemyX, enemyY, bulletX, bulletY):
    d = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if d < 27:
        return True
    else:
        return False


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

gameover = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score :' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    gover = gameover.render('GAME OVER', True, (255, 255, 255))
    screen.blit(gover, (200, 250))


# game loop
running = True
while running:
    # RGB for background
    screen.fill((50, 100, 255))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # to quit game
        if event.type == pygame.QUIT:
            running = False
        # To check keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('music/shoot.wav')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # check boundary so it wont go out of bound
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # enemy movement
    for i in range(number_of_enemy):

        if enemyY[i] > 440:
            for j in range(number_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 4
        elif enemyX[i] >= 736:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -4
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 150)
            explosion_sound = mixer.Sound('music/explosion.wav')
            explosion_sound.play()
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    # COLLSION
    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
