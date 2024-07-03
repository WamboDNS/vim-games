import pygame as pg
import random
from typing import Tuple

# Constants
WINDOW_SIZE: int = 800
TILE_SIZE: int = 50
RANGE: Tuple[int, int, int] = (TILE_SIZE // 2, WINDOW_SIZE - TILE_SIZE // 2, TILE_SIZE)
FPS: int = 60
TIMESTEP: int = 110

# Initialize Pygame
pg.init()

# Utility function to get a random position within the grid
def get_random_pos() -> Tuple[int, int]:
    return random.randrange(*RANGE), random.randrange(*RANGE)

# Initialize game entities
snake = pg.Rect(0, 0, TILE_SIZE - 2, TILE_SIZE - 2)
snake.center = get_random_pos()
apple = pg.Rect(0, 0, TILE_SIZE - 2, TILE_SIZE - 2)
apple.center = get_random_pos()
length: int = 1
segments = [snake]
snake_dir: Tuple[int, int] = (0, 0)
time, last_time = 0, 0

# Set up the display
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pg.time.Clock()

# Allowed moves to prevent reversing direction
allowed_moves = {"k": True, "j": True, "h": True, "l": True}

def reset_game():
    """Resets the game state."""
    global snake, apple, length, segments, allowed_moves
    snake.center = get_random_pos()
    apple.center = get_random_pos()
    length = 1
    segments = [snake.copy()]
    allowed_moves = {"k": True, "j": True, "h": True, "l": True}

def handle_events():
    """Handles user input events."""
    global snake_dir, allowed_moves
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_k and allowed_moves["k"]:
                snake_dir = (0, -TILE_SIZE)
                allowed_moves = {"k": True, "j": False, "h": True, "l": True}
            if event.key == pg.K_j and allowed_moves["j"]:
                snake_dir = (0, TILE_SIZE)
                allowed_moves = {"k": False, "j": True, "h": True, "l": True}
            if event.key == pg.K_h and allowed_moves["h"]:
                snake_dir = (-TILE_SIZE, 0)
                allowed_moves = {"k": True, "j": True, "h": True, "l": False}
            if event.key == pg.K_l and allowed_moves["l"]:
                snake_dir = (TILE_SIZE, 0)
                allowed_moves = {"k": True, "j": True, "h": False, "l": True}

def update_game():
    """Updates the game state."""
    global snake, segments, length, time, last_time
    screen.fill((0, 0, 0))

    # Check for self-collision or boundary collision
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if self_eating or not snake.colliderect(screen.get_rect()):
        reset_game()

    # Check for apple collision
    if snake.colliderect(apple):
        apple.center = get_random_pos()
        length += 1

    # Draw apple and snake
    pg.draw.rect(screen, "red", apple)
    [pg.draw.rect(screen, "green", segment) for segment in segments]

    # Update snake position
    time_now = pg.time.get_ticks()
    if time_now - last_time > TIMESTEP:
        last_time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

def main():
    """Main game loop."""
    while True:
        handle_events()
        update_game()
        pg.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()