import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Интеллект AI")

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

player_size = 30
enemy_size = 30
boss_size = 40

player_rect = pygame.Rect(100, 100, player_size, player_size)
enemy_rect = pygame.Rect(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), enemy_size, enemy_size)
boss_rect = pygame.Rect(-100, -100, boss_size, boss_size)

touch_count = 0
boss_active = False

player_speed = 9
boss_speed = 2

def distance(a, b):
    return math.hypot(a.centerx - b.centerx, a.centery - b.centery)

def score_direction(x, y):
    # Новая позиция, если игрок двинется туда
    temp_rect = player_rect.copy()
    temp_rect.x += x
    temp_rect.y += y

    if not (0 <= temp_rect.x <= WIDTH - player_size and 0 <= temp_rect.y <= HEIGHT - player_size):
        return float('inf')  # не выходить за границы

    dist_to_enemy = distance(temp_rect, enemy_rect)
    danger_score = 0
    if boss_active:
        dist_to_boss = distance(temp_rect, boss_rect)
        danger_score = max(0, 150 - dist_to_boss) * 10  # чем ближе босс, тем хуже

    return dist_to_enemy - danger_score  # хотим ближе к врагу, но подальше от босса

# Основной цикл
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    if touch_count >= 3 and not boss_active:
        boss_rect.topleft = (random.randint(0, WIDTH - boss_size), random.randint(0, HEIGHT - boss_size))
        boss_active = True

    # Оценка всех направлений
    directions = [(0, -player_speed), (0, player_speed), (-player_speed, 0), (player_speed, 0)]
    best_move = min(directions, key=lambda d: score_direction(d[0], d[1]))
    player_rect.x += best_move[0]
    player_rect.y += best_move[1]

    # Босс гонится
    if boss_active:
        dx = player_rect.centerx - boss_rect.centerx
        dy = player_rect.centery - boss_rect.centery
        dist = math.hypot(dx, dy)
        if dist > 0:
            boss_rect.x += int((dx / dist) * boss_speed)
            boss_rect.y += int((dy / dist) * boss_speed)

    # Столкновение с врагом
    if player_rect.colliderect(enemy_rect):
        touch_count += 1
        print(f"Касаний: {touch_count}")
        enemy_rect.topleft = (random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size))

    # Рисуем
    pygame.draw.rect(screen, RED, player_rect)
    pygame.draw.rect(screen, BLACK, enemy_rect)
    if boss_active:
        pygame.draw.rect(screen, BLUE, boss_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
