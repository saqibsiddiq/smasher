import pygame,sys
from random import randint,uniform

pygame.init()

RUNNING = True
WIDTH = 1250
HEIGHT = 690
CLOCK = pygame.time.Clock()

pygame.display.set_caption('spacy')
display_surface = pygame.display.set_mode((WIDTH,HEIGHT))

background_surface = pygame.image.load('graphics/background.png').convert()

background_music = pygame.mixer.Sound('sounds/music.wav')

class Ship(pygame.sprite.Sprite):
    def __init__(self,group):
        super().__init__(group)

        self.image = pygame.image.load('graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH/2,HEIGHT/2))
        self.mask = pygame.mask.from_surface(self.image)
        self.can_shoot = True
        self.shoot_time = None
        self.laser_sound = pygame.mixer.Sound('sounds/laser.ogg')

    def input_pos(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_timer(self,duration = 300):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > duration:
                self.can_shoot = True

    def shoot_laser(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            Laser(laser_group,self.rect.midtop)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self,meteor_group,False,pygame.sprite.collide_mask):
            sys.exit()

    def update(self):
        self.laser_timer()
        self.input_pos()
        self.shoot_laser()
        self.meteor_collision()

class Laser(pygame.sprite.Sprite):
    def __init__(self,group,pos):
        super().__init__(group)

        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midtop = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.midtop)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 500
        self.collision_sound = pygame.mixer.Sound('sounds/explosion.wav')

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self,meteor_group,True,pygame.sprite.collide_mask):
            self.collision_sound.play()
            self.kill()

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        if self.rect.bottom < 0:
            self.kill()
        self.meteor_collision()

class Meteor(pygame.sprite.Sprite):
    def __init__(self,group,pos):
        super().__init__(group)

        meteor_image = pygame.image.load('graphics/meteor.png').convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_image.get_size())*uniform(0.5,1.5)
        self.scaled_image = pygame.transform.scale(meteor_image,meteor_size)
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(500,700)
        self.rotation = 0
        self.rotation_speed = randint(20,50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_image,self.rotation,1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        if self.rect.top > HEIGHT:
            self.kill()
        self.rotate()

class Score():
    def __init__(self):
        self.font = pygame.font.Font('graphics/subatomic.ttf',50)
        
    def display(self):
        score_text = f'Score: {pygame.time.get_ticks()//1000}'
        text_surface = self.font.render(score_text,True,'white')
        text_rect = text_surface.get_rect(center = (WIDTH/2,HEIGHT-80))
        display_surface.blit(text_surface,text_rect)
        pygame.draw.rect(display_surface,'white',text_rect.inflate(30,30),width=8,border_radius=5)



ship_group = pygame.sprite.Group()
ship = Ship(ship_group)

laser_group = pygame.sprite.Group()

meteor_group = pygame.sprite.Group()
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,400)

background_music.play(loops= -1)

while RUNNING:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            sys.exit()

        if event.type == meteor_timer:
            meteor_ypos = randint(-150,-50)
            meteor_xpos = randint(-100,WIDTH + 100)
            Meteor(meteor_group,(meteor_xpos,meteor_ypos))

    dt = CLOCK.tick(60)/1000

    ship_group.update()
    laser_group.update()
    meteor_group.update()

    display_surface.blit(background_surface,(0,0))
    Score().display()
    laser_group.draw(display_surface)
    ship_group.draw(display_surface)
    meteor_group.draw(display_surface)
    

    pygame.display.update()



