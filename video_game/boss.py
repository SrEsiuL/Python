import pygame
from settings import *

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # ✅ Imagen del boss
        self.image = pygame.image.load("archivos/boss_v.png").convert()

        
        self.image = pygame.transform.scale(self.image, (200, 150))  # Gigante
        self.rect = self.image.get_rect()
        self.rect.x = 900  # Aparece fuera de pantalla a la derecha
        self.rect.y = 150
        
        # ✅ STATS DEL BOSS
        self.vida_maxima = 100
        self.vida = self.vida_maxima
        self.velocidad_y = 3
        self.velocidad_entrada = 2  # Para la animación de entrada
        
        # ✅ SISTEMA DE DISPARO
        self.tiempo_ultimo_disparo = 0
        self.intervalo_disparo = 1500  # Dispara cada 1.5 segundos
        self.esta_activo = False  # Para la animación de entrada

    def update(self):
        # ✅ ANIMACIÓN DE ENTRADA
        if not self.esta_activo:
            self.rect.x -= self.velocidad_entrada
            if self.rect.x <= 600:  # Posición final
                self.rect.x = 600
                self.esta_activo = True
            return
        
        # ✅ MOVIMIENTO VERTICAL cuando está activo
        self.rect.y += self.velocidad_y
        if self.rect.y <= 40 or self.rect.y >= 300:
            self.velocidad_y *= -1  # Rebota en bordes

    def disparar(self, all_sprite_list, proyectiles_boss):
        if self.esta_activo:
            # ✅ Crear proyectil del boss
            proyectil = ProyectilBoss(self.rect.x, self.rect.centery)
            all_sprite_list.add(proyectil)
            proyectiles_boss.add(proyectil)
            return proyectil
        return None

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            return True  # Murió
        return False  # Sigue vivo

class ProyectilBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 8))
        self.image.fill((BLANCO))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = -7  # ✅ Va hacia la IZQUIERDA (más rápido)
        self.dano = 2  # ✅ Más daño que los misiles del jugador

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.x < -50:  # Eliminar si sale de pantalla
            self.kill()