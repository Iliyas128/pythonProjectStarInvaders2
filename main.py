import pygame
import random
import math
from pygame import mixer
from Noidea.Button import Button
# Initialize Pygame
pygame.init()



# Create the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Инициализация bullet_x и bullet_y глобально
bullet_x = 0
bullet_y = SCREEN_HEIGHT - 100  # Начальное положение, соответствующее позиции игрока

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
try:
    player_img = pygame.image.load('player.png').convert_alpha()
except Exception as e:
    print(f"Error loading player image: {e}")
player_x = SCREEN_WIDTH / 2 - 32
player_y = SCREEN_HEIGHT - 100
player_x_change = 0

# Level system
current_level = 1
enemies_defeated = 0
enemies_defeat_threshold = 5


def create_enemy():
    speed_increase = current_level * 0.2  # Reduce the multiplier for speed increase per level
    return {
        'img': pygame.image.load('enemy.png').convert_alpha(),
        'x': random.randint(0, SCREEN_WIDTH - 64),
        'y': random.randint(-150, -50),  # Start enemies off-screen or at the top
        'x_change': 0,  # Assuming enemies will only move vertically down
        'y_change': speed_increase * 0.5,
    }


enemies_per_level = 5
enemies = [create_enemy() for _ in range(enemies_per_level)]

# Bullet
try:
    bullet_img = pygame.image.load('bullet.png').convert_alpha()
except pygame.error:
    print("Error loading bullet image.")
# bullet_x = 0
# bullet_y = player_y
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
LEVEL_COMPLETED = 4
game_state = MENU


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, enemy_info):
    screen.blit(enemy_info['img'], (x, y))


