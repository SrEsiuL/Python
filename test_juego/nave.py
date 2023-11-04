import pygame, random

#https://www.pygame.org/docs/ref/key.html (teclas pygame)
#https://soundbible.com/538-Blast.html (Sonidos)
#https://es.pixilart.com/draw (pixeles)

def escribirtextos(surface, text, size, x, y):
	font = pygame.font.SysFont("VCR OSD Mono", size)
	text_surface = font.render(text, True, Negro)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def spawnpowerup(cantidad=1):
		if random.randrange(1, 100) == random.randrange(1, 100):
			for i in range(cantidad):
				coraextra = Powerup()
				coraextra.rect.x = random.randrange(800, 1200)
				coraextra.rect.y = random.randrange(37, 410)
				powerup_list.add(coraextra) 
				all_sprite_list.add(coraextra)

def spawnenemigos(cantidad = 10):
	for i in range(cantidad):
		enemigos = Enemigos()
		enemigos.rect.x = random.randrange(800, 1200)
		enemigos.rect.y = random.randrange(37, 410)
		enemigos_list.add(enemigos) 
		all_sprite_list.add(enemigos)

class Enemigos(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.escala = random.randrange(25, 35)
		self.image = pygame.image.load("archivos/enemigo_v.png").convert()
		self.image = pygame.transform.scale(self.image, (self.escala, self.escala))
		#imagen.set_colorkey(Negro) quitar fondo negro
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x -= 2
		if self.rect.x < 0:
			explosion.play()
			jugador.vida -= 1
			self.kill()
			
			

class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("archivos/nave_v.PNG").convert()
		self.image = pygame.transform.scale(self.image, (40, 40))
		#imagen.set_colorkey(Negro) quitar fondo negro
		self.rect = self.image.get_rect()
		self.rect.centery = 225
		self.speed_x = 0
		self.speed_y = 0
		self.vida = 3
		self.score = 0

	def cambiovelocidadY(self, y):
		self.speed_y += y
		
	def cambiovelocidadX(self, x):
		self.speed_x += x

	def update(self):
		#limiteY
		if self.rect.y < 40:
			self.rect.y = 40
		if self.rect.y > 400:
			self.rect.y = 400
		#limiteX
		if self.rect.x < 7:
			self.rect.x = 7
		if self.rect.x > 750:
			self.rect.x = 750
		#movimiento
		self.rect.y += self.speed_y
		self.rect.x += self.speed_x
	
	def disparar(self):
		misil = Misil(self.rect.centerx + 20, self.rect.centery - 2)
		all_sprite_list.add(misil)
		misil_list.add(misil)
		
	def vidas(self, a, b):
		if a:
			coras = Corazones()
			coras.rect.x = 5
			coras.rect.y = 10
			escribirtextos(ventana, "x" + str(b), 25, coras.rect.x + 36, 7)
			cora_list.add(coras)
			all_sprite_list.add(coras)
		else:		
			coras = Corazones()
			coras.rect.x = 5
			coras.rect.y = 10
			escribirtextos(ventana, "x" + str(b), 25, coras.rect.x + 36, 7)
			cora_list.add(coras)
			all_sprite_list.add(coras)
		
class Corazones(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("archivos/cora_v_extra.PNG").convert()
		self.image = pygame.transform.scale(self.image, (20, 20))
		self.rect = self.image.get_rect()
		

	def coraextra(self):
		spawnpowerup()

class Powerup(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("archivos/cora_v.PNG").convert()
		self.image = pygame.transform.scale(self.image, (20, 20))
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x -= 2
		if self.rect.x < 0:
			self.kill()

class Misil(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("archivos/misil.PNG").convert()
		self.image = pygame.transform.scale(self.image, (15, 5))
		#imagen.set_colorkey(Negro) quitar fondo negro
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = 5
		
		
	def update(self):
		self.rect.x += self.speedy
		if self.rect.x > 755:
			self.kill()

V_ancho = 800
V_altura = 450
Negro = (0, 0, 0)
Blanco = (255, 255, 255)
Verde = (98, 186, 72)
pygame.init()
ventana = pygame.display.set_mode((V_ancho, V_altura))
pygame.display.set_caption("Nave")

tiempo = pygame.time.Clock()

enemigos_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()
misil_list = pygame.sprite.Group()
cora_list = pygame.sprite.Group()
powerup_list = pygame.sprite.Group()

spawnenemigos()

disparo = pygame.mixer.Sound("archivos/misil.mp3")
explosion = pygame.mixer.Sound("archivos/explo.wav")
coran = pygame.mixer.Sound("archivos/powerup.wav")

jugador = Jugador()
corazon = Corazones()

score_final = "000000000"
entro = 1
counter = 0

all_sprite_list.add(jugador)
correr = True

while correr:
	
	

	if not jugador.vida:
			correr = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			correr = False
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				jugador.cambiovelocidadY(3)
			if event.key == pygame.K_UP:
				jugador.cambiovelocidadY(-3)
			if event.key == pygame.K_RIGHT:
				jugador.cambiovelocidadX(3)
			if event.key == pygame.K_LEFT:
				jugador.cambiovelocidadX(-3)
			if event.key == pygame.K_SPACE:
				jugador.disparar()
				disparo.play()
				
			
				
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				jugador.cambiovelocidadY(-3)
			if event.key == pygame.K_UP:
				jugador.cambiovelocidadY(3)
			if event.key == pygame.K_RIGHT:
				jugador.cambiovelocidadX(-3)
			if event.key == pygame.K_LEFT:
				jugador.cambiovelocidadX(3)
	
	all_sprite_list.update()	
	
	#colisiones misil <> enemigos
	hits = pygame.sprite.groupcollide(enemigos_list, misil_list, True, True)
	if hits:
		for hit in hits:
			jugador.score += 1
			corazon.coraextra()
			explosion.play()
			spawnenemigos(1)
		


	#colisiones coraextra <> jugador
	hits = pygame.sprite.spritecollide(jugador, powerup_list, True)
	if hits:
		coran.play()
		jugador.vida += 1
	
	#colisiones jugador <> enemigos
	hits = pygame.sprite.spritecollide(jugador, enemigos_list, True)
	if hits:
		explosion.play()
		jugador.vida -= 1
		jugador.vidas(hits, jugador.vida)
		spawnenemigos(1)
		if not jugador.vida:
			correr = False
		
	ventana.fill(Verde)
	jugador.vidas(hits, jugador.vida)
	all_sprite_list.draw(ventana)
	pygame.draw.rect(ventana, Negro, (0, 35, 800, 410), 5)
	
	
	dif = 9 - len(str(jugador.score))
	score_final = str(jugador.score)
	if dif:
		for i in range(dif):
			score_final = "0" + score_final

	escribirtextos(ventana, score_final, 25, V_ancho - 100, 10)
	
	pygame.display.flip()
	tiempo.tick(60)
	
pygame.quit()