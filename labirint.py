from pygame import *

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, x, y , width, height):
        sprite.Sprite.__init__(self) #connect dgn class sblmnya
        self.image = image.load(player_image) #ambil gmbr
        self.image = transform.scale(self.image,(width,height)) #merubah ukuran
        self.rect = self.image.get_rect() #buat rect utk obj gambar
        self.rect.x = x #posisi x
        self.rect.y = y #posisi y

    def reset(self): #memunculkan obj
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def __init__(self, player_image, x, y, width, height, speed_x, speed_y):
        GameSprite.__init__(self, player_image,x, y, width, height)
        self.speed_x = speed_x #kecepatan x
        self.speed_y = speed_y #kec y

    def update(self): #method utk char bergerak
        if pacman.rect.x > 0 and pacman.speed_x < 0: #batas kiri
            self.rect.x += self.speed_x
        if pacman.rect.x < win_width - 80 and pacman.speed_x > 0: #80px size sprite kt, ini batas kanan
            self.rect.x += self.speed_x

        platform_touched = sprite.spritecollide(self, barriers, False) #false = ada sprite yg ilang, true vice versa
        if self.speed_x>0:
            for p in platform_touched:
                self.speed_x = 0 #spy gbs nembus
                if p.rect.left  < self.rect.right:
                    self.rect.right = p.rect.left #biar kl di click2 lgsg dibalikin ke border kiri tembok
        if self.speed_x<0: #bag kanan
            for p in platform_touched:
                self.speed_x = 0 #spy gbs nembus
                if p.rect.right > self.rect.left:
                    self.rect.left = p.rect.right
        

        #atas bawah
        if pacman.rect.y > 0 and pacman.speed_y < 0: #batas atas?
            self.rect.y += self.speed_y
        if pacman.rect.y < win_height - 80 and pacman.speed_y > 0: 
            self.rect.y += self.speed_y
        
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_y>0:
            for p in platform_touched:
                self.speed_y = 0 
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top

        if self.speed_y<0: 
            for p in platform_touched:
                self.speed_y = 0 
                if p.rect.bottom > self.rect.top:
                    self.rect.top = p.rect.bottom

    def fire(self):
        bullet = Bullet('bulletnew.png', self.rect.right, self.rect.centery, 15, 20, 15)#dikanan char kita, y nya di tgh2 kita
        bullets.add(bullet)


class Bullet(GameSprite):
    def __init__ (self, player_image,x , y, width, height, speed_x):
        GameSprite.__init__(self, player_image, x, y, width, height)
        self.speed = speed_x
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width +10:
            self.kill()

class Enemy(GameSprite):
    side = 'left'
    def __init__ (self, player_image, x, y, width, height, speed_x):
        GameSprite.__init__(self, player_image, x, y, width, height)
        self.speed = speed_x
    
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right' #kl udh smp ujung dia muter balik
        if self.rect.x >= win_width - 80:
            self.side = 'left'

        if self.side =='left':
            self.rect.x -= self.speed
        elif self.side == 'right':
            self.rect.x += self.speed

bullets = sprite.Group() #digrupin

win_height = 500
win_width = 700
bg = transform.scale(image.load("bgnew.png"), (win_width, win_height))
window = display.set_mode((win_width, win_height)) #membuat window/display
display.set_caption('CADET, HELP!') #judul app

pacman = Player('player game1.png', 5, win_height - 80, 80, 80, 0 , 0)
w1 = GameSprite('platform2.png', 116, 300, 300, 50)
w3 = GameSprite('platform2.png', 0, 100, 300, 50)
w2 = GameSprite('platform2_v.png', 380, 100, 50, 400)
final_sprite = GameSprite('rocket game1.png', win_width-130, win_height-110, 120, 120)
finish = False

barriers = sprite.Group() #menggabungkn 2 wall
barriers.add(w1) #tembok ke1
barriers.add(w2) #tembok ke2
barriers.add(w3)

monsters = sprite.Group()
monster1 = Enemy('alien game1.png', win_width-80, 150 , 80, 80, 5)
monster2 = Enemy('alien game1.png', win_width-80, 250 , 80, 80, 5)
monsters.add(monster1)
monsters.add(monster2)

run = True #variabel utk cek looping

while run:
    time.delay(50) #ksh delay dikit

    for e in event.get(): #looping event
        if e.type == QUIT: #kluar dr game
            run = False
        elif e.type == KEYDOWN: #gerak pk keyboard. e.key = event keyboard
            if e.key == K_a:
                pacman.speed_x = -5
            if e.key == K_d:
                pacman.speed_x = 5
            if e.key == K_w:
                pacman.speed_y = -5
            if e.key == K_s:
                pacman.speed_y = 5

            if e.key == K_SPACE: #space bar
                pacman.fire()
        
        elif e.type == KEYUP: #ktk ga di click kembali ke 0
            if e.key == K_a:
                pacman.speed_x = 0
            if e.key == K_d:
                pacman.speed_x = 0
            if e.key == K_w:
                pacman.speed_y = 0
            if e.key == K_s:
                pacman.speed_y = 0

    if not finish:
        window.blit(bg,(0,0)) #masukin warna background
        bullets.update()
        bullets.draw(window)
        barriers.draw(window)
        pacman.update() #pacman bergerak
        pacman.reset() #pacman muncul
        final_sprite.reset()
        sprite.groupcollide(bullets, barriers, True, False)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, monsters, True, True)

        if sprite.spritecollide(pacman, monsters, False):
            finish = True
            window.fill((0, 0, 0))
            img = image.load('lose bg.png')
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))

        if sprite.collide_rect(pacman, final_sprite):
            finish = True
            window.fill((255, 255, 255))
            img = image.load('win bg.png')
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))
        


    
    display.update() #mengupdate konten supaya muncul