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
         # ✅ NUEVO: Estado de teclas para evitar bloqueos
        self.teclas_presionadas = {
            pygame.K_UP: False,
            pygame.K_DOWN: False, 
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }

    def actualizar_velocidad(self):
        """DEBUG: Verificar esta función"""
        print(f"🔍 actualizar_velocidad llamado - teclas: {self.teclas_presionadas}")
        
        self.speed_x = 0
        self.speed_y = 0
        
        # Vertical
        if self.teclas_presionadas[pygame.K_UP] and not self.teclas_presionadas[pygame.K_DOWN]:
            self.speed_y = -5
            print("🔍 Movimiento ARRIBA")
        elif self.teclas_presionadas[pygame.K_DOWN] and not self.teclas_presionadas[pygame.K_UP]:
            self.speed_y = 5
            print("🔍 Movimiento ABAJO")
        
        # Horizontal  
        if self.teclas_presionadas[pygame.K_LEFT] and not self.teclas_presionadas[pygame.K_RIGHT]:
            self.speed_x = -5
            print("🔍 Movimiento IZQUIERDA")
        elif self.teclas_presionadas[pygame.K_RIGHT] and not self.teclas_presionadas[pygame.K_LEFT]:
            self.speed_x = 5
            print("🔍 Movimiento DERECHA")
            
        print(f"🔍 Velocidad calculada: ({self.speed_x}, {self.speed_y})")

    def update(self):
        
        # ✅ Los límites están bien
        if self.rect.y < 40:
            self.rect.y = 40
            self.speed_y = 0
        if self.rect.y > 400:
            self.rect.y = 400
            self.speed_y = 0
            
        if self.rect.x < 7:
            self.rect.x = 7
            self.speed_x = 0
        if self.rect.x > 750:
            self.rect.x = 750
            self.speed_x = 0
            
        # ✅ Movimiento directo (las velocidades vienen de manejar_eventos)
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