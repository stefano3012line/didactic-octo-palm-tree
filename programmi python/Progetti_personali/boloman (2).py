import pygame as game
import numpy as np




#inizializzazione gioco
game.init()
running = True
i=0
change_direction=0
xlim=1280
ylim=720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load("pacman1.png")
background=game.transform.smoothscale(background,(xlim,ylim))



# inizializzazione dati player

pacman = game.image.load("pg.png").convert_alpha()
pacman_mask = game.mask.from_surface(pacman)



muri = game.image.load("pacman2.png").convert_alpha()
muri=game.transform.smoothscale(muri,(xlim,ylim))
muri_mask = game.mask.from_surface(muri)
mask_image = muri_mask.to_surface()

x,y=(35,35)
speed=6
vector=(0,0)

class player(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        screen.blit(pacman,(x,y)) # To draw the hit box around the player
    def draw(self,screen):
        screen.blit(pacman,(x,y))







while running:
    
    #screen.blit(mask_image, (0, 0))
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    game.display.flip()
    screen.blit(background,(0,0))


    #game speed
    game_speed=24
    clock.tick(game_speed)

    #player movement
    man=player(x,y)

    if  game.key.get_pressed()[game.K_s]:
        change_direction=0
        i=0
        #vector=(0,1)
    if  game.key.get_pressed()[game.K_w]:
        change_direction=1
        i=0
        #vector=(0,-1)
    if  game.key.get_pressed()[game.K_d]:
        change_direction=2
        i=0
        #vector=(1,0)
    if  game.key.get_pressed()[game.K_a]:
        change_direction=3
        i=0
        #vector=(-1,0)
    

    if i<=game_speed/2:
        if change_direction==0:
             vector=(0,1)
        elif change_direction==1:
            vector=(0,-1)
        elif change_direction==2:
            vector=(1,0)
        elif change_direction==3:
            vector=(-1,0)   



    x+=speed*vector[0]
    y+=speed*vector[1]
    
    
    #effetto pacman
    if x>1330:
        x-=1340
    if x<-50:
        x+=1330
    man.draw(screen)

    
    if muri_mask.overlap(pacman_mask,(x,y)):
        speed=1
    else:
        speed=6
 


    game.display.update()
    i+=1
game.quit()
