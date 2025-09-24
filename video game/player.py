import pygame
from settings import *

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("archivos/nave_v.PNG").convert()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centery = 225
        self.speed_x = 0
        self.speed_y = 0
        self.vida = 3
        self.score = 0

    def cambiar_velocidadY(self, y):
        self.speed_y += y
        
    def cambiar_velocidadX(self, x):
        self.speed_x += x

    def update(self):
        # Límites Y
        if self.rect.y < 40:
            self.rect.y = 40
        if self.rect.y > 400:
            self.rect.y = 400
        # Límites X
        if self.rect.x < 7:
            self.rect.x = 7
        if self.rect.x > 750:
            self.rect.x = 750
        # Movimiento
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
    
    def disparar(self, all_sprite_list, misil_list):
        from misil import Misil  # Importación local para evitar circular
        misil = Misil(self.rect.centerx + 20, self.rect.centery - 2)
        all_sprite_list.add(misil)
        misil_list.add(misil)
        return misil

class Corazones(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("archivos/cora_v_extra.PNG").convert()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 10