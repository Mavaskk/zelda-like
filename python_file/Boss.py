from settings import *

class Boss(pygame.sprite.Sprite):
	def __init__(self,player):
		super().__init__()		
		
		#animazioni
		self.import_sprites()
		self.image = self.walk_front[0]
		self.animation_speed = 0.25
		self.current_frame = 0
		
		# Posizione iniziale
		self.rect = self.image.get_rect(topleft=(200, 100))
		
		#attributi
		self.speed = 1
		self.life = 2
		self.direction = "right"
		self.hit = False
		self.moving = False
		self.walking_sprite_map = {
			"right" : self.walk_right,
			"left" : self.walk_right,
			"back" : self.walk_back,
			"front" : self.walk_front
		}
		self.last_position_x = self.rect.x
		self.last_position_y = self.rect.y

		#player
		self.player = player
		

	def animation_walk(self):

		
		self.current_frame = self.current_frame + self.animation_speed if not self.hit else 0
		if self.current_frame >= len(self.walking_sprite_map[self.direction]):
			self.current_frame = 0

		# Seleziona sprite e applica flip se necessario
		self.image = self.walking_sprite_map[self.direction][int(self.current_frame)]
		if self.direction == "left":
			self.image = pygame.transform.flip(self.image, True, False)

	def detect_direction(self):
		#idea quella di prendere ogni volta l'ultima posizione e confrontare x e y, in base a se sono o maggiori o minori vuol dire che il boss sale, scende o dx o sx e da li capisco la posizione
		if self.moving:
			if self.rect.x > self.last_position_x:
				self.direction = "right"
			elif self.rect.x < self.last_position_x:
				self.direction = "left"
			
			elif self.rect.y > self.last_position_y:
				self.direction = "front"
			else:
				self.direction = "back"

			# print(self.direction, self.rect.x, self.last_position_x)
			# print(self.direction, self.last_position_y, self.rect.y)

			self.last_position_x = self.rect.x
			self.last_position_y = self.rect.y

	def hit(self):
		#gestire con il colliderect e dopo un tot far partire il colpo
		


	def import_sprites(self):
		self.walk_right = self.load_and_scale_images('../zelda-like/assets/boss/walking/right/walk_right_{i}.png',6,(88, 88))
		self.walk_back = self.load_and_scale_images('../zelda-like/assets/boss/walking/back/walk_back_{i}.png',6,(88, 88))
		self.walk_front = self.load_and_scale_images('../zelda-like/assets/boss/walking/front/walk_front_{i}.png',6,(88, 88))
		self.hit_right = self.load_and_scale_images('../zelda-like/assets/boss/hit/right/walk_right_{i}.png',12,(88, 88)) 
		self.hit_front = self.load_and_scale_images('../zelda-like/assets/boss/hit/front/walk_front_{i}.png',12,(88, 88)) 
		self.hit_back = self.load_and_scale_images('../zelda-like/assets/boss/hit/back/walk_back_{i}.png',12,(88, 88)) 

	def load_and_scale_images(self, path_pattern, count, size):
		#count numero immagini da caricare
		#size dimensione immagine

		return [
			pygame.transform.scale(
				pygame.image.load(path_pattern.format(i=i)).convert_alpha(),
				size
			)
			for i in range(1, count + 1)
		]

	def movement(self):
		self.rect.x += self.speed	
		self.moving = True

	def move_towards_player(self):
			player_x, player_y = self.player.rect.center 
			monster_x, monster_y = self.rect.center

			# Calcolare la direzione verso il player
			dx = player_x - monster_x
			dy = player_y - monster_y
			distance = math.hypot(dx, dy)  # Distanza tra mostro e player con teorema pitagora

			if distance > 0:  # Evitare divisioni per zero
				dx /= distance
				dy /= distance

			self.moving = True

			# Muoviamo il mostro verso il player
			self.rect.x += dx * self.speed
			self.rect.y += dy * self.speed	


	def update(self):
		# self.movement()
		self.move_towards_player()
		self.detect_direction()
		if not self.hit:
			self.animation_walk()



