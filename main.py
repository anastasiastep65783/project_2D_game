import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

fon = pygame.image.load('fon.png')

class Player(pygame.sprite.Sprite):
    right = True

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('igrok.png')

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0



