import pygame, time, math, random  

# === Constante waarden ===
FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
SPEED_INCREASE_FACTOR = 1.1
SPEED_DECREASE_FACTOR = 0.9
START_DELAY = 3
score = 0
MAX_LIVES = 3
lives = MAX_LIVES

ball_paused = False
ball_speed_mode = "normal" 
game_over = False

# Voeg kleine random afwijking toe aan balrichting om te voorkomen dat hij "vastloopt"
def add_random_angle(vx, vy, max_angle_degrees=15):
    angle = math.atan2(vy, vx)
    magnitude = math.hypot(vx, vy)
    deviation = math.radians(random.uniform(-max_angle_degrees, max_angle_degrees))
    new_angle = angle + deviation
    return magnitude * math.cos(new_angle), magnitude * math.sin(new_angle)

# Startwaarden instellen voor bal, paddle en bricks
def initialize_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global paddle_x, paddle_y, game_status_msg, first_bounce
    global bricks, AANTAL_KOLOMMEN, AANTAL_RIJEN
    global BRICK_WIDTH, BRICK_HEIGHT, bricks_x, bricks_y
    global speed_change_count, bricks_img_scaled, score
    global lives, game_over

    BRICK_WIDTH = SCREEN_WIDTH / AANTAL_KOLOMMEN
    BRICK_HEIGHT = int(BRICK_WIDTH * 0.25)

    ball_x = SCREEN_WIDTH // 2
    ball_y = 600

    # Pas beginsnelheid van bal aan op geselecteerde modus
    if ball_speed_mode == "slow":
        base_speed = 4
    elif ball_speed_mode == "fast":
        base_speed = 9
    else:
        base_speed = 6

    ball_speed_x = base_speed
    ball_speed_y = base_speed * math.pi

    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - 100
    game_status_msg = "Links druk [A] rechts druk [D]"
    first_bounce = True
    bricks_x = []
    bricks_y = []
    speed_change_count = 0
    score = 0

    lives = MAX_LIVES
    game_over = False

    # Genereer bricks op basis van rijen en kolommen
    bricks = []
    for i in range(AANTAL_RIJEN):
        row = []
        for j in range(AANTAL_KOLOMMEN):
            row.append(True)
            bricks_x.append(j * BRICK_WIDTH)
            bricks_y.append(i * BRICK_HEIGHT + 100)
        bricks.append(row)

    bricks_img_scaled = pygame.transform.scale(bricks_img, (int(BRICK_WIDTH), int(BRICK_HEIGHT)))

# === Pygame setup ===
pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
fps_clock = pygame.time.Clock()

# Achtergrondafbeelding laden
background_img = pygame.image.load("background_0_breakout.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Spritesheet en onderdelen laden
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

# Bal-afbeelding uitsnijden en schalen
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) 

# Paddle frames uit spritesheet halen
paddle_imgs = []
paddle_coords = [
    (1158, 462, 243, 64),
    (1158, 528, 243, 64),
    (1158, 594, 243, 64)
]
for coords in paddle_coords:
    img = pygame.Surface((243, 64), pygame.SRCALPHA)
    img.blit(spritesheet, (0, 0), coords)
    img = pygame.transform.scale(img, (PADDLE_WIDTH, PADDLE_HEIGHT))
    paddle_imgs.append(img)

# Brick-afbeelding
bricks_img = pygame.Surface((380, 128), pygame.SRCALPHA)
bricks_img.blit(spritesheet, (0, 0), (0, 130, 384, 128))

# Hart-afbeelding uit spritesheet halen (x=1637, y=652, width=64, height=58)
heart_img = pygame.Surface((64, 58), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (32, 29))  # schalen naar kleiner formaat

