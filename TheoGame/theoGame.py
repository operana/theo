#7.8.25 MY FIRST VIDEO GAME ATTEMPT! Following along with The ultimate introduction to Pygame by Clear Code - video on Youtube
#Goal is not to create complex game on a advanced game engine, but to use pygame to learn basics and strengthen understanding of programming
#using adobestock for cc0 images
#to have path consistency-keep images in same folder where code is: can have 3 diff folders: graphs, fonts, audio




import pygame
from sys import exit #used to close any code once we call it

pygame.init() #call at beginning, essentially starts and initiates subparts of pygame needed

#Starter Variables
screen = pygame.display.set_mode((800,400)) #(tuple (width, height)) #create display surface (what player sees), stored in screen variable
pygame.display.set_caption("Theo's World :)") #set game title, pass in String
clock = pygame.time.Clock() #clock object helps with time and control frame rate
pixel_font = pygame.font.Font("Documents/TheoGame/PixelGame.otf", 75) #TEXT STEP 1: create font object with type and size (font type, font size integer) ////None is default type

#Creating Surfaces
#test_surface = pygame.Surface((100,200)) #create a regular surface (default rectangle), accepts tuple with width and height. but need to actually show it on display surface within while loop below
#test_surface.fill('thistle3') #fill regular surface with a predefined pygame color code
#to import image: pygame.image.load('string of image path')
graphics_path = "Documents/TheoGame/graphics/"
cafe_surface = pygame.image.load(graphics_path + 'backgrounds/cafe.png').convert_alpha() #convert_alpha() converts image to something pygame can work with more easily so game runs faster

theo_surface = pygame.image.load(graphics_path + 'player/TheoSpriteSmall.png').convert_alpha()
theo_rectangle = theo_surface.get_rect(midbottom = (400, 310)) #.rect() takes surface and draws rectangle around it. later on, will make this process more streamlined with Sprite class

text_surface = pixel_font.render("theo's world", False, 'cadetblue3') #TEXT STEP 2: create text surface object // (text string, AA or antialias aka smoothing edges of text and usually want this to be True unless working with pixel art then would be False because the appearance fits better, color)
text_surface2 = pixel_font.render("theo's world", False, 'gray15') #TEXT STEP 2: create text surface object // (text string, AA or antialias aka smoothing edges of text and usually want this to be True unless working with pixel art then would be False because the appearance fits better, color)

ube_surface = pygame.image.load(graphics_path + 'items/ubeSmall.png').convert_alpha()
#ube_x_pos = 700
ube_rectangle = ube_surface.get_rect(midbottom = (700, 385))



#while true loop to keep code running forever otherwise display screen would just immediately close after running
#game exists inside while loop
#draw all our elements
#update everything
while True:
    #first line to check for all possible types of player input (note: important also to close game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #QUIT is a constant that is synonymous with 'X'/close button of a window. allows us to close game.
            pygame.quit() #whenever we call pygame.quit(), essentially is opposite of pygame.init(). 
            exit() #closes code entirely. closes while loop, so we don't call display update line below after closing (which would otherwise result in error message)

    
    #showing surfaces on the screen at 60 fps
    screen.blit(cafe_surface, (0,0)) #this displays a regular surface on the display surface. process: call display surface itself, then blit aka block image transfer (put one surface on another surface). arguments: (surface to place, position) coordinate system
    screen.blit(theo_surface, theo_rectangle)

    
    screen.blit(text_surface2, (205,25)) #TEXT STEP 3: blit text surface
    screen.blit(text_surface, (200,20)) #TEXT STEP 3: blit text surface
    
    #basic animations: animating each surface just means changing the position slightly on each frame. use screen.blit that uses a variable that continuously changes the position, recall that our surfaces are constantly being 'updated' at 60 fps. When it's static on the screen, just means that the position is not being altered from frame to frame
    ube_rectangle.left -= 3 #get ube to move to the left
    if ube_rectangle.right <= 0 : #if the right side is <= 0, indicates ube has left the screen, so move back to the right
        ube_rectangle.left = 800 #if statement to place ube surface back to the right if it moves off screen
    screen.blit(ube_surface, ube_rectangle)
    

    
    pygame.display.update() #continuously update display service to player
    clock.tick(60) #set max frame rate: 60 integer tells pygame that the while true loop should not run faster than 60 fps...don't really have to worry about min frame rate for basic 2d game in pygame

#left off 1:03:50 collisions with rectangles