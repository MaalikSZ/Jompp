import pygame
from pygame.locals import *

pygame.init()

game_width = 800
game_height = 600
game_display = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Jompp Alpha")

BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

player_width = 40
player_height = 40
player_x = 0
player_y = game_height - player_height

obstacles = [
    {"x": 100, "y": game_height - 40, "width": 80, "height": 30},
    {"x": 200, "y": game_height - 80, "width": 80, "height": 30},
    {"x": 300, "y": game_height - 60, "width": 80, "height": 30},
    {"x": 400, "y": game_height - 100, "width": 80, "height": 30}
]

coins = [
    {"x": 150, "y": game_height - 60, "width": 20, "height": 20},
    {"x": 250, "y": game_height - 80, "width": 20, "height": 20}
]

level = 1

font = pygame.font.Font(None, 18)

clock = pygame.time.Clock()

moving_left = False
moving_right = False
is_jumping = False
jump_height = 0

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    game_display.blit(text_surface, text_rect)

def draw_player():
    pygame.draw.rect(game_display, BLUE, (player_x, player_y, player_width, player_height))

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(game_display, RED, (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

def draw_coins():
    for coin in coins:
        pygame.draw.rect(game_display, YELLOW, (coin["x"], coin["y"], coin["width"], coin["height"]))

def check_collision(rect1, rect2):
    if (
        rect1["x"] < rect2["x"] + rect2["width"] and
        rect1["x"] + player_width > rect2["x"] and
        rect1["y"] < rect2["y"] + rect2["height"] and
        rect1["y"] + player_height > rect2["y"]
    ):
        return True
    return False

def check_collisions(player_y):
    global level, obstacles, coins

    collected_coins = []

    for obstacle in obstacles:
        if check_collision({"x": player_x, "y": player_y}, obstacle):
            if player_y + player_height <= obstacle["y"]:
                player_y = obstacle["y"] - player_height
            else:
                game_over()

    for coin in coins:
        if check_collision({"x": player_x, "y": player_y}, coin):
            collected_coins.append(coin)

    for coin in collected_coins:
        coins.remove(coin)

    if len(coins) == 0:
        level += 1
        start_next_level()

def game_over():
    pygame.time.delay(1000)
    reset_game()
    draw_game_over()

def reset_game():
    global player_x, player_y, obstacles, coins

    player_x = 0
    player_y = game_height - player_height
    obstacles = [
        {"x": 100, "y": game_height - 40, "width": 80, "height": 30},
        {"x": 200, "y": game_height - 80, "width": 80, "height": 30},
        {"x": 300, "y": game_height - 60, "width": 80, "height": 30},
        {"x": 400, "y": game_height - 100, "width": 80, "height": 30}
    ]
    coins = [
        {"x": 150, "y": game_height - 60, "width": 20, "height": 20},
        {"x": 250, "y": game_height - 80, "width": 20, "height": 20}
    ]

def start_next_level():
    reset_game()
    generate_obstacles()
    generate_coins()

def generate_obstacles():
    obstacles.clear()
    obstacle_positions = [
        {"x": 100, "y": game_height - 40, "width": 80, "height": 30},
        {"x": 200, "y": game_height - 80, "width": 80, "height": 30},
        {"x": 300, "y": game_height - 60, "width": 80, "height": 30},
        {"x": 400, "y": game_height - 100, "width": 80, "height": 30}
    ]
    obstacles.extend(obstacle_positions)

def generate_coins():
    coins.clear()
    coin_positions = [
        {"x": 150, "y": game_height - 60, "width": 20, "height": 20},
        {"x": 250, "y": game_height - 80, "width": 20, "height": 20}
    ]
    coins.extend(coin_positions)

def move_player(move_amount):
    global player_x

    player_x += move_amount

    if player_x < 0:
        player_x = 0
    elif player_x > game_width - player_width:
        player_x = game_width - player_width

def handle_jump():
    global player_y, is_jumping, jump_height

    player_y -= jump_height
    jump_height -= 1

    if player_y >= game_height - player_height:
        player_y = game_height - player_height
        jump_height = 0
        is_jumping = False

def draw_game_over():
    game_over_text = "Koniec gry"
    draw_text(game_over_text, game_width // 2 - 50, game_height // 2 - 10, color=RED)

def draw_copyright():
    copyright_text = "© Szymon Wasik 2023"
    alpha_text = "Wersja Alpha 1.0.2"
    draw_text(alpha_text, game_width - 140, game_height - 30)
    draw_text(copyright_text, 10, game_height - 30)

def main_loop():
    global player_x, player_y, level, moving_left, moving_right, is_jumping, jump_height

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moving_left = True
                elif event.key == K_RIGHT:
                    moving_right = True
                elif event.key == K_SPACE:
                    if not is_jumping:
                        jump_height = 10
                        is_jumping = True

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moving_left = False
                elif event.key == K_RIGHT:
                    moving_right = False

        move_amount = 0
        if moving_left:
            move_amount = -5
        elif moving_right:
            move_amount = 5

        move_player(move_amount)
        if is_jumping:
            handle_jump()
        check_collisions(player_y)

        game_display.fill(GRAY)

        draw_player()
        draw_obstacles()
        draw_coins()
        draw_text("Poziom: {}".format(level), 10, 10)
        draw_text("© Szymon Wasik 2023", 10, game_height - 30)
        draw_text("Wersja Alpha 1.0.2", game_width - 140, game_height - 30)

        pygame.display.update()
        clock.tick(60)

main_loop()
