import pygame
import random
import math
from pygame import mixer
from NoIdea import Button

# Initialize Pygame
pygame.init()

class Button:
    def __init__(self, x, y, width, height, text='', color=(73, 73, 73), highlight_color=(189, 189, 189),
                 function=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.highlight_color = highlight_color
        self.function = function

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color if not self.is_over(pygame.mouse.get_pos()) else self.highlight_color,
                         (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(pygame.mouse.get_pos()):
                if self.function:
                    self.function()




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

def is_over(self, pos):
    # Pos is the mouse position or a tuple of (x,y) coordinates
    if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
        print("Mouse is over the button.")
        return True
    return False


def game_loop():
    global game_state
    game_state = RUNNING

def quit_game():
    pygame.quit()
    quit()

def resume_game():
    global game_state
    game_state = RUNNING  # This resumes the game

def go_to_main_menu():
    global game_state
    game_state = MENU # This takes the player back to the main menu




quit_button = Button(350, 450, 100, 50, "Quit", color=(255, 0, 0), highlight_color=(200, 0, 0), function=quit_game)
play_button = Button(150, 450, 100, 50, "Play", color=(0, 255, 0), highlight_color=(0, 200, 0), function=game_loop)

resume_button = Button(150, 450, 200, 50, "Resume", color=(0, 255, 0), highlight_color=(0, 200, 0), function=resume_game)
main_menu_button = Button(400, 450, 300, 50, "Main Menu", color=(255, 0, 0), highlight_color=(200, 0, 0), function=go_to_main_menu)


def main_menu():
    global game_state
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    play_button.draw(screen)
    quit_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.is_over(pygame.mouse.get_pos()):
                play_button.function()  # Directly call the function
            elif quit_button.is_over(pygame.mouse.get_pos()):
                quit_button.function()  # Directly call the function

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
    while game_state == PAUSED:
        screen.fill((0, 0, 0))  # Or use a more appropriate background
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.is_over(pygame.mouse.get_pos()):
                    resume_button.handle_event(event)
                if main_menu_button.is_over(pygame.mouse.get_pos()):
                    main_menu_button.handle_event(event)

        resume_button.draw(screen)
        main_menu_button.draw(screen)

        pygame.display.update()





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
                elif event.key == pygame.K_ESCAPE:
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
