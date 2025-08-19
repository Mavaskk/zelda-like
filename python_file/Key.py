from settings import *

class Key(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.type = "key"
		self.load = pygame.image.load('../zelda-like/assets/hud/key.png').convert_alpha()
		self.image = pygame.transform.scale(self.load,(20,20))
		self.icon = pygame.transform.scale(self.load,(32,32))
