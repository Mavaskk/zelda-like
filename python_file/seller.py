from settings import *
from SpeedPotion import *

class Seller(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups,screen):
		super().__init__(groups)
		self.image = surf
		self.item_list = []
		self.screen = screen
		self.rect = self.image.get_rect(topleft = pos)
		self.talking = False
		self.hitbox = pygame.Rect(self.rect.x - 40  , self.rect.y + 17, 150, 60)
		self.potion = pygame.image.load('../zelda-like/assets/market/potions/speed_potion.png').convert_alpha()
		self.cloud = pygame.image.load('../zelda-like/assets/market/cloud_text.png').convert_alpha()
		self.cloud_no_coin = pygame.image.load('../zelda-like/assets/market/cloud_no_coins.png').convert_alpha()
		self.cloud_buy_speed = pygame.image.load('../zelda-like/assets/market/buy_speed.png').convert_alpha()
		self.font = pygame.font.Font(None, 25)
		self.potion = pygame.transform.scale(self.potion,(125,125))
		self.cloud = pygame.transform.scale(self.cloud,(30,30))
		self.cloud_no_coin = pygame.transform.scale(self.cloud_no_coin,(100,100))
		self.cloud_buy_speed = pygame.transform.scale(self.cloud_buy_speed,(100,100))
		self.last_talk = 0
		self.last_buy = 0


	def trade(self):
		potion = SpeedPotion()
		return potion

	def draw_no_coin_text(self):
		self.screen.blit(self.cloud_no_coin,pygame.Rect(235,200,20,20))

	def draw_item_speed_potion(self):
		self.screen.blit(self.cloud_buy_speed,pygame.Rect(235,200,20,20))
		



	def display_market(self,screen):
		market_text = self.font.render(f"WELCOME TO THE MARKET!", True, ('white'))
		price_text = self.font.render(f"Price : 10 coins", True, ('white'))
		self.screen.blit(market_text, (20, 20))
		self.screen.blit(price_text, (180, 200))
		self.screen.blit(self.potion,pygame.Rect(180,70,125,125))
		self.screen.blit(self.cloud,pygame.Rect(245,240,20,20))
		# pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox, 2)

		