import pygame
import random
import math

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Умный автоигрок")
clock = pygame.time.Clock()

# Цвета
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Размеры
player_size = 30
enemy_size = 30
boss_size = 40

player_rect = pygame.Rect(100, 100, player_size, player_size)
enemy_rect = pygame.Rect(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), enemy_size, enemy_size)
boss_rect = pygame.Rect(-100, -100, boss_size, boss_size)

touch_count = 0
boss_active = False

player_speed = 20
boss_speed = 2

def distance(rect1, rect2):
    return math.hypot(rect1.centerx - rect2.centerx, rect1.centery - rect2.centery)

def move_towards(rect, target, speed):
    dx = target.centerx - rect.centerx
    dy = target.centery - rect.centery
    dist = math.hypot(dx, dy)
    if dist != 0:
        dx /= dist
        dy /= dist
        rect.x += int(dx * speed)
        rect.y += int(dy * speed)

def move_away(rect, danger, speed):
    dx = rect.centerx - danger.centerx
    dy = rect.centery - danger.centery
    dist = math.hypot(dx, dy)
    if dist != 0:
        dx /= dist
        dy /= dist
        rect.x += int(dx * speed)
        rect.y += int(dy * speed)

# Главный цикл
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    if touch_count >= 15 and not boss_active:
        boss_rect.topleft = (
            random.randint(0, WIDTH - boss_size),
            random.randint(0, HEIGHT - boss_size)
        )
        boss_active = True

    if boss_active and distance(player_rect, boss_rect) < 80:
        move_away(player_rect, boss_rect, player_speed) 
    else:
        move_towards(player_rect, enemy_rect, player_speed)

    if boss_active:
        move_towards(boss_rect, player_rect, boss_speed)

    # Касание с врагом
    if player_rect.colliderect(enemy_rect):
        touch_count += 1
        print(f"Счётчик: {touch_count}")
        enemy_rect.topleft = (
            random.randint(0, WIDTH - enemy_size),
            random.randint(0, HEIGHT - enemy_size)
        )

    # Рисуем
    pygame.draw.rect(screen, RED, player_rect)
    pygame.draw.rect(screen, BLACK, enemy_rect)
    if boss_active:
        pygame.draw.rect(screen, BLUE, boss_rect)

    player_rect.clamp_ip(screen.get_rect())
    boss_rect.clamp_ip(screen.get_rect())
    enemy_rect.clamp_ip(screen.get_rect())
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
