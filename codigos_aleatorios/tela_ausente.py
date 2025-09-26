import pygame
import random

def main():
    pygame.init()

    pygame.mixer.init()
    bouce_sound = pygame.mixer.Sound("bounce.wav")

    screen_title: str = "Simulação tela ausente TV"
    pygame.display.set_caption(screen_title)

    width: int = 800
    height: int = 800
    screen_resolution: tuple = (width, height)
    screen: object = pygame.display.set_mode(screen_resolution)
    clock = pygame.time.Clock()

    delta: float = 10

    size: int = 50
    x: float = width / 2 + 100
    y: float = height / 2 + 100
    dX: float = 250
    dY: float = 200 
    dt: float = 0
    square = pygame.Rect(x, y, size, size)

    obstacles: list = []
    for _ in range(20):
        ow = random.randint(60, 120)
        oh = random.randint(30, 80)
        ox = random.randint(0, width - ow)
        oy = random.randint(0, height - oh)
        obstacles.append(pygame.Rect(ox, oy, ow, oh))

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        x += dX * dt
        y += dY * dt
        square.topleft = (x, y)  

        # Colisão nas bordas da tela.
        if square.right >= width:
            square.right = width
            x = square.x
            dX *= -1
            bouce_sound.play()
        elif square.left <= 0:
            square.left = 0
            x = square.x
            dX *= -1
            bouce_sound.play()
        if square.bottom >= height:
            square.bottom = height
            y = square.y
            dY *= -1
            bouce_sound.play()
        elif square.top <= 0:
            square.top = 0
            y = square.y
            dY *= -1    
            bouce_sound.play()

        # Colisão entre obstáculo e o "jogador".
        for obs in obstacles:
            if square.colliderect(obs):
                if abs(square.right - obs.left) < delta:  
                    square.right = obs.left
                    x = square.x
                    dX *= -1
                    bouce_sound.play()
                elif abs(square.left - obs.right) < delta:  
                    square.left = obs.right
                    x = square.x
                    dX *= -1
                    bouce_sound.play()
                if abs(square.bottom - obs.top) < delta:  
                    square.bottom = obs.top
                    y = square.y
                    dY *= -1
                    bouce_sound.play()
                elif abs(square.top - obs.bottom) < delta: 
                    square.top = obs.bottom
                    y = square.y
                    dY *= -1
                    bouce_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            x = width / 2 + 100
            y = height / 2 + 100

        for obs in obstacles:
            pygame.draw.rect(screen, "gray", obs, border_radius = 6)

        pygame.draw.rect(screen, "green", square, border_radius = 8)

        dt = clock.tick(60) / 1000

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()