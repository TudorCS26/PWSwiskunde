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
