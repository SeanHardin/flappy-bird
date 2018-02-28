#EVEN THOUGH THE INSTRUCTIONS SAY TAP, THAT IS LITERALLY IMPOSSIBLE FOR ME. THEREFORE I USE THE KEYBOARD.
#ESC TO QUIT THE GAME
#R TO RESET THE GAME
#ANY OTHER KEY TO FLAP

import pygame#to use graphical things
from random import randrange#to randomly place pipes
pygame.init()

rightedge = 400#reference right edge of the screen
game_display = pygame.display.set_mode((rightedge,500))
clock = pygame.time.Clock()
xpos = 50#x position for the bird
groundx = 0#position for ground sprite, need to constantly change and reset it to make it scroll endlessly
ground = pygame.image.load("ground.png")#loading image
font = pygame.font.SysFont("comicsansms", 24)#font to make text
best = font.render("Best:", True, (0,50,200))#variable to show best score
instruction = font.render("Tap any key to jump", True, (0,50,200))#var to hold instructions
restart = font.render("Press r to restart", True, (0,50,200))#var to hold instructions for reset
pipelimit = 3#intended to be used as a variable, but changed method, still use as number of pipes used
pipes = []#hold all pipesets used
bg = pygame.image.load("fbg.png")#standard bg
gap = 140#amount of pixels between top and bottom pipes
spacing = 300#number of pixels between each pipe's x position
crashed = False#standard escape for the main loop
rotation = 40#angle to rotate the bird so it looks pretty
spriteno = 0;#number for sprite used, to make bird flap

class game(object):#class to store game variables that need to be changed in many places.
 floor = 450#not even sure why this is in here. maybe python yelled at me for not being able to read it.
 score = 0;#score for active game
 highestscore = 0#highest score of all games in session
 resetsuccess = False#workaround for resetting pipes when reset, could make more efficient, but i dont have the time.
 gamestarted = False#keep track of game state.
 scorenum = font.render(str(score), True, (0,50,200))#display for active score
 bestscorenum = font.render(str(highestscore), True, (0,50,200))#display for best score
 
 def incscore(self):#method to increase score
  self.score += 1;#increment score
  self.scorenum = font.render(str(game.score), True, (0,50,200))#update display
  if (self.highestscore < self.score):#if its better than best, update best too
   self.highestscore = self.score
   self.bestscorenum = font.render(str(self.highestscore), True, (0,50,200))

 def reset(self):#reset game, initializes all game variables to original values
  game.score = 0
  flappy.y = 250
  flappy.rect.y = 250
  game.resetsuccess = True
  self.scorenum = font.render(str(game.score), True, (0,50,200))
  flappy.dy = -9
  flappy.rotinc = 3
  flappy.dead = False
  self.gamestarted = False

class bird(object):#class for bird specific variables
 yhoverinc = True#for floating around before starting
 dead = False#when player dies
 rottimer = 0#timer that must elapse before bird starts rotating, aesthetic thing.
 rotinc = 3#angle to increment rotation
 y = 250#starting height
 dy = -9#amount to change height by each frame, initialized for hovering before start

 def __init__(self):#initializing the bird
  self.rect = pygame.Rect(xpos, 250, 34, 24) #the rectangle used for collision checking, matches the basic sprite dimensions
  self.birdsprites = []#array to hold each image
  self.birdsprites.append(pygame.image.load("yellowbird-midflap.png"))#include all 3 images for the flap that I found online
  self.birdsprites.append(pygame.image.load("yellowbird-downflap.png"))
  self.birdsprites.append(pygame.image.load("yellowbird-midflap.png"))#duplicate this one to look more fluid in final product
  self.birdsprites.append(pygame.image.load("yellowbird-upflap.png"))
  self.activesprite = pygame.image.load("yellowbird-midflap.png")#initialize active sprite before starting 

 def collide(self):#what to do when the bird hits a pipe
  self.dy = 13#set down velocity beyond the limit checked by main loop

 def flap(self):#what to do when bird 'flaps'
  self.dy = -12#set change in height to negative value, this means up.

