import pygame, random
from settings import *

class Enemigos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.escala = random.randrange(25, 35)
        self.image = pygame.image.load("archivos/enemigo_v.png").convert()
        self.image = pygame.transform.scale(self.image, (self.escala, self.escala))
        self.rect = self.image.get_rect()

    def update(self):
        # Solo movimiento básico
        self.rect.x -= 1.5