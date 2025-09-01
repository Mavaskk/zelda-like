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
		self.life = 9
		self.direction = "right"
		self.state = "walk"
		self.moving = False
		self.just_hit = False
		self.shield_status = False
		self.last_time_hit = 0
		self.walking_sprite_map = {
			"right" : self.walk_right,
			"left" : self.walk_right,
			"back" : self.walk_back,
			"front" : self.walk_front
		}
		self.hit_sprite_map = {
			"right" : self.hit_right,
			"left" : self.hit_right,
			"back" : self.hit_back,
			"front" : self.hit_front
		}

		self.hurt_sprite_map = {
			"right" : self.hurt_right,
			"left" : self.hurt_right,
			"back" : self.hurt_back,
			"front" : self.hurt_front
		}
		self.last_position_x = self.rect.x
		self.last_position_y = self.rect.y

		self.player = player
		
		#fireball
		self.fireball_last_time = 0
		self.fireball_bol = False
		self.fireball_rect = self.fireball_sprite.get_rect()
		self.fireball_direction = None


	def animation(self,map):
			if self.state == "hit":
				self.animation_speed = 0.15
			else :
				self.animation_speed = 0.25

			self.current_frame = self.current_frame + self.animation_speed 

			if self.current_frame >= len(map[self.direction]):
				self.current_frame = 0
				if self.state == "hit" or "hurt":
					self.state = "walk"
				

			# Seleziona sprite e applica flip se necessario
			self.image = map[self.direction][int(self.current_frame)]
			if self.direction == "left":
				self.image = pygame.transform.flip(self.image, True, False)

	def check_player_shield(self,shield_status):
		if shield_status:
			self.shield = True
		else:
			self.shield = False

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

			self.last_position_x = self.rect.x
			self.last_position_y = self.rect.y

	def hit_player(self):
		#gestire con il colliderect e dopo un tot far partire il colpo
		current_time = pygame.time.get_ticks()
		if self.rect.colliderect(self.player.rect):
			if current_time - self.last_time_hit >= 500:
				self.state = "hit"
				if not self.player.hit and not self.shield:
					self.player.life -=1

				self.last_time_hit = current_time
			
		

	def import_sprites(self):
		self.walk_right = self.load_and_scale_images('../zelda-like/assets/boss/walking/right/walk_right_{i}.png',6,(60, 60))
		self.walk_back = self.load_and_scale_images('../zelda-like/assets/boss/walking/back/walk_back_{i}.png',6,(60, 60))
		self.walk_front = self.load_and_scale_images('../zelda-like/assets/boss/walking/front/walk_front_{i}.png',6,(60, 60))
		self.hit_right = self.load_and_scale_images('../zelda-like/assets/boss/hit/right/walk_right_{i}.png',12,(60, 60)) 
		self.hit_front = self.load_and_scale_images('../zelda-like/assets/boss/hit/front/walk_front_{i}.png',12,(60, 60)) 
		self.hit_back = self.load_and_scale_images('../zelda-like/assets/boss/hit/back/walk_back_{i}.png',12,(60, 60)) 
		self.hurt_back = self.load_and_scale_images('../zelda-like/assets/boss/hurt/back/hurt_back_{i}.png',4,(60, 60)) 
		self.hurt_front = self.load_and_scale_images('../zelda-like/assets/boss/hurt/front/hurt_front_{i}.png',4,(60, 60)) 
		self.hurt_right = self.load_and_scale_images('../zelda-like/assets/boss/hurt/right/hurt_right_{i}.png',4,(60, 60)) 
		self.fireball_sprite = pygame.transform.scale(pygame.image.load(f'../zelda-like/assets/boss/fireball/fireball.png').convert_alpha(),(60,60))
		self.fireball_sound = pygame.mixer.Sound("assets/sound/enemy_sound/fireball.mp3")
		self.fireball_sound.set_volume(0.1)  
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

	def throw_fireball(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.fireball_last_time >= 5000:
			start_x = self.rect.x
			start_y = self.rect.y
			
			self.fireball_rect = self.fireball_sprite.get_rect(topleft=(start_x,start_y))
			self.fireball_direction = self.direction

			self.fireball_bol = True
			self.fireball_sound.play()
			print("lancio sfera")
			self.fireball_last_time = current_time
	
		if self.fireball_bol:
			if self.fireball_direction == "right":
				self.fireball_rect.x += 3
			elif self.fireball_direction == "left":
				self.fireball_rect.x -= 3
			elif self.fireball_direction == "front":
				self.fireball_rect.y += 3
			else:
				self.fireball_rect.y -= 3
			



	def update(self):
		self.move_towards_player()
		self.detect_direction()

		self.hit_player()

		if self.life <= 1:
			self.kill()
		
		if not self.player.hit:
			self.just_hit = False

		if self.state == "hit":
			self.animation(self.hit_sprite_map)
		elif self.state == "walk":
			self.animation(self.walking_sprite_map)


		self.throw_fireball()




