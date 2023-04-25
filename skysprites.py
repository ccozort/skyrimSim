import pygame as pg
from pygame.sprite import Sprite
from skysettings import *
from random import randint
from random import randrange

vec = pg.math.Vector2

# player class

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # these are the properties
        self.game = game
        # add these lines for using an image with the player...
        # if not rotating, change image_orig to just image...
        self.image = pg.transform.scale(game.player_img, (64, 64))
        # self.image_orig = pg.transform.scale(game.player_img, (64, 64))
        self.image.set_colorkey(WHITE)
        # self.image_orig.set_colorkey(WHITE)
        # ignore these lines - just for rotating...
        # self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.pos = vec(0, 0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
        self.rot = 0
        self.rot_speed = 0
        self.last_update = pg.time.get_ticks()
        self.left_key = pg.K_a
        self.health = 100
        self.stamina = 100
        self.mana = 100

    def input(self):
        keystate = pg.key.get_pressed()
        # if keystate[pg.K_w]:
        #     self.acc.y = -PLAYER_ACC
        if keystate[self.left_key]:
            self.acc.x = -PLAYER_ACC
            self.rot_speed = 8
        # if keystate[pg.K_s]:
        #     self.acc.y = PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = PLAYER_ACC
            self.rot_speed = -8
        # if keystate[pg.K_p]:
        #     if PAUSED == False:
        #         PAUSED = True
        #         print(PAUSED)
        #     else:
        #         PAUSED = False
        #         print(PAUSED)
    # ...
    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 30:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits and self.canjump:
            self.vel.y = -PLAYER_JUMP
    
    def inbounds(self):
        if self.rect.x > WIDTH - 50:
            self.pos.x = WIDTH - 25
            self.vel.x = 0
            print("i am off the right side of the screen...")
        if self.rect.x < 0:
            self.pos.x = 25
            self.vel.x = 0
            print("i am off the left side of the screen...")
        if self.rect.y > HEIGHT:
            print("i am off the bottom of the screen")
        if self.rect.y < 0:
            print("i am off the top of the screen...")
    def mob_collide(self):
            hits = pg.sprite.spritecollide(self, self.game.enemies, True)
            if hits:
                print("you collided with an enemy...")
                self.game.score += 1
    def update(self):
        self.rot_speed = 0
        if self.rot > 312 or self.rot < 56:
            self.canjump = True
        else:
            self.canjump = False
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rotate()
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.x > WIDTH:
            self.pos.x = 0
        self.rect.midbottom = self.pos
        

class Mob(Sprite):
    def __init__(self, game, width,height, color):
        Sprite.__init__(self)
        self.game = game
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(randint(0,WIDTH), randint(0,HEIGHT))
        self.vel = vec(0,0)
        self.acc = vec(1,1)
        self.cofric = 0.01
        self.attached_now = False

    # ...
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            if self.vel.y > 1:
                self.vel = vec(5,-10)
            else:
                self.pos.y = hits[0].rect.top
                self.vel.y = 0
        else:
            self.vel.x = 0
    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.x < 0:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y < 0:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y > HEIGHT:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
    def attached(self, obj):
        if self.attached_now:
            self.pos = obj.pos - vec(0,16) + vec(randint(-64,64), randint(-64,64))
    def update(self):
        if not self.attached_now:
            self.acc = vec(0, PLAYER_GRAV)
            self.jump()
            self.acc.x = self.vel.x * PLAYER_FRICTION
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        else:
            self.attached(self.game.player)
        self.rect.midbottom = self.pos

# create a new platform class...

class Platform(Sprite):
    def __init__(self, x, y, width, height, color, variant):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.variant = variant
    def update(self):
        if self.variant == "moving":
            self.rect.x += 1


