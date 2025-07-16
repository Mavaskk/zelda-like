# Importazioni
from settings import *
from Inventory import Inventory



class Player(pygame.sprite.Sprite):
	def __init__(self,collision_sprites):
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.inventory = Inventory(self)

		self.import_sprites()
		self.image = self.walk_right[0]
		self.animation_speed = 0.2
		self.current_frame = 0

		

		# Posizione iniziale
		self.rect = self.image.get_rect(topleft=(200, 100))
		self.hitbox = pygame.Rect(self.rect.x + 5 , self.rect.y + 17, 5, 5)

		self.direction = "down" 
		self.collision_sprite = collision_sprites

		#bol
		self.hit = False
		self.damage_taken = False
		self.animation_on = False
		self.g_pressed = False

		# Attributi
		self.speed = 3
		self.last_hit = 0
		self.life = 3
		self.prev_life = self.life
		self.coin_count = 0
		self.bag = []

	

	def import_sprites(self):
		self.walk_right = [pygame.image.load(f'../zelda-like/assets/player/walking/right/walk_right_{i}.png').convert_alpha() for i in range(0, 5)]
		self.walk_back = [pygame.image.load(f'../zelda-like/assets/player/walking/back/walk_back_{i}.png').convert_alpha() for i in range(1, 6)]
		self.walk_front = [pygame.image.load(f'../zelda-like/assets/player/walking/front/walk_front_{i}.png').convert_alpha() for i in range(1, 6)]
		self.hit_sword_right = [pygame.image.load(f'../zelda-like/assets/player/hit/right/hit_right_{i}.png').convert_alpha() for i in range(1, 6)]
		self.hit_sword_front = [pygame.image.load(f'../zelda-like/assets/player/hit/front/hit_front_{i}.png').convert_alpha() for i in range(1, 6)]
		self.hit_sword_back = [pygame.image.load(f'../zelda-like/assets/player/hit/up/hit_up_{i}.png').convert_alpha() for i in range(1, 6)]
		self.hurt_back = [pygame.image.load(f'../zelda-like/assets/player/hurt/back/hurt_back_{i}.png').convert_alpha() for i in range(1, 5)]
		self.hurt_right = [pygame.image.load(f'../zelda-like/assets/player/hurt/right/hurt_right_{i}.png').convert_alpha() for i in range(1, 5)]
		self.hurt_front = [pygame.image.load(f'../zelda-like/assets/player/hurt/front/hurt_front_{i}.png').convert_alpha() for i in range(1, 5)]




	# def input(self):
	# 	if joystick:
	# 		# Movimento in 4 direzioni
	# 		axis_x = joystick.get_axis(0)
	# 		axis_y = joystick.get_axis(1)
	# 		moving = False
	# 		if axis_x > 0.1:  # Destra
	# 			self.rect.x += self.speed
	# 			self.direction = "right" 
	# 			self.collision("horizontal")
	# 			moving = True
	# 		elif axis_x < -0.1:  # Sinistra
	# 			self.rect.x -= self.speed
	# 			self.direction = "left" 
	# 			self.collision("horizontal")
	# 			moving = True
	# 		elif axis_y > 0.1:  # Giù
	# 			self.rect.y += self.speed
	# 			self.direction = "down" 
	# 			self.collision("vertical")
	# 			moving = True
	# 		elif axis_y < -0.1:  # Su
	# 			self.rect.y -= self.speed	
	# 			self.direction = "up" 
	# 			self.collision("vertical")
	# 			moving = True
	# 		if joystick.get_button(1) and not self.hit:
	# 			current_time = pygame.time.get_ticks()
	# 			if current_time -self.last_hit > 400:
	# 				self.hit = True
	# 				self.last_hit = current_time
	# 		if not self.hit:
	# 			self.animation_walk(moving)
	#def input(self):
		# keys = pygame.key.get_pressed()
		# moving = False

		# if keys[pygame.K_d]:  # Destra
		# 	self.rect.x += self.speed
		# 	self.direction = "right"
		# 	self.collision("horizontal")
		# 	moving = True
		# elif keys[pygame.K_a]:  # Sinistra
		# 	self.rect.x -= self.speed
		# 	self.direction = "left"
		# 	self.collision("horizontal")
		# 	moving = True
		# elif keys[pygame.K_s]:  # Giù
		# 	self.rect.y += self.speed
		# 	self.direction = "down"
		# 	self.collision("vertical")
		# 	moving = True
		# elif keys[pygame.K_w]:  # Su
		# 	self.rect.y -= self.speed
		# 	self.direction = "up"
		# 	self.collision("vertical")
		# 	moving = True

		# # Attacco con il tasto F
		# if keys[pygame.K_f] and not self.hit:
		# 	current_time = pygame.time.get_ticks()
		# 	if current_time - self.last_hit > 400:
		# 		self.hit = True
		# 		self.last_hit = current_time

		# #entra in shop con tasto G
		# if keys[pygame.K_g] and not self.hit:
		# 	self.g_pressed = True
			


		# if not self.hit:
		# 	self.animation_walk(moving,self.walk_right,self.walk_back,self.walk_front)



	def animation_walk(self,moving, right, up, down):
		sprite_map = {
			"right": right,
			"left": right,  # Flip dopo
			"up": up,
			"down": down
			}
		
		self.current_frame = self.current_frame + self.animation_speed if moving else 0
		if self.current_frame >= len(sprite_map[self.direction]):
			self.current_frame = 0

		# Seleziona sprite e applica flip se necessario
		self.image = sprite_map[self.direction][int(self.current_frame)]
		if self.direction == "left":
			self.image = pygame.transform.flip(self.image, True, False)


	def animation(self, animation_on, right, up, down):
		sprite_map = {
			"right": right,
			"left": right,  # Flip dopo
			"up": up,
			"down": down
			}
		
		if animation_on:
			self.current_frame = self.current_frame + self.animation_speed
			if self.current_frame >= len(sprite_map[self.direction]):
				self.hit = False
				self.current_frame = 0
				self.animation_on = False

			# Seleziona sprite e applica flip se necessario
			self.image = sprite_map[self.direction][int(self.current_frame)]
			if self.direction == "left":
				self.image = pygame.transform.flip(self.image, True, False)
		
	def update_hitbox(self):
		self.hitbox.topleft = (self.rect.x + 5 , self.rect.y + 17)
	
	def collision(self, axis):
			self.update_hitbox()  # Aggiorna hitbox prima di controllare
			for sprite in self.collision_sprite:
				if sprite.rect.colliderect(self.hitbox):
					if axis == "horizontal":
						if self.direction == "left" and self.hitbox.left <= sprite.rect.right:
							self.rect.left = sprite.rect.right - 5  # Offset hitbox
						elif self.direction == "right" and self.hitbox.right >= sprite.rect.left:
							self.rect.right = sprite.rect.left + 5  # Offset hitbox
					elif axis == "vertical":
						if self.direction == "down" and self.hitbox.bottom >= sprite.rect.top:
							self.rect.y = sprite.rect.top - 17  # Offset hitbox
						elif self.direction == "up" and self.hitbox.top <= sprite.rect.bottom:
							self.rect.y = sprite.rect.bottom - 17  # Offset hitbox
			self.update_hitbox()  # Aggiorna hitbox dopo la correzione

	def death(self):
		if self.life == 0:
			self.kill()
		# if self.life < self.prev_life:
				# self.damage_taken = True
		# 		self.animation_on = True 
		# 		self.animation(self.animation_on,self.hurt_right,self.hurt_back,self.hurt_front)
		# 		self.prev_life = self.life



	def update(self):
		# if not self.damage_taken:  
		# self.input()  # Blocca input se è morto

		self.death()

		if self.hit and not self.damage_taken: 
			self.animation_on = True 
			self.animation(self.animation_on,self.hit_sword_right, self.hit_sword_back, self.hit_sword_front)

			
