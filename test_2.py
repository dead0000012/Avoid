import pygame
import random
import math

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Автоматическая игра")
clock = pygame.time.Clock()

# Цвета
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Размеры и объекты
player_size = 30
enemy_size = 30
boss_size = 40

player_rect = pygame.Rect(100, 100, player_size, player_size)
enemy_rect = pygame.Rect(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), enemy_size, enemy_size)
boss_rect = pygame.Rect(-100, -100, boss_size, boss_size)

touch_count = 0
boss_active = False

# Скорости
player_speed = 20
boss_speed = 2

# Движение игрока к точке
def move_towards(target_rect, goal_rect, speed):
    dx = goal_rect.centerx - target_rect.centerx
    dy = goal_rect.centery - target_rect.centery
    dist = math.hypot(dx, dy)
    if dist != 0:
        dx /= dist
        dy /= dist
        target_rect.x += int(dx * speed)
        target_rect.y += int(dy * speed)

# Главный цикл
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Автодвижение игрока к чёрному квадрату
    move_towards(player_rect, enemy_rect, player_speed)

    # Столкновение с чёрным квадратом
    if player_rect.colliderect(enemy_rect):
        touch_count += 1
        print(f"Счётчик касаний: {touch_count}")
        enemy_rect.topleft = (
            random.randint(0, WIDTH - enemy_size),
            random.randint(0, HEIGHT - enemy_size)
        )
        if touch_count >= 50 and not boss_active:
            boss_rect.topleft = (
                random.randint(0, WIDTH - boss_size),
                random.randint(0, HEIGHT - boss_size)
            )
            boss_active = True

    # Босс гонится за игроком
    if boss_active:
        move_towards(boss_rect, player_rect, boss_speed)

    # Рисуем
    pygame.draw.rect(screen, RED, player_rect)
    pygame.draw.rect(screen, BLACK, enemy_rect)
    if boss_active:
        pygame.draw.rect(screen, BLUE, boss_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
