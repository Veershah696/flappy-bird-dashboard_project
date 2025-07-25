import pygame
import random
pygame.init()
# Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, HEIGHT // 2
BIRD_WIDTH, BIRD_HEIGHT = 40, 30  # Adjust according to the bird image
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_VELOCITY = 3
FPS = 30
WHITE = (255, 255, 255)  
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load bird image
bird_img = pygame.image.load("flappy bird.png")
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
bird_y = BIRD_Y
bird_velocity = 10
pipes = []

def create_pipe():
    pipe_height = random.randint(100, 400)
    pipes.append([WIDTH, pipe_height, False])  # False indicates the bird hasn't passed yet

def move_pipes():
    for pipe in pipes:
        pipe[0] -= PIPE_VELOCITY
    if pipes and pipes[0][0] < -PIPE_WIDTH:
        pipes.pop(0)

def check_collision():
    if bird_y <= 0 or bird_y + BIRD_HEIGHT >= HEIGHT:
        return True
    for pipe in pipes:
        pipe_x, pipe_height, _ = pipe
        if (BIRD_X + BIRD_WIDTH > pipe_x and BIRD_X < pipe_x + PIPE_WIDTH):
            if bird_y < pipe_height or bird_y + BIRD_HEIGHT > pipe_height + PIPE_GAP:
                return True
    return False

running = True
score = 0
frame_count = 0
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = JUMP_STRENGTH

    # Apply gravity
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    # Generate and move pipes
    if frame_count % 90 == 0:
        create_pipe()
    move_pipes()

    # Draw bird
    screen.blit(bird_img, (BIRD_X, int(bird_y)))

    # Draw pipes
    for pipe in pipes:
        pipe_x, pipe_height, passed = pipe
        pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, pipe_height))
        pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT))

        # Score update
        if not passed and pipe_x + PIPE_WIDTH < BIRD_X:
            score += 1
            pipe[2] = True

            # Check for collisions
    if check_collision():
        running = False

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, RED)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

pygame.quit()