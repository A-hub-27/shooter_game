import pygame
import random
from pygame import display, image, transform, key, event, QUIT, mixer
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE

pygame.init()
mixer.init()

WIDTH, HEIGHT = 700, 500
FPS = 60

BACKGROUND_IMG = "galaxy.jpg"
ROCKET_IMG = "rocket.png"
BULLET_IMG = "bullet.png"
ENEMY_IMG = "ufo.png"
ASTEROID_IMG = "asteroid.png"
FIRE_SOUND = "fire.ogg"
MUSIC = "space.ogg"


screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Space Shooter")
clock = pygame.time.Clock()


mixer.music.load(MUSIC)
mixer.music.play(-1)
fire_sound = mixer.Sound(FIRE_SOUND)


score = 0
missed = 0
font = pygame.font.SysFont('Arial', 36)

class Game:
    def __init__(self, bg_image):
        self.background = transform.scale(image.load(bg_image), (WIDTH, HEIGHT))

    def draw(self):
        screen.blit(self.background, (0, 0))

class Bullet:
    def __init__(self, x, y):
        self.image = transform.scale(image.load(BULLET_IMG), (10, 20))
        self.x = x
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y < 0

class Enemy:
    def __init__(self, x, y, speed):
        self.image = transform.scale(image.load(ENEMY_IMG), (65, 45))
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Asteroid:
    def __init__(self, x, y, speed):
        self.image = transform.scale(image.load(ASTEROID_IMG), (65, 65))
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Player:
    def __init__(self, x, y):
        self.image = transform.scale(image.load(ROCKET_IMG), (65, 70))
        self.x = x
        self.y = y
        self.speed = 5
        self.bullets = []

    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[K_RIGHT] and self.x < WIDTH - 65:
            self.x += self.speed
        if keys[K_SPACE]:
            self.shoot()

    def shoot(self):
        if len(self.bullets) < 5:
            bullet = Bullet(self.x + 27, self.y)
            self.bullets.append(bullet)
            fire_sound.play()

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)
            else:
                bullet.draw()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def show_message(text, color=(255, 0, 0)):
    font_big = pygame.font.SysFont('Arial', 50, True)
    msg = font_big.render(text, True, color)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 25))
    display.update()
    pygame.time.delay(3000)

game = Game(BACKGROUND_IMG)
player = Player(WIDTH // 2 - 32, HEIGHT - 80)
enemies = [Enemy(random.randint(0, WIDTH - 65), random.randint(-100, -40), random.randint(1, 3)) for _ in range(5)]
asteroids = [Asteroid(random.randint(0, WIDTH - 65), random.randint(-100, -40), random.randint(1, 3)) for _ in range(2)]


running = True
while running:
    screen.fill((0, 0, 0))
    game.draw()
    player.move()
    player.update_bullets()
    player.draw()

    for asteroid in asteroids[:]:
        asteroid.move()
        asteroid.draw()

    for enemy in enemies[:]:
        enemy.move()
        enemy.draw()

        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            missed += 1
            enemies.append(Enemy(random.randint(0, WIDTH - 65), random.randint(-100, -40), random.randint(1, 3)))

            for asteroid in asteroids[:]:
                if asteroid.y > HEIGHT:
                    asteroids.remove(asteroid)
                    asteroids.append(Asteroid(random.randint(0, WIDTH - 65), random.randint(-100, -40), random.randint(1, 3)))

        for bullet in player.bullets[:]:
            if (bullet.x < enemy.x + 65 and bullet.x + 10 > enemy.x and
                bullet.y < enemy.y + 45 and bullet.y + 20 > enemy.y):
                try:
                    player.bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append(Enemy(random.randint(0, WIDTH - 65), random.randint(-100, -40), random.randint(1, 3)))
                    score += 1
                except ValueError:
                    pass
        

    score_text = font.render(f"Score: {score}/3", True, (0, 255, 0))
    missed_text = font.render(f"Missed: {missed}/5", True, (255, 100, 100))
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 40))

    if score >= 5:
        show_message("YOU WIN!", (0, 255, 0))
        running = False

    if missed >= 5:
        show_message("YOU LOSE!", (255, 0, 0))
        running = False

    display.update()
    clock.tick(FPS)

    for e in event.get():
        if e.type == QUIT:
            running = False

pygame.quit()
