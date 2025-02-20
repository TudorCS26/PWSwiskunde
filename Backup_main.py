import pygame, time, math

# Define constants
FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 0
BRICK_HEIGHT = 0
SPEED_INCREASE_FACTOR = 1.1  # Factor to increase speed
SPEED_DECREASE_FACTOR = 0.9  # Factor to decrease speed
START_DELAY = 3  # Start delay in seconds
score = 0

# Initialize global variables
def initialize_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x, paddle_y, game_status_msg, first_bounce, bricks, AANTAL_KOLOMMEN, AANTAL_RIJEN, BRICK_WIDTH, BRICK_HEIGHT, brick_x, brick_y, brick_img_scaled
    global speed_change_count, increasing_speed, score

    # Block size
    BRICK_WIDTH = SCREEN_WIDTH / AANTAL_KOLOMMEN
    BRICK_HEIGHT = int(BRICK_WIDTH * 0.25)

    # Define global variables
    ball_x = SCREEN_WIDTH // 2
    ball_y = 600
    ball_speed_x = 6
    ball_speed_y = ball_speed_x * 2.834583765
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - 40
    game_status_msg = "Links druk [A] rechts druk [D]"
    first_bounce = False
    brick_x = []
    brick_y = []

    # Initialize speed change counters
    speed_change_count = 0
    increasing_speed = True  # Start with increasing speed

    # Create list of bricks
    bricks = []
    for i in range(AANTAL_RIJEN):
        row = []
        for j in range(AANTAL_KOLOMMEN):
            row.append(True)  # True means the brick is present
            brick_x.append(j * BRICK_WIDTH)
            brick_y.append(i * BRICK_HEIGHT + 100)
        bricks.append(row)

    brick_img_scaled = pygame.transform.scale(brick_img, (int(BRICK_WIDTH), int(BRICK_HEIGHT)))

    # Reset score
    score = 0

# Initialize game
pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
fps_clock = pygame.time.Clock()

# Read images
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

# Add ball
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  # Create new image
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))  # Copy part of sheet to image
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

# Add paddle
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0, 0), (1158, 462, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# Add bricks
brick_img = pygame.Surface((380, 130), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (0, 130, 380, 130))

# Add text-startscreen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Create startscreen
def start_screen():
    global AANTAL_RIJEN, AANTAL_KOLOMMEN
    input_active = None
    row_text = ''
    col_text = ''
    input_rect_color = pygame.Color('lightskyblue3')
    
    input_font = pygame.font.SysFont('default', 48)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if row_rect.collidepoint(event.pos):
                    input_active = 'rows'
                elif col_rect.collidepoint(event.pos):
                    input_active = 'cols'
                elif start_button_rect.collidepoint(event.pos):
                    if row_text.isdigit() and col_text.isdigit():
                        AANTAL_RIJEN = int(row_text)
                        AANTAL_KOLOMMEN = int(col_text)
                        if 6 <= AANTAL_RIJEN <= 20 and AANTAL_KOLOMMEN >= AANTAL_RIJEN + 2:
                            return True
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

        screen.fill('black')
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
        
        start_button_rect = pygame.Rect(100, 350, 200, 50)
        pygame.draw.rect(screen, 'green', start_button_rect)
        draw_text('Start', input_font, 'black', screen, start_button_rect.x + 50, start_button_rect.y + 10)
        
        pygame.display.flip()
        fps_clock.tick(FPS)

# Start timer
def countdown_timer():
    for i in range(START_DELAY, 0, -1):
        screen.fill('black')
        draw_text(f'Starting in {i}', font, 'white', screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        time.sleep(1)

# Blit Startscreen
if start_screen():
    countdown_timer()
    initialize_game()

    # Game loop
    print('mygame is running')
    running = True
    paused = False
    ball_paused = False  # Add this variable to track ball pause state

    while running:
        game_current_score = "Score = " + str(score)
        game_current_score_img = font.render(game_current_score, False, 'green')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    initialize_game()  # Reset the game
                elif event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    break
                elif event.key == pygame.K_SPACE:
                    ball_paused = not ball_paused  # Toggle ball pause state

        # Move the paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:  # Key d is down
            paddle_x += 10
        if keys[pygame.K_a]:  # Key a is down
            paddle_x -= 10

        # Ensure the paddle does not go out of the screen
        if paddle_x < 0:
            paddle_x = 0
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

        if not ball_paused:
            # Move the ball
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Ball bounces off the screen edges
            if ball_x < 0 or ball_x + BALL_WIDTH > SCREEN_WIDTH:
                ball_speed_x *= -1

            if ball_y < 0:
                ball_speed_y *= -1

            # Ball bounces off the paddle
            if (ball_x + BALL_WIDTH > paddle_x and
                    ball_x < paddle_x + PADDLE_WIDTH and
                    ball_y + BALL_HEIGHT > paddle_y and
                    ball_y < paddle_y + PADDLE_HEIGHT):
                ball_y = paddle_y - BALL_HEIGHT  # Position ball above the paddle
                ball_speed_y *= -1
                speed_change_count += 1

                # Increase or decrease speed based on the speed change count
                if speed_change_count <= 2:
                    ball_speed_x *= SPEED_INCREASE_FACTOR
                    ball_speed_y *= SPEED_INCREASE_FACTOR
                elif speed_change_count <= 7:
                    ball_speed_x *= SPEED_DECREASE_FACTOR
                    ball_speed_y *= SPEED_DECREASE_FACTOR
                elif speed_change_count <= 12:
                    ball_speed_x *= SPEED_INCREASE_FACTOR
                    ball_speed_y *= SPEED_INCREASE_FACTOR

            # Remove block if ball hits it
            for i in range(len(brick_x) - 1, -1, -1):
                if (ball_x + BALL_WIDTH > brick_x[i] and  # Right side of the ball
                    ball_x < brick_x[i] + BRICK_WIDTH and  # Left side of the ball
                    ball_y + BALL_HEIGHT > brick_y[i] and  # Top of the ball
                    ball_y < brick_y[i] + BRICK_HEIGHT):  # Bottom of the ball
                    score += 10
                    # Determine if the collision was horizontal or vertical
                    if (ball_y + BALL_HEIGHT - ball_speed_y <= brick_y[i] or ball_y - ball_speed_y >= brick_y[i] + BRICK_HEIGHT):
                        ball_speed_y *= -1
                    else:
                        ball_speed_x *= -1
                    brick_x.pop(i)
                    brick_y.pop(i)

            # On the first bounce with paddle, clear game status message
            if not first_bounce:
                first_bounce = True
                game_status_msg = ""

            # Lose condition
            if ball_y > paddle_y:
                ball_speed_x = 0
                ball_speed_y = 0
                game_status_msg = "You Lost!"

            # Win condition
            if len(brick_x) == 0:
                ball_speed_x = 0
                ball_speed_y = 0
                game_status_msg = "You won!!"

            # Game status message color
            game_status_img = font.render(game_status_msg, True, 'Green')

        # Draw everything
        screen.fill('black')
        screen.blit(game_current_score_img, (50, 15))
        screen.blit(ball_img, (ball_x, ball_y))
        screen.blit(paddle_img, (paddle_x, paddle_y))
        for i in range(len(brick_x) - 1, -1, -1):
            screen.blit(brick_img_scaled, (brick_x[i], brick_y[i]))
        screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - 100, 50))

        pygame.display.flip()

        fps_clock.tick(FPS)

    # End loop
    print('mygame stopt running')
    pygame.quit()