from settings import *

class Inventory(pygame.sprite.Sprite):
	def __init__(self, player,screen):
		super().__init__()
		self.player = player
		self.screen = screen
		self.item_inventory = pygame.image.load('../zelda-like/assets/hud/inventory.png').convert_alpha()
		self.apple = pygame.image.load('../zelda-like/assets/tileset/apple.png').convert_alpha()
		self.shield = pygame.image.load('../zelda-like/assets/tileset/shield_powerup.png').convert_alpha()
		self.apple = pygame.transform.scale(self.apple, (30, 30))
		self.shield = pygame.transform.scale(self.shield, (28, 28))
		self.item_inventory = pygame.transform.scale(self.item_inventory, (200, 200))
		self.item_inventory_rect = self.item_inventory.get_rect(center=(WIDTH // 2, HEIGHT // 2)) #per centrare inventario nello schermo
		self.inventory_grid = []

	def add_item_to_list(self,item):
		for i in range(len(self.inventory_grid)):
			if self.inventory_grid[i] == {}:
				self.inventory_grid[i] = item
			

	def draw(self):
		self.screen.blit(self.item_inventory, self.item_inventory_rect)

		start_x = 173
		start_y = 140
		slot_size = 45  # distanza tra gli slot

		for i, item in enumerate(self.inventory_grid): #enumare prende in modo più semplice sia indice che valore
			col = i % 4 #modulo,r restituisce il resto intero della divisione, massimo 3
			row = i // 4 #divisione intera 

			x = start_x + col * slot_size
			y = start_y + row * slot_size

			if item:
				icon_rect = pygame.Rect(x, y, 16, 16)  
				pygame.draw.rect(self.screen, "blue", (start_x, start_y, 32, 32))
				self.screen.blit(item.icon, icon_rect)

		print(self.inventory_grid)
		

	def select_item(self,direction):
		if direction == "right":
			"dssda"



	def populate_from_bag(self, bag):
		# self.clear()
		for item in bag:
			if item.type == "apple":
				item.icon = self.apple
			elif item.type == "shield":
				item.icon = self.shield


		self.inventory_grid = bag
			
			# self.inventory_grid.append(item)

			# self.add_item_to_list(item)

	def remove_item(self,):
		"sdk"
	

	