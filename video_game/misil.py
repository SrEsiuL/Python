import pygame
from settings import *

class Misil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("archivos/misil.PNG").convert()
        self.image = pygame.transform.scale(self.image, (15, 5))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = 5
        self.dano = 1
        
    def update(self):
        self.rect.x += self.speedy
        if self.rect.x > 755:
            self.kill()