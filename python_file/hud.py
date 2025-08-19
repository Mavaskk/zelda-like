from settings import *



class Hud(pygame.sprite.Sprite):
	def __init__(self, player,screen):
		super().__init__()
		self.player = player
		self.font = pygame.font.Font(None, 25)
		self.screen = screen
		self.heart_sprite = pygame.image.load('../zelda-like/assets/hud/heart.png').convert_alpha()
		self.shield_sprite = pygame.image.load('../zelda-like/assets/tileset/shield_powerup.png').convert_alpha()
		self.speed_potion = pygame.image.load('../zelda-like/assets/tileset/speed_potion.png').convert_alpha()
		self.speed_potion = pygame.transform.scale(self.speed_potion, (30, 30))
		self.heart_sprite = pygame.transform.scale(self.heart_sprite,(32,32))
		self.shield_sprite = pygame.transform.scale(self.shield_sprite,(32,32))
		self.rects1 = pygame.Rect(300, 20, 16, 16)   # Prima vita
		self.rects2 = pygame.Rect(340, 20, 16, 16)  # Seconda vita
		self.rects3 = pygame.Rect(380, 20, 16, 16)  # Terza vita		


	def draw(self,screen):
		coin_text = self.font.render(f"x{int(self.player.coin_count)}", True, ('white'))
		screen.blit(coin_text, (450, 20))
		if self.player.life >= 1:
			screen.blit(self.heart_sprite, self.rects1)
		if self.player.life >= 2:
			screen.blit(self.heart_sprite, self.rects2)
		if self.player.life >= 3:
			screen.blit(self.heart_sprite, self.rects3)



	


	def draw_item_text(self,item):
		if item == "shield":
			self.screen.blit(self.shield_sprite,pygame.Rect(260,20,32,32))
		if item == "speed":
			self.screen.blit(self.speed_potion,pygame.Rect(260,20,32,32))


	
