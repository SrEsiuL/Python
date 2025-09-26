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
        pygame.display.set_caption("Galaxy Defender")
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
        
        # ✅ ESTADOS DEL JUEGO
        self.estado = "menu"  # "menu", "jugando", "pausa", "game_over", "mision_superada"
        self.fondo_menu = None
        self.correr = True
        self.score_final = "000000000"
        self.jugador.score = 0

        self.enemigos_destruidos = 0
        self.bosses_derrotados = 0
    
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
        """Actualiza la lógica del boss - VERSIÓN CORREGIDA"""
        if len(self.boss_list) > 0:
            boss = list(self.boss_list)[0]
            
            # ✅ ACTUALIZAR BOSS
            boss.update()
            
            # ✅ DISPAROS DEL BOSS
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - boss.tiempo_ultimo_disparo > boss.intervalo_disparo:
                boss.disparar(self.all_sprite_list, self.proyectiles_boss_list)
                boss.tiempo_ultimo_disparo = tiempo_actual
            
            # ✅ COLISIONES MISIL JUGADOR <> BOSS
            hits = pygame.sprite.spritecollide(boss, self.misil_list, True)
            for misil in hits:
                if boss.recibir_dano(misil.dano):
                    self.derrotar_boss(boss)  # ← ESTA LÍNEA FALTABA
                    return

    def derrotar_boss(self, boss):
        """Función épica cuando el boss es derrotado"""
        self.jugador.score += 500
        self.bosses_derrotados += 1
        
        # ✅ DESTRUIR TODOS LOS ENEMIGOS CON EXPLOSIONES
        for enemigo in self.enemigos_list:
            explosion = Explosion(
                enemigo.rect.centerx + random.randint(-10, 10),
                enemigo.rect.centery + random.randint(-10, 10),
                escala=0.8
            )
            self.explosion_list.add(explosion)
            self.all_sprite_list.add(explosion)
            enemigo.kill()
        
        # ✅ EXPLOSIÓN GIGANTE DEL BOSS
        for i in range(8):
            explosion = Explosion(
                boss.rect.centerx + random.randint(-80, 80),
                boss.rect.centery + random.randint(-80, 80),
                escala=2.5 + random.random() * 1.5
            )
            self.explosion_list.add(explosion)
            self.all_sprite_list.add(explosion)
        
        # ✅ LIMPIAR PROYECTILES
        for proyectil in self.proyectiles_boss_list:
            proyectil.kill()
        
        # ✅ SONIDO DE VICTORIA (opcional)
        """ try:
            victoria_sound = pygame.mixer.Sound("archivos/victoria.wav")
            victoria_sound.play()
        except:
            print("💡 Agrega un sonido de victoria en 'archivos/victoria.wav'") """
        
        boss.kill()
        self.boss_activo = False
        self.estado = "mision_superada"

    def dibujar_mision_superada(self):
        """Pantalla de victoria épica"""
        # Fondo especial (puedes usar verde oscuro o cargar una imagen)
        self.ventana.fill((0, 50, 0))  # Verde muy oscuro
        
        # ✅ TÍTULO ÉPICO
        escribir_textos(self.ventana, "¡MISIÓN SUPERADA!", 72, V_ANCHO//2, V_ALTURA//7, (255, 255, 0))
        escribir_textos(self.ventana, "¡MISIÓN SUPERADA!", 70, V_ANCHO//2 + 1.5, V_ALTURA//7 + 1.5, (255, 150, 0))
        
        # ✅ ESTADÍSTICAS DE LA MISIÓN
        stats = [
            f"BOSSES DERROTADOS: {self.bosses_derrotados}",
            f"PUNTUACIÓN TOTAL: {self.jugador.score}",
            f"ENEMIGOS DESTRUIDOS: {self.enemigos_destruidos}",
            f"VIDAS RESTANTES: {self.jugador.vida}",
        ]

        for i, linea in enumerate(stats):
            tamaño, color = 28, (BLANCO)
            y_pos = V_ALTURA//3.3 + (i * 40)
            escribir_textos(self.ventana, linea, tamaño, V_ANCHO//2, y_pos, color)

        opciones = [
            "[N] - Continuar siguiente misión",
            "[M] - Volver al menú principal",
            "[Q] - Salir del juego"
        ]

        for i, linea in enumerate(opciones):
            tamaño, color = 28, (VERDE)
            y_pos = V_ALTURA//1.35 + (i * 40)
            escribir_textos(self.ventana, linea, tamaño, V_ANCHO//2, y_pos, color)
        
        
        # ✅ MENSAJE SECRETO PARA EL MODO HARDCORE FUTURO
        if self.bosses_derrotados >= 3:
            escribir_textos(self.ventana, "¿Preparado para el modo HARDCORE?", 22, 
                        V_ANCHO//2, V_ALTURA - 150, (255, 0, 0))

    def manejar_mision_superada(self):
        """Manejar pantalla de victoria"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.reiniciar_para_siguiente_nivel()
                    return "jugando"
                elif event.key == pygame.K_m:
                    self.reiniciar_juego()
                    return "menu"
                elif event.key == pygame.K_q:
                    return "salir"
        
        return "mision_superada"

    def reiniciar_para_siguiente_nivel(self):
        """Preparar el juego para la siguiente misión"""
        
        # ✅ MANTENER puntuación y estadísticas
        # ✅ LIMPIAR enemigos y boss actual
        self.enemigos_list.empty()
        self.boss_list.empty()
        self.proyectiles_boss_list.empty()
        
        # ✅ BOSS MÁS DIFÍCIL CADA VEZ
        self.puntuacion_para_boss = 100 + (self.bosses_derrotados * 50)  # 100, 150, 200...
        
        # ✅ MÁS ENEMIGOS CADA NIVEL
        cantidad_enemigos = 10 + (self.bosses_derrotados * 3)
        self.spawn_enemigos_inicial(cantidad_enemigos)
        
        # ✅ RECOMPENSA: Vida extra cada 2 bosses
        if self.bosses_derrotados % 2 == 0 and self.bosses_derrotados > 0:
            self.jugador.vida += 1
        
        self.boss_aparecio = False
        self.boss_activo = False

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.correr = False
            
            if event.type == pygame.KEYDOWN:                
                # ✅ MOVIMIENTO (CORRECTO)
                if event.key == pygame.K_UP:
                    self.jugador.speed_y = -5
                elif event.key == pygame.K_DOWN:
                    self.jugador.speed_y = 5
                elif event.key == pygame.K_LEFT:
                    self.jugador.speed_x = -5
                elif event.key == pygame.K_RIGHT:
                    self.jugador.speed_x = 5
                elif event.key == pygame.K_SPACE and self.estado == "jugando":
                    misil = Misil(self.jugador.rect.centerx + 20, self.jugador.rect.centery - 2)
                    self.all_sprite_list.add(misil)
                    self.misil_list.add(misil)
                    if self.disparo_sound:
                        self.disparo_sound.play()
                elif event.key == pygame.K_ESCAPE:
                    if self.estado == "jugando":
                        self.estado = "pausa"
                    elif self.estado == "pausa":
                        self.estado = "jugando"
            
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    self.jugador.speed_y = 0
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.jugador.speed_x = 0

    def actualizar(self):
        # ✅ NO ACTUALIZAR NADA si está en pausa o menu
        if self.estado != "jugando":
            return
        
        # Actualizar todos los sprites
        self.all_sprite_list.update()

        # ✅ DETECTAR MUERTE DEL JUGADOR (usando el sistema de estados)
        if self.jugador.vida <= 0:
            self.jugador.vida = 0  # Asegurar que no sea negativo

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
            if self.coran_sound:
                self.coran_sound.play()
            self.jugador.vida += 1
        
        # Colisiones misil <> enemigos
        hits = pygame.sprite.groupcollide(self.enemigos_list, self.misil_list, False, True)

        for enemigo, misiles in hits.items():
            for misil in misiles:
                murio = enemigo.recibir_dano(misil.dano)
                if murio:
                    self.enemigos_destruidos += 1
                    explosion = Explosion(enemigo.rect.centerx, enemigo.rect.centery, escala=1.0)
                    self.explosion_list.add(explosion)
                    self.all_sprite_list.add(explosion)

                    self.jugador.score += 2
                    if self.explosion_sound:
                        self.explosion_sound.play()
                    spawn_powerup(1, self.powerup_list, self.all_sprite_list, enemigo.rect.x, enemigo.rect.y)
                    enemigo.kill()
                    self.spawn_enemigos_durante_juego(1)
            
        # Colisiones jugador <> enemigos
        hits = pygame.sprite.spritecollide(self.jugador, self.enemigos_list, True)
        if hits:
            for enemigo in hits:
                explosion = Explosion(enemigo.rect.centerx, enemigo.rect.centery, escala=1.2)
                self.explosion_list.add(explosion)
                self.all_sprite_list.add(explosion)
                
                murio = enemigo.recibir_dano(1)
                if murio:
                    self.enemigos_destruidos += 1
                    self.jugador.score += 2
                    # Respawnear nuevo enemigo por cada uno que chocó
                    self.spawn_enemigos_durante_juego(1)

            if self.explosion_sound:
                self.explosion_sound.play()
            self.jugador.vida -= 1
            self.spawn_enemigos_durante_juego(1)

        # ✅ COLISIONES JUGADOR <> BOSS
        hits = pygame.sprite.spritecollide(self.jugador, self.boss_list, False)
        if hits:
            boss = hits[0]
            # Explosión en el BOSS, no en el jugador
            explosion = Explosion(self.jugador.rect.centerx, self.jugador.rect.centery)
            self.explosion_list.add(explosion)
            self.all_sprite_list.add(explosion)
            
            self.jugador.vida -= 2  # Más daño del boss

        # Colisiones proyectiles_boss <> jugador
        hits = pygame.sprite.spritecollide(self.jugador, self.proyectiles_boss_list, True)
        if hits:
            for proyectil in hits:
                explosion = Explosion(proyectil.rect.centerx, proyectil.rect.centery)
                self.explosion_list.add(explosion)
                self.all_sprite_list.add(explosion)
                
                self.jugador.vida -= proyectil.dano  # Usar el daño del proyectil
                
                if self.jugador.vida <= 0:
                    self.jugador.vida = 0
    
    def dibujar(self):
        self.ventana.fill(VERDE)

        # ✅ DIBUJAR SEGÚN EL ESTADO ACTUAL
        if self.estado == "jugando" or self.estado == "pausa":
            # ✅ DIBUJAR JUEGO NORMAL (también para pausa, pero congelado)
            
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
            
            # Dibujar score
            score_text = str(self.jugador.score).zfill(9)
            escribir_textos(self.ventana, score_text, 25, V_ANCHO - 100, 10)

            # ❌ ELIMINADO: if self.pausado: (ahora se maneja en ejecutar())
            pygame.draw.rect(self.ventana, NEGRO, (0, 35, 800, 410), 5)
            
        elif self.estado == "game_over":
            # ✅ DIBUJAR GAME OVER (sobre el juego congelado)
            self.all_sprite_list.draw(self.ventana)  # Mostrar escena final
            pygame.draw.rect(self.ventana, NEGRO, (0, 35, 800, 410), 5)
            # ❌ ELIMINADO: self.dibujar_game_over() (ahora se maneja en ejecutar())

    def dibujar_menu(self):
        """Dibuja el menú principal"""
        # ✅ FONDO (imagen o color sólido)
        if self.fondo_menu:
            self.ventana.blit(self.fondo_menu, (0, 0))
        else:
            self.ventana.fill((VERDE))

        # ✅ TÍTULO PRINCIPAL CON EFECTO
        escribir_textos(self.ventana, "GALAXY DEFENDER", 74, V_ANCHO//2, V_ALTURA//5, (BLANCO))
        escribir_textos(self.ventana, "GALAXY DEFENDER", 72, V_ANCHO//2 + 2, V_ALTURA//5 + 2, (NEGRO))  # Sombra
        
        # ✅ INSTRUCCIONES
        instrucciones = [
            "CONTROLES:",
            "[Flechas] - Movimiento",
            "[ESPACIO] - Disparar",
            "[ESC] - Pausa",
            "",
            "Presiona [ENTER] para iniciar",
            "Presiona [Q] para salir"
        ]
        
        for i, linea in enumerate(instrucciones):
            if "CONTROLES" in linea:
                tamaño, color = 32, (NEGRO)
            elif "Presiona" in linea:
                tamaño, color = 28, (NEGRO)
            else:
                tamaño, color = 24, BLANCO
            
            y_pos = V_ALTURA//2.5 + (i * 35)
            escribir_textos(self.ventana, linea, tamaño, V_ANCHO//2, y_pos, color)
        
        # ✅ SCORE MÁXIMO (si quieres guardar records)
        escribir_textos(self.ventana, f"Score máximo: {self.score_final}", 20, V_ANCHO//2, V_ALTURA - 130, (GRIS))

    def manejar_menu(self):
        """Maneja las opciones del menú principal - CON DEBUG"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER
                    return "jugando"
                elif event.key == pygame.K_q:
                    return "salir"

        return "menu"

    def dibujar_pausa(self):
        """Dibuja menú de pausa - ASEGURAR FONDO VISIBLE"""
        # ✅ FONDO SEMI-TRANSPARENTE (debe ser después de dibujar el juego)
        superficie_pausa = pygame.Surface((V_ANCHO, V_ALTURA), pygame.SRCALPHA)
        superficie_pausa.fill((0, 0, 0, 128))  # Negro semi-transparente
        self.ventana.blit(superficie_pausa, (0, 0))
        
        # ✅ TEXTO DE PAUSA (que contraste con el fondo)
        escribir_textos(self.ventana, "JUEGO EN PAUSA", 64, V_ANCHO//2, V_ALTURA//3, BLANCO)
        escribir_textos(self.ventana, f"Score: {self.jugador.score:09d}", 36, V_ANCHO//2, V_ALTURA//2, BLANCO)
        escribir_textos(self.ventana, f"Vidas: {self.jugador.vida}", 36, V_ANCHO//2, V_ALTURA//2 + 40, BLANCO)
        escribir_textos(self.ventana, "Presiona [ESC] para reanudar", 28, V_ANCHO//2, V_ALTURA//2 + 100, (0, 255, 0))

    def manejar_pausa(self):
        """Maneja las opciones de pausa"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC para reanudar
                    return "jugando"
                elif event.key == pygame.K_q:
                    return "salir"
        
        return "pausa"  # Mantener en pausa

    def dibujar_game_over(self):
        """Versión minimalista en verde y blanco"""
        # ✅ FONDO VERDE OSCURO para contraste
        self.ventana.fill((VERDE))  # Verde más oscuro
        
        # ✅ TÍTULO SIMPLE
        escribir_textos(self.ventana, "GAME OVER", 80, V_ANCHO//2, V_ALTURA//4, BLANCO)
        escribir_textos(self.ventana, "GAME OVER", 80, V_ANCHO//2 + 2, V_ALTURA//4 + 2, (NEGRO))  # Sombra
        
        # ✅ INFORMACIÓN ORGANIZADA
        info = [
            f"SCORE: {self.jugador.score:09d}",
            f"ENEMIGOS DERROTADOS: {self.enemigos_destruidos}",
            f"BOSSES DERROTADOS: {self.bosses_derrotados}"
        ]
        
        for i, linea in enumerate(info):
            escribir_textos(self.ventana, linea, 24, V_ANCHO//2, 210 + (i * 35), (BLANCO))
        
        # ✅ OPCIONES MINIMALISTAS
        opciones = [
            "[R] Reiniciar",
            "[M] Menú", 
            "[Q] Salir"
        ]
        
        for i, linea in enumerate(opciones):
            y_pos = V_ALTURA//1.7 + 60 + (i * 40)
            escribir_textos(self.ventana, linea, 26, V_ANCHO//2, y_pos, (NEGRO))

    def manejar_game_over(self):
        """Maneja las opciones de game over"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    self.reiniciar_juego()
                    return "jugando"
                elif event.key == pygame.K_m:  # Menú principal
                    self.reiniciar_juego()
                    return "menu"
                elif event.key == pygame.K_q:
                    return "salir"
        
        return "game_over"

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
    
    def reiniciar_juego(self):
        """Reinicia el juego COMPLETAMENTE - VERSIÓN CORREGIDA"""
        print("🔄 Reiniciando juego...")
        
        # ✅ LIMPIAR TODOS LOS SPRITES (INCLUYENDO BOSS)
        self.all_sprite_list.empty()
        self.enemigos_list.empty()
        self.misil_list.empty()
        self.powerup_list.empty()
        self.cora_list.empty()
        self.explosion_list.empty()
        self.boss_list.empty()  # ✅ IMPORTANTE: Limpiar boss
        self.proyectiles_boss_list.empty()  # ✅ Y sus proyectiles
        
        # ✅ REINICIAR JUGADOR (posición y stats)
        self.jugador = Jugador()
        self.all_sprite_list.add(self.jugador)
        
        # ✅ REINICIAR VARIABLES DEL BOSS
        self.boss_activo = False
        self.boss_aparecio = False
        self.puntuacion_para_boss = 100  # ✅ Resetear puntuación para boss
        
        # ✅ REINICIAR ESTADÍSTICAS
        self.jugador.score = 0  # ✅ Puntos a cero
        self.enemigos_destruidos = 0  # ✅ Contador a cero
        self.bosses_derrotados = 0  # ✅ Bosses derrotados a cero
        
        # ✅ REINICIAR ENEMIGOS
        self.spawn_enemigos_inicial(10)
        
        # ✅ REINICIAR ESTADO
        self.estado = "jugando"

    def activar_game_over(self):
        """Activa el estado de game over"""
        self.game_over = True
        self.tiempo_muerte = pygame.time.get_ticks()
        
        # ✅ Opcional: Sonido de game over
        try:
            self.explosion_sound.play()  # O un sonido específico de game over
        except:
            pass

    def ejecutar(self):
        self.estado = "menu"
        
        while self.correr:            
            # ✅ CADA ESTADO MANEJA SUS PROPIOS EVENTOS
            if self.estado == "menu":
                self.dibujar_menu()
                self.estado = self.manejar_menu()  # ✅ Maneja eventos del menú
                    
            elif self.estado == "jugando":
                self.manejar_eventos()  # ✅ Maneja eventos de juego
                self.actualizar()
                self.dibujar()
                
                if self.jugador.vida <= 0:
                    self.estado = "game_over"
                    
            elif self.estado == "pausa":
                self.dibujar()  # Juego congelado
                self.dibujar_pausa()  # Overlay de pausa
                self.estado = self.manejar_pausa()  # ✅ Maneja eventos de pausa

            elif self.estado == "mision_superada":
                self.dibujar_mision_superada()
                self.estado = self.manejar_mision_superada()
                    
            elif self.estado == "game_over":
                self.dibujar_game_over()
                self.estado = self.manejar_game_over()  # ✅ Maneja eventos de game over
                    
            elif self.estado == "salir":
                self.correr = False
            
            pygame.display.flip()
            self.tiempo.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()