class pipe(object):#class for individual pipe object, holds position and rectangle for collisions.

 def __init__(self, height, distance):#initialize based on 2 inputs passed
  self.x = distance
  self.y = height
  self.rect = pygame.Rect(self.x, self.y, 40, 320)#create collision react with same position, and 12 fewer pixels wide
   #the reduced pixels give the illusion that the bird is avoiding the pipe based on the angle even though the collision
   #rectangle does hit the right edge if the sprite barely misses it.

 def decrease(self):#moves the pipe to the left, towards the player
  self.rect.x -= 2#first move rectangle
  if (self.rect.colliderect(flappy.rect)):#if it collides, kill the player
   flappy.collide()#this sets speed below threshold to allow jumping
   flappy.dead = True
  self.x -= 2#changed position of sprite after checking collision

class pipepair(object):#class to hold each set of pipes
 passed = False#keeps track of if player has passed it, is used to increment score.
 offset = 0#used when resetting the pipes

 def __init__(self, spacing):#initialize a pipepair
  self.passed = False
  place = randrange(0,200)#adjust to screen#choose a random height to place the gap
  self.botpipe = pipe(100+gap+place, spacing)#bottom pipe placed at y for top left point, and x passed through
  self.botpipeimage = pygame.image.load("botpipe.png")#load image
  self.toppipe = pipe(100+place - 320, spacing)#same x, y is placed above the screen so the bottom of the top pipe is in right spot
  self.toppipeimage = pygame.image.load("toppipe.png")
  pipes.append(self)#adds pipepair to the array of pipes

 def reset(self):#reset position of pipes, done when pipe passes left edge of screen
  place = randrange(0,200)#create new random to use
  self.botpipe.x += spacing*pipelimit#shifts x by spacing multiplied by # of pipes
  self.botpipe.y = 100+gap+place#creates new y
  self.toppipe.x += spacing*pipelimit
  self.toppipe.y = 100+place - 320
  self.botpipe.rect.x += spacing*pipelimit#applies changes to rectangles too
  self.botpipe.rect.y = 100+gap+place
  self.toppipe.rect.x += spacing*pipelimit
  self.toppipe.rect.y = 100+place - 320
  self.passed = False#reset passed variable to reuse later.

def rotate(image, angle):#tried to do something fancy here, saw no effect so cut off excess
 return pygame.transform.rotate(image, angle)#simply returns a rotated image, done since rotation loses data

flappy = bird()#initialize bird class
game = game()#initialize game class
for a in range(3):#initialize pipepairs in pipes
 pipepair(rightedge + a*spacing)#value passed is spacing apart from the previous.

