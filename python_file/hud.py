from settings import *



class Hud(pygame.sprite.Sprite):
	def __init__(self, player):
		super().__init__()
		self.player = player
		self.font = pygame.font.Font(None, 25)
		self.item_box_asset = pygame.image.load('../zelda-like/assets/hud/item_box_hud.png').convert_alpha()
		self.item_box_asset = pygame.transform.scale(self.item_box_asset, (30, 30))
		self.item_one_rect = pygame.Rect(10,10,30,30)

	def draw(self,screen):
		coin_text = self.font.render(f"x{int(self.player.coin_count)}", True, ('white'))
		screen.blit(coin_text, (450, 20))

	def invetory(self, screen):
		screen.blit(self.item_box_asset,self.item_one_rect)