# Tekst renderen op scherm
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Startscherm met inputvelden voor rijen en kolommen + snelheidsselectie
def start_screen():
    global AANTAL_RIJEN, AANTAL_KOLOMMEN
    global ball_speed_mode 

    input_active = None
    row_text = ""
    col_text = ""
    input_rect_color = pygame.Color("lightskyblue3")

    input_font = pygame.font.SysFont('default', 48)

    slow_button_rect = pygame.Rect(400, 350, 200, 50)
    fast_button_rect = pygame.Rect(650, 350, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            # Klik op inputvelden of knoppen
            if event.type == pygame.MOUSEBUTTONDOWN:
                if row_rect.collidepoint(event.pos):
                    input_active = 'rows'
                elif col_rect.collidepoint(event.pos):
                    input_active = 'cols'
                elif start_button_rect.collidepoint(event.pos):
                    # Valideer invoer
                    if row_text.isdigit() and col_text.isdigit():
                        AANTAL_RIJEN = int(row_text)
                        AANTAL_KOLOMMEN = int(col_text)
                        if 6 <= AANTAL_RIJEN <= 20 and AANTAL_KOLOMMEN >= AANTAL_RIJEN + 2:
                            return True
                elif slow_button_rect.collidepoint(event.pos):
                    ball_speed_mode = "slow"
                elif fast_button_rect.collidepoint(event.pos):
                    ball_speed_mode = "fast"

            # Toetsenbord input voor rijen/kolommen
            if event.type == pygame.KEYDOWN:
                if input_active == 'rows':
                    if event.key == pygame.K_BACKSPACE:
                        row_text = row_text[:-1]
                    else:
                        row_text += event.unicode
                elif input_active == 'cols':
                    if event.key == pygame.K_BACKSPACE:
                        col_text = col_text[:-1]
                    else:
                        col_text += event.unicode

        # Tekst en inputvelden tekenen
        screen.blit(background_img, (0, 0))  
        draw_text('Voer het aantal rijen (6-20) in:', input_font, 'white', screen, 100, 100)
        draw_text('Voer het aantal kolommen in (rijen + 2):', input_font, 'white', screen, 100, 200)

        row_surface = input_font.render(row_text, True, input_rect_color)
        col_surface = input_font.render(col_text, True, input_rect_color)

        row_rect = pygame.Rect(100, 150, 140, 50)
        col_rect = pygame.Rect(100, 250, 140, 50)
        pygame.draw.rect(screen, input_rect_color, row_rect, 2)
        pygame.draw.rect(screen, input_rect_color, col_rect, 2)

        screen.blit(row_surface, (row_rect.x + 5, row_rect.y + 5))
        screen.blit(col_surface, (col_rect.x + 5, col_rect.y + 5))

        start_button_rect = pygame.Rect(100, 450, 200, 50)
        pygame.draw.rect(screen, 'green', start_button_rect)
        draw_text('Start', input_font, 'black', screen, start_button_rect.x + 50, start_button_rect.y + 10)

        pygame.draw.rect(screen, 'blue', slow_button_rect)
        draw_text('Langzaam', input_font, 'white', screen, slow_button_rect.x + 10, slow_button_rect.y + 5)

        pygame.draw.rect(screen, 'red', fast_button_rect)
        draw_text('Snel', input_font, 'white', screen, fast_button_rect.x + 50, fast_button_rect.y + 5)

        pygame.display.flip()
        fps_clock.tick(FPS)

# Simpele countdown voor spelstart
def countdown_timer():
    for i in range(START_DELAY, 0, -1):
        screen.blit(background_img, (0, 0)) 
        draw_text(f'Starting in {i}', font, 'white', screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        time.sleep(1)
# Het spelen van het spel
def initialize_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global paddle_x, paddle_y, game_status_msg, first_bounce
    global bricks, AANTAL_KOLOMMEN, AANTAL_RIJEN
    global BRICK_WIDTH, BRICK_HEIGHT, bricks_x, bricks_y
    global speed_change_count, bricks_img_scaled, game_over  

    BRICK_WIDTH = SCREEN_WIDTH / AANTAL_KOLOMMEN
    BRICK_HEIGHT = int(BRICK_WIDTH * 0.25)

    paddle_y = SCREEN_HEIGHT - 100
    game_status_msg = "Links druk [A] rechts druk [D]"
    first_bounce = True
    bricks_x = []
    bricks_y = []
    speed_change_count = 0

    game_over = False

    # Genereer bricks op basis van rijen en kolommen
    bricks = []
    for i in range(AANTAL_RIJEN):
        row = []
        for j in range(AANTAL_KOLOMMEN):
            row.append(True)
            bricks_x.append(j * BRICK_WIDTH)
            bricks_y.append(i * BRICK_HEIGHT + 100)
        bricks.append(row)

    bricks_img_scaled = pygame.transform.scale(bricks_img, (int(BRICK_WIDTH), int(BRICK_HEIGHT)))

    reset_ball_and_paddle() 

def reset_ball_and_paddle():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x, ball_paused, first_bounce

    ball_x = SCREEN_WIDTH // 2
    ball_y = 600
    if ball_speed_mode == "slow":
        base_speed = 4
    elif ball_speed_mode == "fast":
        base_speed = 9
    else:
        base_speed = 6
    ball_speed_x = base_speed
    ball_speed_y = base_speed * math.pi
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    ball_paused = True
    first_bounce = True

# === Start van het spel ===
if start_screen():
    countdown_timer()
    score = 0                
    lives = MAX_LIVES       
    initialize_game()

    paddle_frame = 0
    frame_counter = 0
    running = True
    while running:
        game_current_score = "Score = " + str(score)
        game_current_score_img = font.render(game_current_score, False, 'green')
        
        # Alle keys voor het spelen van het spel
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                running = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0                    
                    lives = MAX_LIVES            
                    initialize_game()
                    game_over = False
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
                    pygame.quit()
                    break
                elif event.key == pygame.K_SPACE:
                    if not game_over:
                        ball_paused = not ball_paused
                    else:
                        score = 0                
                        lives = MAX_LIVES        
                        initialize_game()
                        game_over = False
        # De keys a + d en de snelheid van hoe de paddle beweegt
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_d]: 
                paddle_x += 22
            if keys[pygame.K_a]: 
                paddle_x -= 22
            paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - PADDLE_WIDTH))

        if not ball_paused and not game_over:
            next_ball_x = ball_x + ball_speed_x
            next_ball_y = ball_y + ball_speed_y

            if (ball_speed_y > 0 and
                ball_y + BALL_HEIGHT <= paddle_y and
                next_ball_y + BALL_HEIGHT >= paddle_y and
                next_ball_x + BALL_WIDTH > paddle_x and
                next_ball_x < paddle_x + PADDLE_WIDTH):

                ball_y = paddle_y - BALL_HEIGHT
                ball_speed_y *= -1

                hit_pos = (next_ball_x + BALL_WIDTH / 2) - (paddle_x + PADDLE_WIDTH / 2)
                offset = hit_pos / (PADDLE_WIDTH / 2)
                angle = offset * (math.pi / 3)  
                speed = math.hypot(ball_speed_x, ball_speed_y)
                ball_speed_x = speed * math.sin(angle)
                ball_speed_y = -speed * math.cos(angle)

                if first_bounce:
                    first_bounce = False
                    game_status_msg = ""
                # Veranderen van de snelheid van de bal
                speed_change_count += 1
                if speed_change_count <= 2:
                    ball_speed_x *= SPEED_INCREASE_FACTOR
                    ball_speed_y *= SPEED_INCREASE_FACTOR
                elif speed_change_count >= 7:
                    ball_speed_x *= SPEED_DECREASE_FACTOR
                    ball_speed_y *= SPEED_DECREASE_FACTOR

            if next_ball_x < 0 or next_ball_x > SCREEN_WIDTH - BALL_WIDTH:
                ball_speed_x *= -1

            if next_ball_y < 0:
                ball_speed_y *= -1

            if next_ball_y > SCREEN_HEIGHT:
                lives -= 1                        
                if lives <= 0:
                    game_over = True
                    game_status_msg = "Game Over! Druk R om opnieuw te starten."
                else:
                    reset_ball_and_paddle()       
            # Collision met de blocken en het weghalen van de blocken
            brick_hit = False
            for i, row in enumerate(bricks):
                for j, brick_alive in enumerate(row):
                    if brick_alive:
                        brick_rect = pygame.Rect(j*BRICK_WIDTH, i*BRICK_HEIGHT + 100, BRICK_WIDTH, BRICK_HEIGHT)
                        ball_rect = pygame.Rect(next_ball_x, next_ball_y, BALL_WIDTH, BALL_HEIGHT)
                        if brick_rect.colliderect(ball_rect):
                            bricks[i][j] = False
                            score += 30*0.31415926535989793238462643383279
                            ball_speed_y *= -1
                            brick_hit = True
                            break
                if brick_hit:
                    break

            if not brick_hit:
                ball_x = next_ball_x
                ball_y = next_ball_y
        # Het blitten van alles
        screen.blit(background_img, (0, 0))
        for i, row in enumerate(bricks):
            for j, brick_alive in enumerate(row):
                if brick_alive:
                    screen.blit(bricks_img_scaled, (j * BRICK_WIDTH, i * BRICK_HEIGHT + 100))
        screen.blit(ball_img, (int(ball_x), int(ball_y)))
        paddle_frame = (paddle_frame + 1) % len(paddle_imgs)
        screen.blit(paddle_imgs[paddle_frame], (paddle_x, paddle_y))
        screen.blit(game_current_score_img, (SCREEN_WIDTH - 300, 10))
        for i in range(lives):
            screen.blit(heart_img, (10 + i*40, 10))

        if game_status_msg:
            draw_text(game_status_msg, font, 'red', screen, 80, 60)

        pygame.display.flip()
        fps_clock.tick(FPS)

pygame.quit()