def fire_bullet(x, y):
    global bullet_state, bullet_x, bullet_y  # Указываем, что используем глобальные переменные
    bullet_state = "fire"
    bullet_x = x
    bullet_y = y
    screen.blit(bullet_img, (bullet_x + 16, bullet_y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    return False


def update_level():
    global current_level, enemies_defeated, enemies, enemies_per_level, game_state
    if enemies_defeated >= enemies_defeat_threshold or not enemies:
        current_level += 1  # Исправлено с 10 на 1
        enemies_defeated = 0  # Reset the counter for the next level
        enemies_per_level += 2  # Optionally increase the number of enemies per level
        enemies = [create_enemy() for _ in range(enemies_per_level)]  # Repopulate enemies
        game_state = LEVEL_COMPLETED


def game_loop():
    global game_state, enemies
    game_state = RUNNING
    enemies = [create_enemy() for _ in range(enemies_per_level)]  # Recreate enemies for the new level
    main()


play_button = Button(150, 450, 100, 50, "Play", color=(0, 255, 0), highlight_color=(0, 200, 0), function=game_loop)


def quit_game():
    pygame.quit()
    quit()


def resume_game():
    global game_state
    game_state = RUNNING


def go_to_main_menu():
    global game_state
    game_state = MENU


quit_button = Button(350, 450, 100, 50, "Quit", color=(255, 0, 0), highlight_color=(200, 0, 0), function=quit_game)
# play_button = Button(150, 450, 100, 50, "Play", color=(0, 255, 0), highlight_color=(0, 200, 0), function=game_loop)
resume_button = Button(150, 450, 200, 50, "Resume", color=(0, 255, 0), highlight_color=(0, 200, 0),
                       function=resume_game)
# Assuming SCREEN_WIDTH and SCREEN_HEIGHT are the dimensions of your screen
# and that you want to center the buttons both horizontally and vertically
# with some space between them

button_width = 300  # The width of your buttons
button_height = 50  # The height of your buttons
button_space = 20  # The space between buttons

# Calculate the starting Y position of the first button so they are centered together vertically
total_buttons_height = (2 * button_height) + button_space
start_y_position = (SCREEN_HEIGHT - total_buttons_height) // 2

# Calculate the X position so that the buttons are centered horizontally
x_position = (SCREEN_WIDTH - button_width) // 2

# Now position the buttons using the calculated positions
continue_button = Button(x_position, start_y_position, button_width, button_height, "Continue", color=(0, 255, 0),
                         highlight_color=(0, 200, 0), function=game_loop)
main_menu_button = Button(x_position, start_y_position + button_height + button_space, button_width, button_height,
                          "Main Menu", color=(255, 0, 0), highlight_color=(200, 0, 0), function=go_to_main_menu)


def level_completed_screen():
    congrats_image = pygame.transform.scale(pygame.image.load('Congrats.jpg').convert_alpha(),
                                            (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(congrats_image, (0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render(f"You finished level {current_level - 1}", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150))
    continue_button.draw(screen)
    main_menu_button.draw(screen)


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
                play_button.function()
            elif quit_button.is_over(pygame.mouse.get_pos()):
                quit_button.function()
    pygame.display.update()


def pause_menu():
    global game_state
    while game_state == PAUSED:
        screen.fill((0, 0, 0))
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
def main():
    global game_state, bullet_y, bullet_state, player_x, score_value, enemies_defeated, player_x_change, bullet_x
    running = True
    player_x_change = 0  # Initialize player_x_change here to ensure it's defined before use

    while running:
        if game_state == MENU:
            main_menu()
        elif game_state == RUNNING:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_x_change = -2
                    elif event.key == pygame.K_RIGHT:
                        player_x_change = 2
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

            # Enemy drawing and collision detection
            for i, enemy_info in enumerate(enemies[:]):
                enemy_info['y'] += enemy_info['y_change']

                # Check if the enemy goes off the bottom of the screen
                if enemy_info['y'] >= SCREEN_HEIGHT - enemy_info['img'].get_height():
                    game_state = GAME_OVER  # Change game state to GAME_OVER
                    break  # Exit the loop, as the game is over

                # If the game is not over, draw the enemy
                enemy(enemy_info['x'], enemy_info['y'], enemy_info)

                # Check for collision with bullet
                collision = is_collision(enemy_info['x'], enemy_info['y'], bullet_x, bullet_y)
                if collision:
                    explosion_sound = mixer.Sound("explosion.wav")
                    explosion_sound.play()
                    bullet_y = player_y
                    bullet_state = "ready"
                    score_value += 1
                    enemies_defeated += 1
                    enemies.pop(i)  # Remove the enemy that was hit

            player_x += player_x_change
            if player_x <= 0:
                player_x = 0
            elif player_x >= SCREEN_WIDTH - 64:
                player_x = SCREEN_WIDTH - 64

            if bullet_state == "fire":
                fire_bullet(bullet_x, bullet_y)
                bullet_y -= bullet_y_change
            if bullet_y <= 0:
                bullet_y = player_y
                bullet_state = "ready"

            player(player_x, player_y)
            show_score(text_x, text_y)

            if not enemies:  # Check if all enemies are defeated to proceed to the next level
                update_level()

            pygame.display.update()
        elif game_state == PAUSED:
            pause_menu()
        elif game_state == LEVEL_COMPLETED:
            level_completed_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_over(pygame.mouse.get_pos()):
                        continue_button.handle_event(event)
                    elif main_menu_button.is_over(pygame.mouse.get_pos()):
                        main_menu_button.handle_event(event)
            pygame.display.update()
            # kogda game over
        if game_state == GAME_OVER:
            game_over_text()  # Function to display the game over message
            restart_button.draw(screen)
            quitt_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.is_over(pygame.mouse.get_pos()):
                        restart_button.handle_event(event)
                    elif quitt_button.is_over(pygame.mouse.get_pos()):
                        quitt_button.handle_event(event)


        pygame.display.update()


def restart_game():
    global game_state, score_value, player_x, player_y, enemies, current_level
    score_value = 0
    player_x = SCREEN_WIDTH / 2 - 32
    player_y = SCREEN_HEIGHT - 100
    current_level = 1
    enemies = [create_enemy() for _ in range(enemies_per_level)]
    game_state = RUNNING


restart_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 300, 50, "Restart", color=(0, 255, 0),
                        highlight_color=(0, 200, 0), function=restart_game)
quitt_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 120, 300, 50, "Quit", color=(255, 0, 0),
                      highlight_color=(200, 0, 0), function=quit_game)

if __name__ == "__main__":
    main()
