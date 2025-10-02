import pygame
import random

from agente import Agent
import colisoes as cls

def main():
    pygame.init()

    pygame.mixer.init()

    bounce_sound: object = pygame.mixer.Sound("bounce.wav")

    TITLE: str = "Bolinha pulando"
    pygame.display.set_caption(TITLE)

    WIDTH : float = 800
    HEIGHT : float = 800
    RESOLUTION : tuple = (WIDTH, HEIGHT)
    SCREEN : object = pygame.display.set_mode(RESOLUTION)
    CLOCK : object = pygame.time.Clock()
    
    dt: float = 0

    circle: object = Agent(WIDTH / 2, HEIGHT / 2, cor="green", altura=20, largura=20, delta_x=250, delta_y=200)

    obstacles: list = []
    for _ in range(30):
        ow = random.randint(60, 120)
        oh = random.randint(30, 80)
        ox = random.randint(0, WIDTH - ow)
        oy = random.randint(0, HEIGHT - oh)
        obstacles.append(pygame.Rect(ox, oy, ow, oh))

    running : bool = True
    while running:
        SCREEN.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        circle.position.x += circle.delta_x * dt
        circle.position.y += circle.delta_y * dt

        if circle.position.x >= WIDTH - circle.raio:
            circle.position.x = WIDTH - circle.raio
            circle.delta_x *= -1
            if bounce_sound: bounce_sound.play()
        elif circle.position.x <= circle.raio:
            circle.position.x = circle.raio
            circle.delta_x *= -1
            if bounce_sound: bounce_sound.play()

        if circle.position.y >= HEIGHT - circle.raio:
            circle.position.y = HEIGHT - circle.raio
            circle.delta_y *= -1
            if bounce_sound: bounce_sound.play()
        elif circle.position.y <= circle.raio:
            circle.position.y = circle.raio
            circle.delta_y *= -1
            if bounce_sound: bounce_sound.play()

        for obstacle in obstacles:
            rectangle = Agent(obstacle.x, obstacle.y, cor="red", largura=obstacle.width, altura=obstacle.height)

            colision, side, delta_x, delta_y = cls.circulo_retangulo(circle, rectangle)

            if not colision:
                pygame.draw.rect(SCREEN, "gray", obstacle)
                continue

            if side:
                circle.delta_x *= -1
                circle.position.x += (circle.raio - abs(delta_x)) * (1 if delta_x > 0 else -1)
            else:
                circle.delta_y *= -1
                circle.position.y += (circle.raio - abs(delta_y)) * (1 if delta_y > 0 else -1)

            if bounce_sound: bounce_sound.play()
            pygame.draw.rect(SCREEN, rectangle.cor, obstacle)
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            circle.position.x = WIDTH / 2
            circle.position.y = HEIGHT / 2

        pygame.draw.circle(SCREEN, circle.cor, (int(circle.position.x), int(circle.position.y)), int(circle.raio))

        dt = CLOCK.tick(60) / 1000
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()