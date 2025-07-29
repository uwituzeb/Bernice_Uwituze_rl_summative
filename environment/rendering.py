import pygame
import numpy as np

def draw_environment(window, grid_size, cell_size, agent_location, target_location, obstacles):
    window_size = grid_size * cell_size
    canvas = pygame.Surface((window_size, window_size))
    canvas.fill((255, 255, 255))
    pix_square_size = cell_size

    # Draw target
    pygame.draw.rect(
        canvas,
        (0, 255, 0),
        pygame.Rect(
            pix_square_size * target_location[1],
            pix_square_size * target_location[0],
            pix_square_size,
            pix_square_size,
        ),
    )

    # Draw agent
    pygame.draw.circle(
        canvas,
        (0, 0, 255),
        (agent_location[1] * pix_square_size + pix_square_size // 2,
         agent_location[0] * pix_square_size + pix_square_size // 2),
        pix_square_size // 3,
    )

    # Draw obstacles
    for (i, j) in obstacles:
        pygame.draw.rect(
            canvas,
            (255, 0, 0),
            pygame.Rect(j * pix_square_size, i * pix_square_size, pix_square_size, pix_square_size),
        )

    # Draw gridlines
    for x in range(grid_size + 1):
        pygame.draw.line(canvas, (0, 0, 0), (0, x * pix_square_size), (window_size, x * pix_square_size), 2)
        pygame.draw.line(canvas, (0, 0, 0), (x * pix_square_size, 0), (x * pix_square_size, window_size), 2)

    return canvas