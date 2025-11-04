import pygame as game
import numpy as np

#inizializzazione gioco
game.init()
running = True
xlim=1280
ylim=720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load("C:/Users/Dell/Desktop/memes/games pyton/unipipi.jpeg")
background=game.transform.smoothscale(background,(xlim,ylim))


#info giocatore
x=xlim/2
y=ylim/2
size = 80
speed= 10



#info ostacolo
e_size=200
O_x= np.random.randint(e_size,xlim-e_size)
O_y= - 2*e_size
e_dir= 1
e_speed=150

e_accell=20
enemy=game.image.load("C:/Users/Dell/Desktop/memes/games pyton/bolognesi.jpeg")
enemy=game.transform.smoothscale(enemy,(e_size,e_size))

while running:

    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    game.display.flip()
    screen.blit(background,(0,0))


    #game speed
    clock.tick(60)



    #player movement
    if  game.key.get_pressed()[game.K_s]and y <= ylim - (size+speed):
        y+=speed
    if  game.key.get_pressed()[game.K_w]and y >= size+speed:
        y-=speed
    if  game.key.get_pressed()[game.K_d] and x <= xlim -(size+speed):
        x+=speed
    if  game.key.get_pressed()[game.K_a] and x >= size + speed:
        x-=speed




    #player character
    #game.draw.circle(screen,'black',(x,y),size)
    immage=game.image.load("C:/Users/Dell/Desktop/memes/games pyton/franchino.jpg")
    immage=game.transform.smoothscale(immage,(size,size))
    screen.blit(immage,(x,y))





    #enemy movement
    if e_dir == 0:#from north
        if O_y>= -(2*e_size) and O_y<=ylim+(e_size*2):
            screen.blit(enemy,(O_x,O_y))
            O_y+=e_speed/(0.3*e_size)


    elif e_dir == 1:#from south
        if O_y>= -(2*e_size) and O_y<=ylim+(e_size*2):
            screen.blit(enemy,(O_x,O_y))
            O_y -= e_speed/(0.3*e_size)


    elif e_dir == 2:#from est
        if O_x>= -(2*e_size) and O_x<=xlim+(2*e_size):
            screen.blit(enemy,(O_x,O_y))
            O_x -= e_speed/(0.3*e_size)



    elif e_dir == 3:#from west
        if O_x>= -(2*e_size) and O_x<=xlim+(2*e_size):
            screen.blit(enemy,(O_x,O_y))
            O_x += e_speed/(0.3*e_size)


        #giving random dir
    if O_y< -(2*e_size) or O_y>ylim+(e_size*2) or O_x< -(2*e_size) or O_x>xlim+(e_size*2) :
        e_dir = np.random.randint(0,4)
        print(e_size)



#spawn for different directions size and speed
        if e_dir == 0:#from north
            e_size=np.random.randint(size,3*size)
            O_x= np.random.randint(e_size,xlim-e_size)
            O_y= -(2*e_size)
            e_speed+= e_accell
        elif e_dir == 2:#from est
            e_size=np.random.randint(size,3*size)
            O_y= np.random.randint(e_size,ylim-e_size)
            O_x= xlim+(2*e_size)
            e_speed+= e_accell
        elif e_dir == 1:#from south
            e_size=np.random.randint(size,3*size)
            O_x= np.random.randint(e_size,xlim-e_size)
            O_y= ylim +(2*e_size)
            e_speed+= e_accell
        elif e_dir == 3:#from west
            e_size=np.random.randint(size,3*size)
            O_y= np.random.randint(e_size,ylim-e_size)
            O_x= -(2*e_size)
            e_speed+= e_accell
    enemy=game.transform.smoothscale(enemy,(e_size,e_size))


    #getting hit
    if np.abs(x-O_x)<=size+e_size and np.abs(y-O_y)<=size+e_size:
        size =  (size/2)-14
        O_y = ylim +1000
        e_speed= e_speed*0.2
    if size <= 0 or size>=100:
        drunning=False





    game.display.update()
game.quit()