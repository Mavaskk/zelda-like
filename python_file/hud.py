from settings import *



class Hud(pygame.sprite.Sprite):
	def __init__(self, player,screen, boss):
		super().__init__()
		self.player = player
		self.boss = boss
		self.font = pygame.font.Font(None, 25)
		self.screen = screen
		self.heart_sprite = pygame.image.load('../zelda-like/assets/hud/heart.png').convert_alpha()
		self.shield_sprite = pygame.image.load('../zelda-like/assets/tileset/shield_powerup.png').convert_alpha()
		self.speed_potion = pygame.image.load('../zelda-like/assets/tileset/speed_potion.png').convert_alpha()
		self.coin_sprite = pygame.image.load('../zelda-like/assets/hud/coin.png').convert_alpha()
		self.life_0 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_0.png').convert_alpha()
		self.life_1 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_1.png').convert_alpha()
		self.life_2 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_2.png').convert_alpha()
		self.life_3 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_3.png').convert_alpha()
		self.life_4 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_4.png').convert_alpha()
		self.life_5 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_5.png').convert_alpha()
		self.life_6 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_6.png').convert_alpha()
		self.life_7 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_7.png').convert_alpha()
		self.life_8 = pygame.image.load('../zelda-like/assets/hud/boss_life/life_8.png').convert_alpha()
		self.speed_potion = pygame.transform.scale(self.speed_potion, (30, 30))
		self.heart_sprite = pygame.transform.scale(self.heart_sprite,(32,32))
		self.shield_sprite = pygame.transform.scale(self.shield_sprite,(32,32))
		self.coin_sprite = pygame.transform.scale(self.coin_sprite,(32,32))
		self.rects1 = pygame.Rect(300, 20, 16, 16)   # Prima vita
		self.rects2 = pygame.Rect(340, 20, 16, 16)  # Seconda vita
		self.rects3 = pygame.Rect(380, 20, 16, 16)  # Terza vita	
		self.boss_rect= pygame.Rect(80, 20, 16, 16)  # Terza vita	


	def draw(self,screen):
		coin_text = self.font.render(f"{int(self.player.coin_count)}", True, ('white'))
		screen.blit(coin_text, (455, 27))
		screen.blit(self.coin_sprite, (420, 20))

		if self.player.life >= 1:
			screen.blit(self.heart_sprite, self.rects1)
		if self.player.life >= 2:
			screen.blit(self.heart_sprite, self.rects2)
		if self.player.life >= 3:
			screen.blit(self.heart_sprite, self.rects3)



	def draw_boss_life(self,screen):
		boss_life_sprites = [
			pygame.transform.scale(img, (182, 32)) 
			for img in [
				self.life_0, self.life_1, self.life_2,
				self.life_3, self.life_4, self.life_5,
				self.life_6, self.life_7, self.life_8
			]
		]
		
		# ciclo fino al valore di vita attuale del boss
		for i in range(self.boss.life):
			if i < len(boss_life_sprites):  # evita index error se vita > sprite disponibili
				self.screen.blit(boss_life_sprites[i], self.boss_rect)





	


	def draw_item_text(self,item):
		if item == "shield":
			self.screen.blit(self.shield_sprite,pygame.Rect(260,20,32,32))
		if item == "speed":
			self.screen.blit(self.speed_potion,pygame.Rect(260,20,32,32))


	
