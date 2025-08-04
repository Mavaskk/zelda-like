from settings import *
import math

class Monster(pygame.sprite.Sprite):
	def __init__(self, pos, groups, player,):
		super().__init__(groups)		

		self.walk_front = [pygame.image.load(f'../zelda-like/assets/monster_slime/idle/idle_{i}.png').convert_alpha() for i in range(1, 6)]
		self.image = self.walk_front[0]
		self.rect = self.image.get_rect(topleft = pos)   
		self.speed = 2
		self.life = 2
		self.animation_speed = 0.18
		self.current_frame = 0
		self.activate_rect = pygame.Rect(0,0 , 150,150)
		self.activate_rect.center = self.rect.center # per centrare l'area del mostro sul rect del mostro
		self.player = player
		self.activate = False
		self.last_time_hit = pygame.time.get_ticks() 
		self.shield = False

	def activate_monster(self):
			collide = pygame.Rect.colliderect(self.activate_rect, self.player.rect)
			if collide:
				self.activate = True
	
	def check_player_shield(self,shield_status):
		if shield_status == True:
			self.shield = True
		else:
			self.shield = False
			

	def death(self):
		if self.life == 0:
			self.kill()


	def movement(self):
		self.rect.y -= self.speed

	def standing_animation(self):
		self.current_frame += self.animation_speed
		if int(self.current_frame) < len(self.walk_front):
			self.image = self.walk_front[int(self.current_frame)]
		else:
			self.current_frame = 0
			self.image = self.walk_front[0]



	def move_towards_player(self):
		if self.activate:
			player_x, player_y = self.player.rect.center 
			monster_x, monster_y = self.rect.center

			# Calcolare la direzione verso il player
			dx = player_x - monster_x
			dy = player_y - monster_y
			distance = math.hypot(dx, dy)  # Distanza tra mostro e player con teorema pitagora

			if distance > 0:  # Evitare divisioni per zero
				dx /= distance
				dy /= distance

			# Muoviamo il mostro verso il player
			self.rect.x += dx * self.speed
			self.rect.y += dy * self.speed

	def hit_player(self):
		current_time = pygame.time.get_ticks()

		if self.rect.colliderect(self.player.rect): #mettere un cooldown per ogni hit
			if self.shield == False :
				if current_time - self.last_time_hit >= 500:
					self.player.life -=1
					self.last_time_hit = current_time
			else:
				print("mostro non puo colpire")
		else:
			self.last_time_hit = current_time
				

	def update(self):
		self.activate_monster()
		self.hit_player()
		self.move_towards_player()
		self.death()
		self.standing_animation()
