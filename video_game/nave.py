import pygame, random
from settings import *
from player import Jugador, Corazones
from enemigos import Enemigos
from powerups import spawn_powerup
from misil import Misil
from utils import escribir_textos
from boss import Boss
from explosion import Explosion

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
        self.proyectiles_boss_list = pygame.sprite.Group()
        self.boss_list = pygame.sprite.Group()
        self.enemigos_list = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        self.misil_list = pygame.sprite.Group()
        self.cora_list = pygame.sprite.Group()
        self.powerup_list = pygame.sprite.Group()
        self.explosion_list = pygame.sprite.Group()
        
        # ✅ SISTEMA DEL BOSS
        self.boss_activo = False
        self.boss_aparecio = False
        self.puntuacion_para_boss = 100

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
            enemigo.rect.y = random.randrange(80, 410)
            self.enemigos_list.add(enemigo)
            self.all_sprite_list.add(enemigo)
    
    def spawn_enemigos_durante_juego(self, cantidad=1):
        """Función para spawnear enemigos durante el juego"""
        for i in range(cantidad):
            enemigo = Enemigos()
            enemigo.rect.x = random.randrange(800, 1200)
            enemigo.rect.y = random.randrange(80, 410)
            self.enemigos_list.add(enemigo)
            self.all_sprite_list.add(enemigo)

    def spawn_boss(self):
        """Función para hacer aparecer al boss"""
        if not self.boss_aparecio and self.jugador.score >= self.puntuacion_para_boss:
            boss = Boss()
            self.boss_list.add(boss)
            self.all_sprite_list.add(boss)
            self.boss_activo = True
            self.boss_aparecio = True
    
    def actualizar_vidas(self):
        for cora in self.cora_list:
            cora.kill()
        
        # Crear y agregar corazón
        corazon = Corazones()

        self.cora_list.add(corazon)
        self.all_sprite_list.add(corazon)
    
    def actualizar_boss(self):
        """Maneja toda la lógica del boss"""
        if len(self.boss_list) > 0:
            boss = list(self.boss_list)[0]  # Tomar el primer boss
            
            # ✅ DISPARO AUTOMÁTICO del boss
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - boss.tiempo_ultimo_disparo > boss.intervalo_disparo:
                boss.disparar(self.all_sprite_list, self.proyectiles_boss_list)
                boss.tiempo_ultimo_disparo = tiempo_actual
            
            # ✅ COLISIONES MISIL JUGADOR <> BOSS
            hits = pygame.sprite.spritecollide(boss, self.misil_list, True)
            for misil in hits:
                if boss.recibir_dano(misil.dano):

                    explosion = Explosion(boss.rect.centerx, boss.rect.centery, escala=3.0)  # 3 veces más grande
                    self.explosion_list.add(explosion)
                    self.all_sprite_list.add(explosion)

                    self.jugador.score += 100
                    boss.kill()
                    self.explosion_sound.play()
                    self.boss_activo = False
            
            # ✅ COLISIONES PROYECTILES BOSS <> JUGADOR
            hits = pygame.sprite.spritecollide(self.jugador, self.proyectiles_boss_list, True)
            for hit in hits:
                self.explosion_sound.play()
                self.jugador.vida -= hit.dano
                if self.jugador.vida <= 0:
                    self.correr = False

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

        # ✅ SPAWN DEL BOSS
        self.spawn_boss()
        
        # ✅ ACTUALIZAR BOSS si está activo
        if self.boss_activo:
            self.actualizar_boss()

        # ✅ Actualizar powerups específicamente (movimiento)
        for powerup in self.powerup_list:
            powerup.update()
        
        # Verificar enemigos que salen de pantalla
        for enemigo in self.enemigos_list:
            if enemigo.rect.x < -50:                
                enemigo.rect.x = random.randrange(800, 1200)
                enemigo.rect.y = random.randrange(80, 410)            
                
        # Colisiones jugador <> powerups
        hits = pygame.sprite.spritecollide(self.jugador, self.powerup_list, True)
        if hits:
            self.coran_sound.play()
            self.jugador.vida += 1
        
        # Colisiones misil <> enemigos
        hits = pygame.sprite.groupcollide(self.enemigos_list, self.misil_list, False, True)

        for enemigo, misiles in hits.items():
            for misil in misiles:
                murio = enemigo.recibir_dano(misil.dano)
                if murio:

                    explosion = Explosion(enemigo.rect.centerx, enemigo.rect.centery, escala=1.0)
                    self.explosion_list.add(explosion)
                    self.all_sprite_list.add(explosion)

                    self.jugador.score += 5
                    self.explosion_sound.play()
                    spawn_powerup(1, self.powerup_list, self.all_sprite_list, enemigo.rect.x, enemigo.rect.y)
                    enemigo.kill()
                    self.spawn_enemigos_durante_juego(1)
            
        # Colisiones jugador <> enemigos
        hits = pygame.sprite.spritecollide(self.jugador, self.enemigos_list, True)
        if hits:
            for enemigo in hits:
                # Crear explosión en la posición del ENEMIGO, no del jugador
                explosion = Explosion(enemigo.rect.centerx, enemigo.rect.centery, escala=1.2)
                self.explosion_list.add(explosion)
                self.all_sprite_list.add(explosion)
                
                # Respawnear nuevo enemigo por cada uno que chocó
                self.spawn_enemigos_durante_juego(1)

            self.explosion_sound.play()
            self.jugador.vida -= 1
            self.spawn_enemigos_durante_juego(1)
            if self.jugador.vida <= 0:
                self.correr = False

        # ✅ COLISIONES JUGADOR <> BOSS (si decides implementarlo)
        hits = pygame.sprite.spritecollide(self.jugador, self.boss_list, False)
        if hits:
            boss = hits[0]
            # Explosión en el BOSS, no en el jugador
            explosion = Explosion(self.jugador.rect.centerx, self.jugador.rect.centery)
            self.explosion_list.add(explosion)
            self.all_sprite_list.add(explosion)
            
            self.jugador.vida -= 2  # Más daño del boss
    
    def dibujar(self):
        self.ventana.fill(VERDE)

        # ✅ NUEVO: Dibujar barras de vida de enemigos
        for enemigo in self.enemigos_list:
            enemigo.dibujar_barra_vida(self.ventana)

        # ✅ BARRA DE VIDA DEL BOSS (si está activo)
        if self.boss_activo and len(self.boss_list) > 0:
            boss = list(self.boss_list)[0]
            self.dibujar_barra_vida_boss(boss)
        
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

    def dibujar_barra_vida_boss(self, boss):
        """Dibuja una barra de vida grande para el boss"""
        barra_largo = 200
        barra_alto = 20
        x = 300
        y = 10
        
        # Porcentaje de vida
        porcentaje_vida = boss.vida / boss.vida_maxima
        fill_largo = int(barra_largo * porcentaje_vida)
        
        # Fondo de la barra (negro)
        pygame.draw.rect(self.ventana, NEGRO, (x, y, barra_largo, barra_alto))
        # Vida actual (verde)
        pygame.draw.rect(self.ventana, VERDE, (x, y, fill_largo, barra_alto))
        # Borde
        pygame.draw.rect(self.ventana, BLANCO, (x, y, barra_largo, barra_alto), 2)
        
        # ✅ TEXTO CON escribir_textos - mucho más profesional
        escribir_textos(self.ventana, "", 20, x + barra_largo//2, y + barra_alto + 5)
        
        # ✅ Opcional: Porcentaje de vida dentro de la barra
        porcentaje_texto = f"{int(porcentaje_vida * 100)}%"
        escribir_textos(self.ventana, porcentaje_texto, 16, x + barra_largo//2, y + 2, BLANCO)
    
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