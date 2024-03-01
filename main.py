import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.transform.scale(pygame.image.load('DeathStar.jpg').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('player.png').convert_alpha()
player_x = SCREEN_WIDTH / 2 - 32 # centering
player_y = SCREEN_HEIGHT -100
player_x_change = 0

# Enemy
enemy_img = pygame.image.load('enemy.png').convert_alpha()
enemy_x = random.randint(0, SCREEN_WIDTH - 64 )
enemy_y = random.randint(50, 150)
enemy_x_change = 2
enemy_y_change = 40

# Bullet
bullet_img = pygame.image.load('bullet.png').convert_alpha()
bullet_x = 0
bullet_y = player_y
bullet_x_change = 0
bullet_y_change = 5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Game States
MENU = 0
RUNNING = 1
PAUSED = 2
GAME_OVER = 3
game_state = MENU


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse= pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1]>y:
        pygame.draw.rect(screen, active_color,(x,y,width,height))
        if click[0] ==1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color,(x,y,width, height))

    small_text = pygame.font.Font("freesansbold.ttf",20)
    text_surf = small_text.render(text ,True,(255,255,255))
    text_rect = text_surf.get_rect()
    text_rect.center = ((x+width/2), (y+height/2))
    screen.blit(text_surf, text_rect)

def game_loop():
    global game_state
    game_state = RUNNING

def quit_game():
    pygame.quit()
    quit()
def main_menu():
    global game_state
    while game_state == MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        draw_button("Play", 150, 450, 100, 50, (0, 255, 0), (0, 200, 0), game_loop)
        draw_button("Quit", 350, 450, 100, 50, (255, 0, 0), (200, 0, 0), quit_game)

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_state = RUNNING
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()


def pause_menu():
    global game_state
    pause_text = over_font.render("Paused", True, (255, 255, 255))
    screen.blit(pause_text, (540, SCREEN_HEIGHT / 2 - 50))
    pygame.display.update()

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    game_state = MENU
                    paused = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()


# Main game loop
running = True
while running:
    if game_state == MENU:
        main_menu()
    elif game_state == RUNNING:
        # Game running logic
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -5
                elif event.key == pygame.K_RIGHT:
                    player_x_change = 5
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound("laser.wav")
                        bullet_sound.play()
                        bullet_x = player_x + 16
                        fire_bullet(bullet_x, bullet_y)
                elif event.key == pygame.K_p:
                    game_state = PAUSED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= SCREEN_WIDTH-64:
            player_x = SCREEN_WIDTH-64

        # Enemy movement
        enemy_x += enemy_x_change
        if enemy_x <= 0 or enemy_x >= SCREEN_WIDTH - 64:
            enemy_x_change = -enemy_x_change
            enemy_y += enemy_y_change

        # Collision detection
        collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
        if collision:
            bullet_y = player_y
            bullet_state = "ready"
            score_value += 1
            enemy_x = random.randint(0, SCREEN_WIDTH - 64)
            enemy_y = random.randint(50, 150)
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()

        # Bullet movement
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = player_y
            bullet_state = "ready"

        player(player_x, player_y)
        enemy(enemy_x, enemy_y)
        show_score(text_x, text_y)
        pygame.display.update()
    elif game_state == PAUSED:
        pause_menu()
