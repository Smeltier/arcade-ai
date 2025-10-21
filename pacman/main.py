import pygame

from environment import Environment

pygame.init()

WIDTH, HEIGHT = 900, 950
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

environment = Environment(screen, 'pacman/maze.txt')

running = True
while running:
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    environment.draw_maze()

    pygame.display.flip()  

pygame.quit()