while not crashed:#standard while loop
 for event in pygame.event.get():#standard
  if(event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
   crashed = True#end the game if player exits or hits escape
  if (not game.gamestarted and event.type == pygame.KEYDOWN and event.key != pygame.K_r):
   game.gamestarted = True#dont start game until player hits some key other than r
   flappy.flap()#extra flap in here since taking input from other loop
  if (event.type == pygame.KEYDOWN):#if player presses any key
   if (event.key == pygame.K_r):#if the key is r, reset the game
    game.reset()
   if (game.resetsuccess):#manually reset pipes if game was reset
    for a in range(3):
     place = randrange(0,200)#new random
     pipes[a].botpipe.x = rightedge + spacing*a#first at right edge, next ones spacing away
     pipes[a].botpipe.y = 100+gap+place#same height method as initialize
     pipes[a].toppipe.x = rightedge + spacing*a
     pipes[a].toppipe.y = 100+place - 320
     pipes[a].botpipe.rect.x = rightedge + spacing*a
     pipes[a].botpipe.rect.y = 100+gap+place
     pipes[a].toppipe.rect.x = rightedge + spacing*a
     pipes[a].toppipe.rect.y = 100+place - 320
     pipes[a].passed = False
    game.resetsuccess = False#turn to false to not run this multiple times
   if (not flappy.dead and game.gamestarted and flappy.dy != 13):#if game is actively running, flap 
    flappy.flap()
    spriteno = 1#since flap, reset sprite, rotation timer, and rotation angle
    flappy.rottimer = 0
    rotation = 40
 if (not game.gamestarted):#before game start, float flappy around middle
  if (flappy.y < 250):#if above midline, change dy to go downward
   flappy.dy += 1
  elif (flappy.y > 250):#if below midline, change to go upward
   flappy.dy -= 1
 if (not game.gamestarted):#before game starts, just keep cycling without pause
  spriteno += 1#i use % in the selector so this can keep going
  if (spriteno == 4):
   spriteno = 0#in case neglecting this would cause integer overflow.
 if (game.gamestarted and flappy.dy < 12):#if the game is running normally
  flappy.dy += 1#simulates grabity
  spriteno += 1#simulate flapping
  flappy.rottimer += 1#increment rotation timer
 flappy.y += flappy.dy#update height with dy, this runs for both normal game and for floating before game.
 if (game.gamestarted and flappy.rottimer > 10):#if running normally and timer expired
  if (flappy.dead):#if dead, have higher rotation limit
   if (flappy.y < game.floor and rotation > -450):
    rotation -= flappy.rotinc#rotinc at this point will be higher, to simulate spiraling out of control
  elif (rotation > -90):#stop rotating while facing straight down if still alive
   rotation -= flappy.rotinc
 flappy.rect.y += flappy.dy#move rect alongside bird
 if (flappy.y < 0):#stop player from going off top of screen
  flappy.y = 0
  flappy.rect.y = 0
 if (flappy.y > game.floor):#kill and stop player if they touch bottom of screen
  flappy.dead = True
  flappy.y = game.floor
  flappy.rect.y = game.floor
 game_display.blit(bg, (0,0))#redraw the background, for cleaning up old sprites
 if (game.gamestarted and not flappy.dead):#move the ground while alive
  if (groundx <= -22):#resets the location of ground to give illusion of moving endlessly
   groundx = 0
  else:#ground hasn't reached point where it can reset seamlessly yet
   groundx -= 2
 for pipepair in pipes:#block for moving pipes left
  if (game.gamestarted and not flappy.dead):
   pipepair.botpipe.decrease()#moves each pipe left while checking collisions
   pipepair.toppipe.decrease()
   if (not pipepair.passed and pipepair.botpipe.x < 10):#if pipepair hasn't been scored from and is behind the bird
    game.incscore()#increase score
    pipepair.passed = True#set this true so it only counts once
   if (pipepair.botpipe.x < -52):#once pipes are offscreen, push them to right edge, spacing away from last pipe.
    pipepair.reset()
  elif (game.gamestarted and flappy.dead):#when flappy dies, eliminate timer before rotation and increase increment
   flappy.rotinc = 10#higher increment to simulate spiraling out of control
   flappy.rottimer = 11
  game_display.blit(pipepair.toppipeimage, (pipepair.toppipe.x, pipepair.toppipe.y))#display each pipe in the array
  game_display.blit(pipepair.botpipeimage, (pipepair.botpipe.x, pipepair.botpipe.y))
 if (game.gamestarted):#while game is active
  flappy.activesprite = rotate(flappy.birdsprites[spriteno%4], rotation)#rotate and cycle through flappy sprites
 else:#before game is running
  flappy.activesprite = flappy.birdsprites[spriteno%4]#dont rotate but do cycle sprites
 if (not game.gamestarted):#before game starts, explain the controls
  game_display.blit(instruction, (100, 30))
 game_display.blit(game.scorenum, (200, 400))#show current attempt score at all times
 game_display.blit(ground, (groundx, game.floor + 20))#place floor at x position, used var to move it constantly
 game_display.blit(flappy.activesprite, (xpos, flappy.y))#display the bird based on current sprite and current y
 if (game.gamestarted and flappy.dead):#when the player dies, display message on how to restart,
  game_display.blit(restart, (100,30))
  game_display.blit(best, (130, 300))#marks which score was the best attempt
  game_display.blit(game.bestscorenum, (200, 300))#shows the score from the best attempt in session
 pygame.display.update()#updates all the blits at once
 clock.tick(60)#framerate. except not, 30 does NOT look that choppy.
pygame.quit()#when player hits escape or exit, ends the game.