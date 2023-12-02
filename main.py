import pygame,sys
from random import randint,uniform

pygame.init()

RUNNING = True
WIDTH = 1250
HEIGHT = 690
FONT = pygame.font.Font('graphics/subatomic.ttf',50)
CLOCK = pygame.time.Clock()

pygame.display.set_caption('spacy')
display_surf = pygame.display.set_mode((WIDTH,HEIGHT))

background_img = pygame.image.load('graphics/background.png').convert()

ship_img = pygame.image.load('graphics/ship.png').convert_alpha()
ship_rect = ship_img.get_rect(center = (WIDTH/2,HEIGHT/2))

laser_img = pygame.image.load('graphics/laser.png').convert_alpha()
laser_list = []

meteor_img = pygame.image.load('graphics/meteor.png').convert_alpha()
meteor_list = []

can_shoot = True
shoot_timer = None

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,400)

background_sound = pygame.mixer.Sound('sounds/music.wav')
laser_sound = pygame.mixer.Sound('sounds/laser.ogg')
collision_sound = pygame.mixer.Sound('sounds/explosion.wav')

background_sound.play(loops= -1)

def meteor_update(meteor_list,speed = 300):
    for tuple in meteor_list:
        direction = tuple[1]
        meteor_rect = tuple[0]
        meteor_rect.center += direction*speed*dt
        # if meteor_rect.top > HEIGHT:
        #     meteor_list.remove(tuple)

def laser_update(laser_list,speed = 500):
    for rect in laser_list:
        rect.y -= round(speed*dt)
        if rect.bottom < 0:
            laser_list.remove(rect)

def laser_timer(can_shoot,duration = 500):
    if not can_shoot:
        current = pygame.time.get_ticks()
        if current - shoot_timer > duration:
            can_shoot = True
    return can_shoot 

def score_update():
    score_text = f'Score:{round(pygame.time.get_ticks()/1000)}'
    space_txt = FONT.render(score_text,True,(255,255,255))
    space_txt_rect = space_txt.get_rect(center = (WIDTH/2,HEIGHT - 80))
    display_surf.blit(space_txt,space_txt_rect)
    pygame.draw.rect(display_surf,'white',space_txt_rect.inflate(30,30),width=4,border_radius=4)

while RUNNING:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            laser_rect = laser_img.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)
            can_shoot = False
            shoot_timer = pygame.time.get_ticks()
            laser_sound.play()

        if event.type == meteor_timer:
            x_pos = randint(-100,WIDTH + 100)
            y_pos = randint(-100,-50)
            meteor_rect = meteor_img.get_rect(center = (x_pos,y_pos))
            direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
            meteor_list.append((meteor_rect,direction))

    dt = CLOCK.tick(60)/1000

    meteor_update(meteor_list)

    laser_update(laser_list)

    display_surf.fill((0,0,0))
    display_surf.blit(background_img,(0,0))

    score_update()

    can_shoot = laser_timer(can_shoot,500)
    
    ship_rect.center = pygame.mouse.get_pos()
    display_surf.blit(ship_img,ship_rect)

    for rect in laser_list:
        for tuple in meteor_list:
            meteor_rect = tuple[0]
            if laser_rect.colliderect(tuple[0]):
                laser_list.remove(rect)
                meteor_list.remove(tuple)
                collision_sound.play()

    for rect in laser_list:
        display_surf.blit(laser_img,rect)

    for tuple in meteor_list:
        display_surf.blit(meteor_img,tuple[0])

    for tuple in meteor_list:
        meteor_rect = tuple[0]
        if ship_rect.colliderect(meteor_rect):
            RUNNING = False
    

    pygame.display.update()