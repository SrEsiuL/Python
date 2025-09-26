import pygame
from settings import *

def escribir_textos(surface, text, size, x, y, color=NEGRO):
    font = pygame.font.Font(FUENTE, size=size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)