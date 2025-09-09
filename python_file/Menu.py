from settings import *



class Menu(pygame.sprite.Sprite):
	def __init__(self,screen):
		super().__init__()
		self.screen = screen
		self.font = pygame.font.Font(None, 35)


		self.selected_index = 0
		self.button_pressed = False

		self.last_move_time = 0
		self.cooldown = 200
		self.background_image = pygame.image.load('assets/hud/menu_background.png').convert_alpha()
		self.box_sprite = pygame.image.load('assets/hud/menu_box.png').convert_alpha()

		self.create_menu_items()


	def create_menu_items(self):
		self.items = [
				MenuItem("continue", (165, 110), self.font, self.box_sprite),
				MenuItem("restart", (165, 190), self.font, self.box_sprite),
				MenuItem("exit", (165, 270), self.font, self.box_sprite)
			]

	def draw(self):
		for i, item in enumerate(self.items):
			if i == self.selected_index:
				item.text_surf = self.font.render(item.text, True, ('red'))
			else:
				item.text_surf = self.font.render(item.text, True, ('black'))
			item.draw(self.screen)


	def input(self):
		current_time = pygame.time.get_ticks()
		if joystick:
			axis_y = joystick.get_axis(1)
			if current_time - self.last_move_time > self.cooldown:  # Controllo cooldown
				if axis_y > 0.5:  # Spostamento giù
					self.selected_index += 1
					self.last_move_time = current_time  # Aggiorna il tempo dell'ultima mossa
				elif axis_y < -0.5:  # Spostamento su
					self.selected_index -= 1
					self.last_move_time = current_time  # Aggiorna il tempo dell'ultima mossa
				if self.selected_index >= len(self.items):
					self.selected_index = 0
				if self.selected_index < 0:
					self.selected_index = len(self.items) - 1

	def selected_button(self):
		if joystick:
			# Verifica se il pulsante è premuto ora
			button_is_pressed = joystick.get_button(2)

			# Rileva una pressione solo quando lo stato cambia da non premuto a premuto
			if button_is_pressed and not self.button_pressed:
				self.button_pressed = True
				if self.selected_index == 0:
					return "continue"
				elif self.selected_index == 1:
					return "restart"
				elif self.selected_index == 2:
					return "exit"
			# Aggiorna lo stato quando il pulsante viene rilasciato
			elif not button_is_pressed and self.button_pressed:
				self.button_pressed = False
		return None
	
	def set_background(self):
		self.background_rect = pygame.Rect(0, 0, 512, 448)
		self.background_image = pygame.transform.scale(self.background_image,(512, 448))
		self.screen.blit(self.background_image,self.background_rect)
	
	def update(self):
		# self.set_background()
		self.draw()
		self.input()
	

class MenuItem(pygame.sprite.Sprite):
	def __init__(self, text, pos, font, box_sprite):
		super().__init__()
		self.image = pygame.transform.scale(box_sprite, (180, 75))
		self.rect = self.image.get_rect(topleft=pos)
		self.text = text

		# Renderizza il testo centrato nel box
		self.text_surf = font.render(self.text, True, ('black'))
		self.text_rect = self.text_surf.get_rect(center=self.rect.center)

	# Metodo di disegno
	def draw(self, screen):
		screen.blit(self.image, self.rect.topleft)  # Disegna il box
		screen.blit(self.text_surf, self.text_rect)