#Создай собственный Шутер!
from pygame import *
from random import *
mixer.init()
font.init()
pause = 80
counter = 0
source = 350, 250
shet = 0
level = 1
skipping = 0
killing = 0
wait = 50
s1 = 'Пропущено: '
s2 = 'Уничтожено: '
s3 = 'Уровень: '
#создай окно игры
window = display.set_mode((700, 500))
display.set_caption('Foo_fighters')
#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
window.blit(background, (0, 0))
#Игровой цикл
game = True
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')
clock = time.Clock()
global FPS
FPS = 60
#mixer.music.play()
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, p_speed, p_s_x, p_s_y):
        super().__init__()
        self.image =  transform.scale(image.load(p_image), (p_s_x, p_s_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        if key_pressed[K_a]:
            self.rect.x -= 10
        if key_pressed[K_d]:
            self.rect.x += 10
    def restart(self):
        self.rect.x = 0
        self.rect.y = 0
    def fire(self):
        global counter
        if key_pressed[K_SPACE]:
            if counter > 10:
                counter = 0
                bullets.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 20, 50))
class Enemy(GameSprite):
    def __init__ (self, p_image, p_x, p_y, p_speed, p_s_x, p_s_y, direction):
        super().__init__(p_image, p_x, p_y, p_speed, p_s_x, p_s_y)
        self.direction = direction
        self.hp = 1
    def update(self):
        global skipping
        self.rect.y += self.speed
        if self.rect.y >= 520:
            self.hp = level
            self.rect.y = 0
            self.rect.x = randint(0, 540)
            self.rect.y = randint(0, 70)
            self.speed = randint(2, 5)
            skipping += 1
class Meteor(GameSprite):
    def __init__ (self, p_image, p_x, p_y, p_speed, p_s_x, p_s_y):
        super().__init__(p_image, p_x, p_y, p_speed, p_s_x, p_s_y)
        self.rect.x = randint(0, 540)
        self.rect.y = randint(0, 70)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 520:
            self.kill()
class Text():
    def __init__ (self, x, y, weidth, height, color = (255, 255, 255)):
        self.rect = Rect(x, y, weidth, height)
        self.color = color
    def text(self, text, k = 40):
        font1 = font.SysFont('Arial', k)
        self.question = font1.render(text, True, (255, 255, 255))
    def text_draw(self):
        window.blit(self.question, (self.rect.x, self.rect.y))
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -50:
            self.kill()
def new_start():
    appolon_11.reset()
    for k in foo_fighters:
        k.rect.y = 0
appolon_11 = Player('rocket.png', 0, 400, 8, 80, 100)
foo_fighters = sprite.Group()
bullets = sprite.Group()
apofis = sprite.Group()
foo_fighters.add(Enemy('ufo.png', 275, 0, 4, 150, 60, 'down'))
foo_fighters.add(Enemy('ufo.png', 275, 0, 4, 150, 60, 'down'))
foo_fighters.add(Enemy('ufo.png', 275, 0, 4, 150, 60, 'down'))
foo_fighters.add(Enemy('ufo.png', 275, 0, 4, 150, 60, 'down'))
foo_fighters.add(Enemy('ufo.png', 275, 0, 4, 150, 60, 'down'))
color = 255, 255, 255
skip = Text(25, 25, 100, 100, color)
kill = Text(25, 75, 100, 100, color)
levell = Text(25, 125, 100, 100, color)
while game:
    random1 = randint(0, 400//(level+1))
    counter += 1
    clock.tick(FPS)
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    key_pressed = key.get_pressed()
    appolon_11.update()
    appolon_11.fire()
    appolon_11.reset()
    foo_fighters.update()
    apofis.update()
    apofis.draw(window)
    if random1 == 1:
        apofis.add(Meteor('asteroid.png', 275, 0, 3, 100, 100))
    foo_fighters.draw(window)
    bullets.update()
    bullets.draw(window)
    skip.text(s1+str(skipping))
    skip.text_draw()
    kill.text(s2+str(killing))
    kill.text_draw()
    levell.text(s3+str(level))
    levell.text_draw()
    list_rill = sprite.groupcollide(foo_fighters, bullets, False, True)
    sprite.groupcollide(apofis, bullets, False, True)
    lr = sprite.spritecollide(appolon_11, apofis, False)
    if list_rill:
        for a in list_rill:
            a.hp -= 1
            if a.hp < 1:
                a.rect.y = -100
                a.rect.x = randint(0, 540)
                a.rect.y = randint(0, 70)
                a.hp += level
            killing += 1
            level = killing//10
    if killing == 100 and wait >= 50:
        win = font.SysFont('Arial', 70).render('YOU WIN!!!', True, (255, 215, 0))
        wait = 0
    if skipping == 28 or lr:
        win = font.SysFont('Arial', 70).render('YOU LOSE!!', True, (255, 0, 0))
        pause = 0
        skipping = 0
        killing = 0
    if wait < 50 or pause < 80:
        window.blit(win, (200, 220))
        wait += 1
        pause += 1
        if wait == 49:
            break
        if pause == 29:
            new_start()
    display.update()