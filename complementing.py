import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt - Havo 4 Edition")

# Load assets
duck_img = pygame.image.load("duck.png")
duck_img = pygame.transform.scale(duck_img, (80, 80))  # Resize the duck

background_color = (135, 206, 235)  # Sky blue

# Duck settings
duck_x = random.randint(0, WIDTH - 80)
duck_y = random.randint(100, HEIGHT - 150)
duck_speed = 5

# Score
score = 0
font = pygame.font.SysFont(None, 40)

# Clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    screen.fill(background_color)

    # Move the duck
    duck_x += duck_speed
    if duck_x > WIDTH or duck_x < -80:
        duck_speed *= -1
        duck_y = random.randint(100, HEIGHT - 150)

    # Draw the duck
    screen.blit(duck_img, (duck_x, duck_y))

    # Draw the score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot duck
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            duck_rect = pygame.Rect(duck_x, duck_y, 80, 80)
            if duck_rect.collidepoint(mx, my):
                score += 1
                duck_x = random.randint(0, WIDTH - 80)
                duck_y = random.randint(100, HEIGHT - 150)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
