import pygame
import random
import sys
pygame.init()
WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Avoid")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 80
player_speed = 7

enemy_width = 20
enemy_height = 20
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -enemy_height
enemy_speed = 6
last_enemy_add_score = 0
score = 0

font = pygame.font.SysFont(None, 36)

def create_enemy():
    return {
        "x" : random.randint(0, WIDTH-enemy_width),
        "y" : random.randint(-300, -enemy_height)
    }

enemies = [create_enemy()]

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    if player_x < 0:
        player_x = 0

    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for enemy in enemies:
        enemy["y"] += enemy_speed

        if enemy["y"] > HEIGHT:
            enemy["y"] = random.randint(-300, -enemy_height)
            enemy["x"] = random.randint(0, WIDTH - enemy_width)
            score += 1

            if score % 3 == 0:
                enemy_speed += 2

    if score >= last_enemy_add_score + 10:
        enemies.append(create_enemy())
        enemy_speed -= 4
        last_enemy_add_score = score



    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)

        if player_rect.colliderect(enemy_rect):
            print("게임종료")
            print(f"최종점수:{score}")
            running = False

    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, player_rect)

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
        pygame.draw.rect(screen, RED, enemy_rect)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    pygame.display.update()

pygame.quit()
sys.exit()
