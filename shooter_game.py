import pygame
from pygame import *
from pygame import mixer
from time import time as timer
from random import randint

window_h = 500
window_w = 700
window = display.set_mode((window_w, window_h))
display.set_caption("space")

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

FPS = 60
lost = 0
score = 0
life = 3


font.init()
font1 = font.Font("Arial", 80)
font2 = font.Font("Arial", 36)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE", True, (180, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, size_x, size_y, p_speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (size_x, size_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
        self.size_x = size_x
        self.size_y = size_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < window_w - 80:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > window_h:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1


bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy("asteroid.png", randint(30, window_w-30), -40, 80, 50, randint(1,10))
    asteroids.add(asteroid)
player = Player("rocket.png", 350, 400, 80, 100, 10)

for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, window_w - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

goal = 10
max_lost = 10

num_fire = 0
rel_time = False

finish = False
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.shoot()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time == True



    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("WAIT, AAAAAA", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False



        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, window_w - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1


        
        if lost == max_lost or life == 0:
            finish = True
            window.blit(lose, (200, 200))



        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if life == 3:
            life_color = (0, 250, 0)
        if life == 2:
            life_color = (250, 250, 0)
        if life == 1:
            life_color = (255, 0, 0)
        

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        num_fire = 0
        bullets.empty()
        monsters.empty()


        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy("ufo.png", randint(80, window_w - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy("asteroid.png", randint(80, window_w-80), -40, 80, 50, randint(1,5))
            asteroids.add(asteroid)

    time.delay(50)