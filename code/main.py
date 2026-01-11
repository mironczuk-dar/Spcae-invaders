import pygame
import random
from sys import exit

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Klasa Gracza
class Player:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 5

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

# Klasa Pocisku
class Bullet:
    def __init__(self, x, y):
        self.x = x + 22
        self.y = y
        self.speed = -7

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 5, 15))

# Klasa Przeciwnika (Kosmity)
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 2

    def update(self, direction):
        self.x += self.speed * direction

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Główna funkcja gry
def main():
    clock = pygame.time.Clock()
    player = Player()
    bullets = []
    enemies = []
    enemy_direction = 1
    enemy_drop = 0
    
    # Tworzenie floty przeciwników
    for row in range(5):
        for col in range(10):
            enemies.append(Enemy(col * 60 + 50, row * 50 + 50))

    running = True
    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x, player.y))
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        # Ruch gracza
        player.move(keys)
        player.draw()

        # Obsługa pocisków
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw()
            if bullet.y < 0:
                bullets.remove(bullet)

        # Obsługa przeciwników
        move_down = False
        for enemy in enemies:
            enemy.update(enemy_direction)
            enemy.draw()
            if enemy.x + enemy.width >= SCREEN_WIDTH or enemy.x <= 0:
                move_down = True

        if move_down:
            enemy_direction *= -1
            for enemy in enemies:
                enemy.y += 10

        # Kolizje (Pocisk z Przeciwnikiem)
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + 5 > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + 15 > enemy.y):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        # Warunki końca gry
        if not enemies:
            print("Wygrana!")
            running = False
        
        for enemy in enemies:
            if enemy.y + enemy.height >= player.y:
                print("Przegrana!")
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()