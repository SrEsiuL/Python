import pygame, random
from settings import *

def escribir_textos(surface, text, size, x, y, color=NEGRO):
    font = pygame.font.Font("archivos/font/VCR_OSD_Mono.ttf", size=size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def spawn_enemigos(cantidad=10, enemigos_list=None, all_sprite_list=None):
    from enemigos import Enemigos
    
    for i in range(cantidad):
        enemigo = Enemigos()
        enemigo.rect.x = random.randrange(800, 1200)
        enemigo.rect.y = random.randrange(37, 410)
        
        if enemigos_list and all_sprite_list:
            enemigos_list.add(enemigo)
            all_sprite_list.add(enemigo)