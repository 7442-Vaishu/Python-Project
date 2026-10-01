import pygame
import random
import sys

# Pygame initialize
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (15, 15, 15)
GREEN = (0, 255, 100)
RED = (230, 50, 50)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)

# Clock & Font setup
clock = pygame.time.Clock()
font_main = pygame.font.SysFont("arial", 40, bold=True)
font_sub = pygame.font.SysFont("arial", 22)

# Global variables
snake = []
snake_dir = ""
food = []
score = 0
game_over = False

def reset_game():
    global snake, snake_dir, food, score, game_over
    
    snake = [[100, 100], [80, 100], [60, 100]]
    snake_dir = "RIGHT"
    
    food = [
        random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE,
        random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE
    ]
    
    score = 0
    game_over = False

reset_game()

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
            else:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake_dir != "DOWN":
                    snake_dir = "UP"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake_dir != "UP":
                    snake_dir = "DOWN"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake_dir != "RIGHT":
                    snake_dir = "LEFT"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake_dir != "LEFT":
                    snake_dir = "RIGHT"

    if not game_over:
        head_x, head_y = snake[0]

        if snake_dir == "UP":
            head_y -= CELL_SIZE
        elif snake_dir == "DOWN":
            head_y += CELL_SIZE
        elif snake_dir == "LEFT":
            head_x -= CELL_SIZE
        elif snake_dir == "RIGHT":
            head_x += CELL_SIZE

        new_head = [head_x, head_y]

        if (head_x < 0 or head_x >= WIDTH or 
            head_y < 0 or head_y >= HEIGHT or 
            new_head in snake):
            game_over = True

        if not game_over:
            snake.insert(0, new_head)

            if head_x == food[0] and head_y == food[1]:
                score += 10
                food = [
                    random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE,
                    random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE
                ]
            else:
                snake.pop()

    win.fill(BLACK)

    if not game_over:
        for segment in snake:
            pygame.draw.rect(win, GREEN, (segment[0], segment[1], CELL_SIZE - 2, CELL_SIZE - 2))

        pygame.draw.circle(win, ORANGE, (food[0] + CELL_SIZE // 2, food[1] + CELL_SIZE // 2), CELL_SIZE // 2)

        score_text = font_sub.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

    else:
        go_text = font_main.render("GAME OVER", True, RED)
        restart_text = font_sub.render("Press R to Restart", True, WHITE)

        go_rect = go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        res_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

        win.blit(go_text, go_rect)
        win.blit(restart_text, res_rect)

    pygame.display.update()
    clock.tick(10)