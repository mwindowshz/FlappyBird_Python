import pygame
import pygame.event
# from pygame.locals import *

import sys , random

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,screen_dim[1]-floor_size[1]))
    screen.blit(floor_surface,(floor_x_pos+screen.get_size()[0],screen_dim[1]-floor_size[1]))

def create_pipe():
    random_pipe_pos = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(midtop=(screen_dim[0]+50,random_pipe_pos)) #midtop is the middle point of top of rectangel #create pipe on x that is out of the screen so it would come from left to right of whole screen
    top_pipe = pipe_surface.get_rect(midbottom =(screen_dim[0]+50,random_pipe_pos -120)) #midbottom is middel of bottom of rectangle #create pipe on x that is out of the screen so it would come from left to right of whole screen
    return bottom_pipe,top_pipe
    
#move all the pipes to the left to create motion
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx-=3
    return pipes
#draw all pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_dim[1]: #this is a pipe on bottom of screen, top pipe would never reach this postion
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collistion(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            print("collisiton")
            return False
    #check if bird is too high or too low
    if bird_rect.top <= -100 or bird_rect.bottom >= screen_dim[1] - floor_size[1]:
        print("left screen")
        return False
    return True
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,- bird_movment * 3,1)
    return new_bird

def score_display(game_state):
    if game_state:
        score_surface = game_font.render(str(int(score)),True,(0,255,255))
        score_rect = score_surface.get_rect(center = (screen_dim[0]/2,40))
        screen.blit(score_surface,score_rect)
    else:
       score_surface = game_font.render(str(int(score)),True,(0,255,255))
       score_rect = score_surface.get_rect(center = (screen_dim[0]/2,40))
       screen.blit(score_surface,score_rect)
       score_surface = game_font.render('High Score: ' + str(int(high_score)),True,(0,0,255))
       score_rect = score_surface.get_rect(center = (screen_dim[0]/2,80))
       screen.blit(score_surface,score_rect) 

    
#START GAME
pygame.mixer.pre_init(buffer = 512)
pygame.init()
#create a window, surface to draw on
# screen = pygame.display.set_mode((576,1024))
screen_dim = (288,512)
screen = pygame.display.set_mode(screen_dim)
clock = pygame.time.Clock()
#Game Variables
gravity = 0.1
bird_movment = 0
game_active = True
collistion_num = 0
score = 0
high_score = 0
#surfaces to draw
bg_surface = pygame.image.load('assets/background-day.png').convert()  #convert the file to type that is good for pygem rendering
# bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0
floor_size = floor_surface.get_size()
#load bird
# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center = (screen_dim[0]/6,screen_dim[1]/3))
#load list of birds for animations
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (screen_dim[0]/6,screen_dim[1]/3))

BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP,200);
#pipes
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE,1200) #create a timer every 1200ms to trigger our custom event SPWNPIPE
pipe_heights = [200,280,360]
# text with pygame, 1.creating font(style,size), 2.render the font(tet,colour) 3.usth the resulting text surface
game_font = pygame.font.Font('04B_19.TTF',40)

#game over screen
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (screen_dim[0]/2,screen_dim[1]/2))

#SOUNDS
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
#MAIN GAME LOOP
while True:
    for event in pygame.event.get(): #CHECK EVENTS
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movment = 0
                bird_movment -= 3
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                #clear pipe list, and set bird in starting point
                pipe_list.clear() 
                bird_rect.center = (screen_dim[0]/6,screen_dim[1]/3)
                bird_movment = 0
                collistion_num = 0
                score = 0
        if event.type == BIRDFLAP:
            bird_index = (bird_index +1)  % len(bird_frames) #.len()
    
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) # we returned a tupple so we do not append but extend, so we get a list 
        
    #draw background
    screen.blit(bg_surface,(0,0)) # place background image on surface, in the place 0,0,
    
    if game_active:
        #BIRD
        bird_movment+=gravity
        
        rotated_bird = rotate_bird(bird_frames[bird_index])
        bird_rect.centery+=bird_movment
        screen.blit(rotated_bird,bird_rect)
        # game_active = check_collistion(pipe_list)
        if not check_collistion(pipe_list):
            collistion_num+=1
            if collistion_num >= 20:
                game_active = False
                hit_sound.play()
                if high_score <= score:
                    high_score = score
        #PIPES
        # screen.blit(pipe_surface,(100,100))
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        #increment score
        score+=0.01
        score_sound_countdown -=1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface,game_over_rect)
    #FLOOR
    floor_x_pos-=1 #move floor to the left
    draw_floor()
    if floor_x_pos <= - screen.get_size()[0]:
        floor_x_pos = 0
    
    score_display(game_active)
    
       

    pygame.display.update()
    clock.tick(80)

   
