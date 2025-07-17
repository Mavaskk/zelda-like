from settings import *



class Hud(pygame.sprite.Sprite):
	def __init__(self, player):
		super().__init__()
		self.player = player
		self.font = pygame.font.Font(None, 25)

	def draw(self,screen):
		coin_text = self.font.render(f"x{int(self.player.coin_count)}", True, ('white'))
		screen.blit(coin_text, (450, 20))
