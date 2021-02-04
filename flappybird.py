import pygame
import random
import time
from pygame.locals import *

pygame.init()
screen_width = 288
screen_height = 512
window = pygame.display.set_mode((screen_width,screen_height))
fps = pygame.time.Clock()

# Declare variables
BACKGROUND = pygame.image.load("media/background.png").convert_alpha()
BASE = pygame.image.load("media/base.png").convert_alpha()
BOTTOM_PIPE = pygame.image.load("media/pipe.png").convert_alpha()
TOP_PIPE = pygame.transform.flip(BOTTOM_PIPE, False, True)
BIRD = pygame.image.load("media/flappybird-animation.png").convert_alpha()
DIE = pygame.mixer.Sound("media/die.wav")
HIT = pygame.mixer.Sound("media/hit.wav")
WING = pygame.mixer.Sound("media/wing.wav")
SWOOSH = pygame.mixer.Sound("media/swoosh.wav")
ARIAL = pygame.font.SysFont("Arial", 40)
pipe_height = 320
pipe_width = 52
pipe_gap = 100
pipe_speed = 10

finished = False
flap = False
pipe = [300, 100] # X location of both pipes, Y location of top of gap
bird = [50, 250]
bird_animation_count = 0
jump = 0
lives = 5

# Main game loop
while not finished:
    # Process keyboard and mouse events
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                finished = True
            if event.key == K_SPACE:
                flap = True
        if event.type == MOUSEBUTTONDOWN:
            flap = True

    # Game logic
    if flap:
        jump = 20
        flap = False
        WING.play()
    bird[1] -= jump
    if jump > -20:
        jump -= 2
    pipe[0] -= pipe_speed
    if pipe[0] < -pipe_width:
        pipe[0] = screen_width
        pipe[1] = random.randint(50, screen_height-150)
        pipe_gap = random.randint(100,200)

    # Draw graphics
    window.fill((0,0,0))
    window.blit(BACKGROUND, (0,0)) # Background
    window.blit(BASE, (0,400)) # Base
    label = ARIAL.render(str(lives), 1, (255,255,255))
    window.blit(label, (5,5))
    # Pipes
    window.blit(TOP_PIPE, (pipe[0], pipe[1]-pipe_height))
    window.blit(BOTTOM_PIPE, (pipe[0], pipe[1]+pipe_gap))
    # Flappy bird
    window.blit(BIRD, bird, (0,bird_animation_count*24,34,24))
    bird_animation_count = (bird_animation_count + 1) % 3
    # Detect collisions
    top_pipe_rect = TOP_PIPE.get_rect(topleft=(pipe[0], pipe[1]-pipe_height))
    bottom_pipe_rect = BOTTOM_PIPE.get_rect(topleft=(pipe[0], pipe[1]+pipe_gap))
    bird_rect = Rect(bird[0], bird[1], 34, 24)
    if bird_rect.colliderect(bottom_pipe_rect) or bird_rect.colliderect(top_pipe_rect):
        # Collision
        lives -= 1
        bird = [50, 250]
        pipe[0] = screen_width + pipe_speed*25
        pipe[1] = random.randint(50, screen_height-150)
        pipe_gap = random.randint(150,250)        
        if lives == 0:
            finished = True
            DIE.play()
        else:
            HIT.play()
    # Update screen
    pygame.display.update()
    fps.tick(25)

# Loop over, game over
time.sleep(1)
pygame.quit()


