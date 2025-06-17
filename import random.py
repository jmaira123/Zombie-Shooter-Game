import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
ZOMBIE_SPAWN_RATE = 50
PLAYER_SPEED = 5
BULLET_SPEED = 10
ZOMBIE_SPEED = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED

# Zombie class
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        self.rect.y += ZOMBIE_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            return True
        return False

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zombie Shooter")
    clock = pygame.time.Clock()

    player = Player()
    all_sprites = pygame.sprite.Group()
    zombies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    all_sprites.add(player)

    running = True
    score = 0
    missed_zombies = 0
    zombie_spawn_timer = 0
    start_time = pygame.time.get_ticks()

    level = 1
    level_score_targets = {1: 30, 2: 40, 3: 50}
    game_state = "playing"  # could be "playing", "win", or "lose"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_state == "playing":
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.center)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        if game_state == "playing":
            zombie_spawn_timer += 1
            if zombie_spawn_timer >= ZOMBIE_SPAWN_RATE:
                zombie = Zombie()
                all_sprites.add(zombie)
                zombies.add(zombie)
                zombie_spawn_timer = 0

            all_sprites.update()

            for bullet in bullets:
                hit_zombies = pygame.sprite.spritecollide(bullet, zombies, True)
                score += len(hit_zombies)
                if hit_zombies:
                    bullet.kill()

            for zombie in zombies:
                if zombie.update():
                    missed_zombies += 1

            if pygame.sprite.spritecollideany(player, zombies):
                game_state = "lose"

            if level < 3 and score >= level_score_targets[level]:
                level += 1
            elif level == 3 and score >= level_score_targets[3]:
                game_state = "win"

        screen.fill(BLACK)
        all_sprites.draw(screen)

        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f'Score: {score}', True, WHITE), (10, 10))
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        screen.blit(font.render(f'Time: {elapsed_time} s', True, WHITE), (10, 50))
        screen.blit(font.render(f'Missed Zombies: {missed_zombies}', True, WHITE), (10, 90))
        screen.blit(font.render(f'Level: {level}', True, WHITE), (10, 130))

        if game_state == "win":
            msg = font.render("🎉 You Win! 🎉", True, GREEN)
            screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2))
        elif game_state == "lose":
            msg = font.render("💀 Game Over! 💀", True, RED)
            screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

        if game_state in ["win", "lose"]:
            pygame.time.delay(3000)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

