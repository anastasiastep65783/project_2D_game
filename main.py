import pygame

pygame.init()
win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Мой платформер")

run = True
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()