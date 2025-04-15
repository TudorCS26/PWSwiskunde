import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt Deluxe - Havo 4")

# Load assets
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

duck_img = pygame.image.load("duck.png")
duck_img = pygame.transform.scale(duck_img, (80, 80))

shoot_sound = pygame.mixer.Sound("shoot.wav")

# Font
font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 80)

# Duck class
class Duck:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 80)
        self.y = random.randint(100, HEIGHT - 150)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-2, 2])

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH - 80:
            self.speed_x *= -1
        if self.y <= 50 or self.y >= HEIGHT - 100:
            self.speed_y *= -1

    def draw(self, surface):
        surface.blit(duck_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 80, 80)

# Game variables
ducks = [Duck() for _ in range(3)]
score = 0
missed_shots = 0
max_misses = 5

clock = pygame.time.Clock()

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2
state = START

# Functions
def draw_text(text, size, x, y, center=True):
    f = pygame.font.SysFont(None, size)
    img = f.render(text, True, (255, 255, 255))
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))

    if state == START:
        screen.blit(background, (0, 0))
        draw_text("🦆 DUCK HUNT DELUXE 🦆", 80, WIDTH // 2, HEIGHT // 3)
        draw_text("Klik om te beginnen", 50, WIDTH // 2, HEIGHT // 2)
        draw_text("Schiet op de eenden voordat je 5 mist!", 40, WIDTH // 2, HEIGHT // 2 + 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = PLAYING
                score = 0
                missed_shots = 0
                ducks = [Duck() for _ in range(3)]

    elif state == PLAYING:
        screen.blit(background, (0, 0))

        for duck in ducks:
            duck.move()
            duck.draw(screen)

        draw_text(f"Score: {score}", 40, 10, 10, center=False)
        draw_text(f"Missed: {missed_shots}/{max_misses}", 40, 10, 50, center=False)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot_sound.play()
                hit = False
                mx, my = pygame.mouse.get_pos()
                for duck in ducks:
                    if duck.get_rect().collidepoint(mx, my):
                        ducks.remove(duck)
                        ducks.append(Duck())
                        score += 1
                        hit = True
                        break
                if not hit:
                    missed_shots += 1
                    if missed_shots >= max_misses:
                        state = GAME_OVER

        clock.tick(60)

    elif state == GAME_OVER:
        screen.blit(background, (0, 0))
        draw_text("GAME OVER", 100, WIDTH // 2, HEIGHT // 3)
        draw_text(f"Je score: {score}", 60, WIDTH // 2, HEIGHT // 2)
        draw_text("Klik om opnieuw te spelen", 50, WIDTH // 2, HEIGHT // 2 + 80)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = START

pygame.quit()
sys.exit()