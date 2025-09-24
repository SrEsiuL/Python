import pygame, random
from settings import *

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        try:
            self.image = pygame.image.load("archivos/cora_v.PNG").convert()
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect()
            
            # Usar posición específica o aleatoria
            if x is not None and y is not None:
                self.rect.x = x
                self.rect.y = y
            else:
                self.rect.x = random.randrange(800, 1200)
                self.rect.y = random.randrange(37, 410)
        except Exception as e:
            # Fallback
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 1
        if self.rect.x < 0:
            self.kill()

def spawn_powerup(cantidad=1, powerup_list=None, all_sprite_list=None, x=None, y=None):
    if random.randint(1, 100) <= 1:
        for i in range(cantidad):
            powerup = Powerup(x, y)
            if powerup_list is not None and all_sprite_list is not None:
                powerup_list.add(powerup)
                all_sprite_list.add(powerup)