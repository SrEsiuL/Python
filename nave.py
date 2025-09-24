import pygame, random
from settings import *
from player import Jugador, Corazones
from enemigos import Enemigos
from powerups import Powerup, spawn_powerup
from misil import Misil
from utils import escribir_textos, spawn_enemigos

#https://www.pygame.org/docs/ref/key.html (teclas pygame)
#https://soundbible.com/538-Blast.html (Sonidos)
#https://es.pixilart.com/draw (pixeles)

class Juego:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.ventana = pygame.display.set_mode((V_ANCHO, V_ALTURA))
        pygame.display.set_caption("Nave")
        self.tiempo = pygame.time.Clock()
        
        # Inicializar grupos PRIMERO
        self.enemigos_list = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        self.misil_list = pygame.sprite.Group()
        self.cora_list = pygame.sprite.Group()
        self.powerup_list = pygame.sprite.Group()
        
        # Jugador
        self.jugador = Jugador()
        self.all_sprite_list.add(self.jugador)
        
        # Sonidos
        try:
            self.disparo_sound = pygame.mixer.Sound("archivos/misil.mp3")
            self.explosion_sound = pygame.mixer.Sound("archivos/explo.wav")
            self.coran_sound = pygame.mixer.Sound("archivos/powerup.wav")
        except:
            # Silencioso en caso de error
            self.disparo_sound = self.explosion_sound = self.coran_sound = None
        
        # Inicializar enemigos - LLAMAR DIRECTAMENTE
        self.spawn_enemigos_inicial(10)
        
        self.correr = True
        self.score_final = "000000000"
    
    def spawn_enemigos_inicial(self, cantidad):
        for i in range(cantidad):
            enemigo = Enemigos()
            enemigo.rect.x = random.randrange(800, 1200)
            enemigo.rect.y = random.randrange(37, 410)
            self.enemigos_list.add(enemigo)
            self.all_sprite_list.add(enemigo)
    
    def spawn_enemigos_durante_juego(self, cantidad=1):
        """Función para spawnear enemigos durante el juego"""
        for i in range(cantidad):
            enemigo = Enemigos()
            enemigo.rect.x = random.randrange(800, 1200)
            enemigo.rect.y = random.randrange(37, 410)
            self.enemigos_list.add(enemigo)
            self.all_sprite_list.add(enemigo)
    
    def actualizar_vidas(self):
        for cora in self.cora_list:
            cora.kill()
        
        # Crear y agregar corazón
        corazon = Corazones()

        self.cora_list.add(corazon)
        self.all_sprite_list.add(corazon)
    
    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.correr = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.jugador.cambiar_velocidadY(3)
                if event.key == pygame.K_UP:
                    self.jugador.cambiar_velocidadY(-3)
                if event.key == pygame.K_RIGHT:
                    self.jugador.cambiar_velocidadX(3)
                if event.key == pygame.K_LEFT:
                    self.jugador.cambiar_velocidadX(-3)
                if event.key == pygame.K_SPACE:
                    misil = Misil(self.jugador.rect.centerx + 20, self.jugador.rect.centery - 2)
                    self.all_sprite_list.add(misil)
                    self.misil_list.add(misil)
                    self.disparo_sound.play()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.jugador.cambiar_velocidadY(-3)
                if event.key == pygame.K_UP:
                    self.jugador.cambiar_velocidadY(3)
                if event.key == pygame.K_RIGHT:
                    self.jugador.cambiar_velocidadX(-3)
                if event.key == pygame.K_LEFT:
                    self.jugador.cambiar_velocidadX(3)
    
    def actualizar(self):
        # Actualizar todos los sprites
        self.all_sprite_list.update()

         # ✅ Actualizar powerups específicamente (movimiento)
        for powerup in self.powerup_list:
            powerup.update()
        
        # Verificar enemigos que salen de pantalla
        for enemigo in self.enemigos_list.copy():
            if enemigo.rect.x < -50:
                self.explosion_sound.play()
                self.jugador.vida -= 1
                enemigo.kill()
                self.spawn_enemigos_durante_juego(1)
                

        hits = pygame.sprite.spritecollide(self.jugador, self.powerup_list, True)
        if hits:
            self.coran_sound.play()
            self.jugador.vida += 1
        
        # Colisiones misil <> enemigos
        hits = pygame.sprite.groupcollide(self.enemigos_list, self.misil_list, True, True)
        if hits:
            for hit in hits:
                # Guardar posición del enemigo
                posicion_x = hit.rect.x
                posicion_y = hit.rect.y
                
                self.jugador.score += 1
                self.explosion_sound.play()
                self.spawn_enemigos_durante_juego(1)
                
                # ✅ LLAMAR DIRECTAMENTE la función importada
                spawn_powerup(1, self.powerup_list, self.all_sprite_list, posicion_x, posicion_y)
        
        # Colisiones jugador <> enemigos
        hits = pygame.sprite.spritecollide(self.jugador, self.enemigos_list, True)
        if hits:
            self.explosion_sound.play()
            self.jugador.vida -= 1
            self.spawn_enemigos_durante_juego(1)
            if self.jugador.vida <= 0:
                self.correr = False
    
    def dibujar(self):
        self.ventana.fill(VERDE)
        
        # Actualizar y dibujar vidas
        self.actualizar_vidas()
        
        # Dibujar texto de vidas
        if len(self.cora_list) > 0:
            primer_corazon = list(self.cora_list)[0]
            escribir_textos(self.ventana, "x" + str(self.jugador.vida), 25, primer_corazon.rect.x + 36, 7)
        
        # Dibujar todos los sprites
        self.all_sprite_list.draw(self.ventana)
        pygame.draw.rect(self.ventana, NEGRO, (0, 35, 800, 410), 5)
        
        # Dibujar score
        score_text = str(self.jugador.score).zfill(9)
        escribir_textos(self.ventana, score_text, 25, V_ANCHO - 100, 10)
        
        pygame.display.flip()
    
    def ejecutar(self):
        while self.correr and self.jugador.vida > 0:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.tiempo.tick(FPS)
    
        pygame.quit()

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()