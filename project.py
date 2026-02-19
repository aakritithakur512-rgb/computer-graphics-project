import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("City Day & Night Cycle")

clock = pygame.time.Clock()
time_passed = 0

# Generate buildings
buildings = []
for i in range(8):
    width = random.randint(80, 130)
    height = random.randint(200, 350)
    x = i * 130 + 20
    y = HEIGHT - height - 150
    buildings.append((x, y, width, height))

# Generate stars
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT//2)) for _ in range(100)]

def draw_gradient(color1, color2):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = color1[0] * (1 - ratio) + color2[0] * ratio
        g = color1[1] * (1 - ratio) + color2[1] * ratio
        b = color1[2] * (1 - ratio) + color2[2] * ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

running = True
while running:
    clock.tick(60)
    time_passed += 0.002

    cycle = (math.sin(time_passed) + 1) / 2  # 0 to 1

    # Sky colors
    day_top = (135, 206, 250)
    day_bottom = (255, 180, 120)
    night_top = (10, 10, 40)
    night_bottom = (40, 40, 80)

    sky_top = [day_top[i] * cycle + night_top[i] * (1 - cycle) for i in range(3)]
    sky_bottom = [day_bottom[i] * cycle + night_bottom[i] * (1 - cycle) for i in range(3)]

    draw_gradient(sky_top, sky_bottom)

    # Stars at night
    if cycle < 0.4:
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 2)

    # Sun / Moon path
    angle = time_passed
    celestial_x = WIDTH // 2 + math.cos(angle) * 350
    celestial_y = 250 - math.sin(angle) * 200

    if cycle > 0.5:
        pygame.draw.circle(screen, (255, 223, 0), (int(celestial_x), int(celestial_y)), 45)
    else:
        pygame.draw.circle(screen, (230, 230, 255), (int(celestial_x), int(celestial_y)), 35)

    # Draw buildings
    for b in buildings:
        building_color = (40 * cycle + 20, 40 * cycle + 20, 60 * cycle + 40)
        pygame.draw.rect(screen, building_color, b)

        # Windows
        for i in range(3):
            for j in range(6):
                wx = b[0] + 15 + i * 30
                wy = b[1] + 20 + j * 40
                if cycle < 0.4:
                    pygame.draw.rect(screen, (255, 255, 120), (wx, wy, 15, 20))
                else:
                    pygame.draw.rect(screen, (180, 220, 255), (wx, wy, 15, 20))

    # Road
    pygame.draw.rect(screen, (60, 60, 60), (0, HEIGHT - 120, WIDTH, 120))
    pygame.draw.line(screen, (255, 255, 0), (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 4)

    # Street lights
    for i in range(5):
        x = 150 + i * 170
        pygame.draw.rect(screen, (80, 80, 80), (x, HEIGHT - 200, 10, 80))
        if cycle < 0.4:
            pygame.draw.circle(screen, (255, 255, 180), (x + 5, HEIGHT - 200), 15)

    # Parked car
    pygame.draw.rect(screen, (200, 0, 0), (700, HEIGHT - 160, 140, 40))
    pygame.draw.circle(screen, (0, 0, 0), (730, HEIGHT - 120), 20)
    pygame.draw.circle(screen, (0, 0, 0), (800, HEIGHT - 120), 20)

    # Headlights at night
    if cycle < 0.4:
        pygame.draw.circle(screen, (255, 255, 180), (840, HEIGHT - 145), 12)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
