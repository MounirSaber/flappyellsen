import pygame
import random

# Initialisierung
pygame.init()
pygame.mouse.set_visible(False)  # Mauszeiger ausblenden im Web

# Feste Fenstergröße (webkompatibel)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FlappyEllsen 🧠 Web Mode")

# Bilder laden (ohne "res/"-Ordner, webfreundlich)
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("ManuellsenHintergrund.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("Mhead.png"), (100, 100))
PIPE_IMAGE_ORIGINAL = pygame.image.load("pipe.png")

# Spieler-Maske
player_mask = pygame.mask.from_surface(PLAYER_IMAGE)

# Spielerposition und Bewegung
player_x = 50
player_y = SCREEN_HEIGHT // 2
player_y_movement = 0
gravity = 0.5
jump_strength = -8

# Rohre
pipes = []
pipe_width = 80
pipe_gap = 300
pipe_velocity = 3
pipe_timer = 0
pipe_interval = 90
min_pipe_height = 80

# Punktestand
score = 0
max_score = 88
font = pygame.font.Font(None, 36)

# Hintergrundscrolling
background_x = 0

def create_pipe():
    max_top_height = SCREEN_HEIGHT - pipe_gap - min_pipe_height
    top_height = random.randint(min_pipe_height, max_top_height)
    bottom_y = top_height + pipe_gap
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, top_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, bottom_y, pipe_width, SCREEN_HEIGHT - bottom_y)
    return {"top": top_pipe, "bottom": bottom_pipe, "scored": False}

def show_message(message):
    screen.fill((0, 0, 0))
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    text_surface = font.render(message, True, (255, 255, 255))
    subtext_surface = font.render("Press SPACE to start", True, (200, 200, 200))
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(subtext_surface, (SCREEN_WIDTH // 2 - subtext_surface.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Startscreen anzeigen
show_message("FlappyEllsen 🧠")

# Clock & Game Loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))
    background_x -= 1
    if background_x <= -SCREEN_WIDTH:
        background_x = 0
    screen.blit(BACKGROUND_IMAGE, (background_x, 0))
    screen.blit(BACKGROUND_IMAGE, (background_x + SCREEN_WIDTH, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_y_movement = jump_strength
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Spielerbewegung
    player_y_movement += gravity
    player_y += player_y_movement
    player_rect = pygame.Rect(player_x, player_y, PLAYER_IMAGE.get_width(), PLAYER_IMAGE.get_height())
    screen.blit(PLAYER_IMAGE, (player_x, player_y))

    # Rohrlogik
    pipe_timer += 1
    if pipe_timer >= pipe_interval:
        pipes.append(create_pipe())
        pipe_timer = 0

    new_pipes = []
    for pipe in pipes:
        top_pipe = pipe["top"]
        bottom_pipe = pipe["bottom"]
        top_pipe.x -= pipe_velocity
        bottom_pipe.x -= pipe_velocity

        # Bild skalieren & einzeichnen
        top_pipe_img = pygame.transform.scale(PIPE_IMAGE_ORIGINAL, (pipe_width, top_pipe.height))
        bottom_pipe_img = pygame.transform.scale(pygame.transform.flip(PIPE_IMAGE_ORIGINAL, False, True), (pipe_width, bottom_pipe.height))
        top_mask = pygame.mask.from_surface(top_pipe_img)
        bottom_mask = pygame.mask.from_surface(bottom_pipe_img)

        screen.blit(top_pipe_img, top_pipe)
        screen.blit(bottom_pipe_img, bottom_pipe)

        # Kollision
        offset_top = (top_pipe.x - player_rect.x, top_pipe.y - player_rect.y)
        offset_bottom = (bottom_pipe.x - player_rect.x, bottom_pipe.y - player_rect.y)
        if player_mask.overlap(top_mask, offset_top) or player_mask.overlap(bottom_mask, offset_bottom):
            show_message("Game Over! Press SPACE to retry")

        if not pipe["scored"] and top_pipe.right < player_x:
            score += 1
            pipe["scored"] = True

        if top_pipe.right > 0:
            new_pipes.append(pipe)

    pipes = new_pipes

    if player_y < 0 or player_y > SCREEN_HEIGHT:
        show_message("Game Over! Press SPACE to retry")

    # Punkteanzeige
    score_text = font.render(f"Punkte: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if score >= max_score:
        show_message("Ziel erreicht! Press SPACE to restart")

    pygame.display.update()
    clock.tick(60)

pygame.quit()
