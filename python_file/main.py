from settings import *
from Level import *

pygame.init()
pygame.joystick.init()



screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_bol = True

game_surface = pygame.Surface((WIDTH, HEIGHT))
running = True

class Game:
	def __init__(self):
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Zelda 1")
		self.level_params = ()
		self.level = Level(game_surface)
	def run(self):
		global game_bol

		while game_bol:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_bol = False
					pygame.quit()
			self.level.run()
			scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
			screen.blit(scaled_surface,(0,0))
			pygame.display.flip()
			self.clock.tick(FPS)



game = Game()

while running:
	if game_bol:
		game.run()
