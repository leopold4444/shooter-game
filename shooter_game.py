#Создай собственный Шутер!
#123
from random import*
from pygame import*
from time import time as timer
win_height = 500
win_width = 700
window = display.set_mode((win_width,win_height))
display.set_caption('space shooter')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
clock = time.Clock()
fps = 50
game = True
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
lost = 0
goal = 10
finish = False
font.init()
font1 = font.SysFont('Arial',70)
font2 = font.SysFont('Arial',50)
win = font1.render('Победа!',True,(170, 233, 0))
lose = font1.render('Поражение!',True,(178, 1, 40))
class Game_sprite(sprite.Sprite):
    def __init__(self,pic,x,y,speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(pic),(width,height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(Game_sprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,5,15)
        bullets.add(bullet)
class Enemy(Game_sprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,635)
            lost += 1
class Bullet(Game_sprite):
        def update(self):
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.kill()
bullets = sprite.Group()
player = Player('rocket.png',350,400,5,65,75)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(0,635),-50,randint(1,3),65,55) 
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(0,635),-50,randint(1,3),65,55)
    asteroids.add(asteroid)
run = True
score = 0
num_fire = 0
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True 
                    fix_time = timer()
    if finish != True:
        window.blit(background,(0,0))
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        player.reset()
        player.update()
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters,bullets,True,True)
        if rel_time == True:
            now_time = timer()
            if (now_time - fix_time) < 3:
                reload = font1.render('перезарядка',True,(170, 233, 0))
                window.blit(reload,(350,425))
            else:
                num_fire = 0
                rel_time = False
        for collide in collides:
            score += 1
            monster = Enemy('ufo.png',randint(0,635),-50,randint(1,3),65,55) 
            monsters.add(monster)
        if sprite.spritecollide(player,monsters,False) or lost >= 5 :
            finish = True
            window.blit(lose,(200,200))
        if score == goal:
            finish = True
            window.blit(win,(200,200))
        text1 =font2.render('Счет:' + str(score),True,(255,255,255))
        window.blit(text1,(10,10))
        text2 = font2.render('Пропущено:' + str(lost),True,(255,255,255))
        window.blit(text2,(10,40))
    display.update()
    clock.tick(fps)
