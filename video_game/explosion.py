import pygame
from settings import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, escala=1.5):
        super().__init__()
        
        # ✅ Cargar sprites de explosión (crea estas imágenes en Pixilart)
        self.sprites = []
        try:
            # Sprite sheet o imágenes individuales
            for i in range(1, 4):  # 5 frames de explosión
                sprite = pygame.image.load(f"archivos/explosion_{i}.png").convert()
                sprite.set_colorkey(NEGRO)  # Remover fondo negro
                sprite = pygame.transform.scale(sprite, (int(40 * escala), int(40 * escala)))
                self.sprites.append(sprite)
        except:
            # ✅ Placeholder si no tienes los sprites aún
            for i in range(4):
                sprite = pygame.Surface((int(40 * escala), int(40 * escala)))
                sprite.fill((255, 165, 0))  # Naranja como placeholder
                self.sprites.append(sprite)
        
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # ✅ Animación
        self.frame_actual = 0
        self.velocidad_animacion = 0.1  # Velocidad de la animación
        self.contador_frames = 0
        
    def update(self):
        # ✅ Avanzar la animación
        self.contador_frames += self.velocidad_animacion
        if self.contador_frames >= 1:
            self.frame_actual += 1
            self.contador_frames = 0
            
            if self.frame_actual < len(self.sprites):
                self.image = self.sprites[self.frame_actual]
            else:
                self.kill()  # ✅ Eliminar cuando termina la animación