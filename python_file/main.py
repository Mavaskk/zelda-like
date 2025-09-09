from settings import *
from Level import *
from Menu import *

pygame.init()
pygame.joystick.init()



screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
start_screen = pygame.image.load("assets/start_screen1.jpeg")
start_screen = pygame.transform.scale(start_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
game_bol = True
level_bol = False

game_surface = pygame.Surface((WIDTH, HEIGHT))

class Game:
	def __init__(self):
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Zelda 1")
		self.level_params = ()
		self.paused = False
		self.level = Level(game_surface)
		self.pause_menu = Menu(game_surface)
	def run(self):
		global game_bol
		global level_bol

		while game_bol:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_bol = False
					pygame.quit()

				elif event.type == pygame.JOYBUTTONDOWN:
					button = event.button
					if button == 8:
						self.paused = not self.paused
					if button == 9:
						level_bol = True
						self.paused = False


			if self.paused and level_bol:
				action = self.pause_menu.selected_button()
				if action == "continue":
					self.paused = False
				if action =="restart":
					self.level = Level(game_surface)
					self.paused = False
				if action == "exit":
					pygame.quit()


				self.level.check_pause_status(self.paused)
				self.pause_menu.update()
				scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
				screen.blit(scaled_surface,(0,0))
				pygame.display.flip()

				

			if level_bol and not self.paused:
				self.level.check_pause_status(self.paused)
				self.level.run()
				scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
				screen.blit(scaled_surface,(0,0))
				pygame.display.flip()
				self.clock.tick(FPS)		

			if self.level.check_player_status():
				self.level = Level(game_surface)


game = Game()

if not level_bol:
	screen.blit(start_screen,screen.get_rect())
	pygame.display.flip()


if game_bol:
	game.run()
