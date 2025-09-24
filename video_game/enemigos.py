import pygame, random
from settings import *

class Enemigos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.escala = random.randrange(25, 35)
        self.image = pygame.image.load("archivos/enemigo_v.png").convert()
        self.image = pygame.transform.scale(self.image, (self.escala, self.escala))
        self.rect = self.image.get_rect()
        
        #Sistema de vida
        self.vida_maxima = 2 #random.randint(2, 4)  # Vida entre 2 y 4
        self.vida = self.vida_maxima

    def update(self):
        self.rect.x -= 2
    
    # ✅ NUEVO: Método para recibir daño
    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            return True  # Retorna True si murió
        return False  # Retorna False si sigue vivo
    
    def dibujar_barra_vida(self, superficie):
        """Dibuja una barra de vida sobre el enemigo"""
        if self.vida < self.vida_maxima:  # Solo mostrar si tiene daño
            barra_largo = 30
            barra_alto = 4
            fill = (self.vida / self.vida_maxima) * barra_largo
            
            # Fondo de la barra (rojo)
            fondo_rect = pygame.Rect(self.rect.x, self.rect.y - 10, barra_largo, barra_alto)
            pygame.draw.rect(superficie, VERDE, fondo_rect)
            
            # Vida actual (verde)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10, fill, barra_alto)
            pygame.draw.rect(superficie, NEGRO, fill_rect)