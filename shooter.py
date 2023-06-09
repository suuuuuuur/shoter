from pygame import *
from random import randint 
from time import time as timer


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

font.init()
font1 = font.Font(None,80)
win = font1.render('YOU WIN!!!',True , (255,255,255))
lose = font1.render('YOU LOX!!!',True, (180,0,0))
font2 = font.Font(None,36)


mixer.init()
mixer.music.load('ruapporangespace_Viktor_Cojj_-_Gruppa_krovi_47828908.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'


score = 0
lost = 0
max_lost = 20
goal = 20
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        elif keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy_1(GameSprite):
    def update(self):
        self.rect.y +=self.speed 
        global lost 
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost +=1

class Enemy_2(GameSprite):
    def update(self):
        self.rect.y +=self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1,15):
    monster = Enemy_1(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,3))
    monsters.add(monster)

asteroids = sprite.Group()
for d in range(1,2):
    asteroid = Enemy_2(img_asteroid, randint(80, win_width-80), -40, 80, 80, randint(1,5))
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False
run = True
rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
        

    if not finish:

        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        

        text = font2.render('Счёт:'+str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Пропущено:'+str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        if life == 3:
            life_colour = (0,150,0)
        if life == 2:
            life_colour = (150,150,0)
        if life == 1:
            life_colour = (150,0,0)

        text_life = font1.render(str(life),1, life_colour)
        window.blit(text_life, (650,10))
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150,0 ,0))
                window.blit(reload, (260, 460))
            else:
                rel_time = False


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy_1(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,3))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship,asteroids, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    else: 
        finish = False
        score = 0
        lost = 0
        life = 3
        num_fire = 0


        for b in bullets:
            b.kill()
        for i in monsters:
            i.kill()

        for m in asteroids:
            m.kill()


        for i in range(1,15):
            monster = Enemy_1(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        for i in range(1,2):
            asteroid = Enemy_2(img_asteroid, randint(80, win_width-80), -40, 80, 80, randint(1,5))
            asteroids.add(asteroid)

        

    time.delay(50)

        
