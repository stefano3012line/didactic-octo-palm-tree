import pygame as game
import numpy as np




#inizializzazione gioco
game.init()
running = True
xlim=1280
ylim=720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load("sfondo.png")
background=game.transform.smoothscale(background,(xlim,ylim))
muri=game.image.load("muri.png")
muri=game.transform.smoothscale(muri,(xlim/10,ylim/10))




# inizializzazione dati player
x,y=(20,20)
speed=6
vector=(0,0)
pg=game.image.load("pg.png").convert_alpha()
class player(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        screen.blit(pg,(x,y)) # To draw the hit box around the player
    def draw(self,screen):
        screen.blit(pg,(x,y))

man_mask=game.mask.from_surface(pg)

wall_mask=game.mask.from_surface(muri)
wall_immage=wall_mask.to_surface()






while running:

    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    game.display.flip()
    screen.blit(background,(0,0))

    screen.blit(wall_immage,(0,500))
    #game speed
    clock.tick(24)

    #player movement
    man=player(x,y)

    if  game.key.get_pressed()[game.K_s]:
        vector=(0,1)
    if  game.key.get_pressed()[game.K_w]:
        vector=(0,-1)
    if  game.key.get_pressed()[game.K_d]:
        vector=(1,0)
    if  game.key.get_pressed()[game.K_a]:
        vector=(-1,0)
    
    x+=speed*vector[0]
    y+=speed*vector[1]
    if x>1330:
        x-=1340
    if x<-50:
        x+=1330
    man.draw(screen)

    man_mask=game.mask.from_surface(pg)
    if man_mask.overlap(wall_mask,(0,0)):
        speed=1
    else:
        speed=6
 


    game.display.update()
game.quit()
