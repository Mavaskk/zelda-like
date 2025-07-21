from settings import *
from player import *
from monster import *
from map_setup import *
from hud import *
from seller import *
from Item import *
from Inventory import Inventory



class Level():
	def __init__(self, game_surface):
		super().__init__()


		self.game_surface = game_surface


		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.monster_sprites = pygame.sprite.Group()
		self.market_sprites = pygame.sprite.Group()
		self.pickup_items_grups = pygame.sprite.Group()

		self.map_grid = [
			["overworld_room1", "overworld_room2","overworld_room3"],
			["overworld_room4", "overworld_room5","overworld_room6"],
			["overworld_room7", "overworld_room8","overworld_room9"]

		]

		self.map_files = {
			"overworld_room1": '../zelda-like/assets/tileset/file_tmx/overworld_room1.tmx',
			"overworld_room2": '../zelda-like/assets/tileset/file_tmx/overworld_room2.tmx',
			"overworld_room3": '../zelda-like/assets/tileset/file_tmx/overworld_room3.tmx',
			"overworld_room4": '../zelda-like/assets/tileset/file_tmx/overworld_room4.tmx',
			"overworld_room5": '../zelda-like/assets/tileset/file_tmx/overworld_room5.tmx',
			"overworld_room6": '../zelda-like/assets/tileset/file_tmx/overworld_room6.tmx',
			"overworld_room7": '../zelda-like/assets/tileset/file_tmx/overworld_room7.tmx',
			"overworld_room8": '../zelda-like/assets/tileset/file_tmx/overworld_room8.tmx',
			"overworld_room9": '../zelda-like/assets/tileset/file_tmx/overworld_room9.tmx',
		}

		self.current_row = 0
		self.current_col = 0

		#bol
		self.market_on = False
		self.inventory_key = False 
		self.g_pressed = False


		self.current_map_key = self.map_grid[self.current_row][self.current_col]
		self.tmx_map = pytmx.load_pygame(self.map_files[self.current_map_key])
		
		self.market_map_path =  "../zelda-like/assets/tileset/file_tmx/market_1.tmx"

		self.player = Player(self.collision_sprites) 
		self.hud = Hud(self.player,self.game_surface)
		self.inventory = Inventory(self.player,self.game_surface)
		self.game_state = "gameplay"
		self.setup()
		self.setup_market(self.market_map_path) #accedi direttamente al market
		self.all_sprites.add(self.player)

		

	def apply_item_to_player(self,item):

		if item is not None:
			if item.type == "apple":
				self.player.life += item.power
			if item.type == "shield":
				# self.activate_shield(item.power)
				self.player.shield = True
				self.player.last_shield = pygame.time.get_ticks()
		else:
			print("troppe vite") #fai apparire messaggio di errore


		

	def handle_input(self):

		keys = pygame.key.get_pressed()
		moving = False

		if keys[pygame.K_g]:
			if not self.g_pressed:
				if self.game_state == "gameplay":
					self.game_state = "inventory"
					self.inventory.populate_from_bag(self.player.bag)
				elif self.game_state == "inventory":
					self.game_state = "gameplay"
				print("Stato gioco:", self.game_state)
				self.g_pressed = True
		else:
			self.g_pressed = False

		if self.game_state == "gameplay" :
			if keys[pygame.K_d]:  # Destra
				self.player.rect.x += self.player.speed
				self.player.direction = "right"
				self.player.collision("horizontal")
				moving = True
			elif keys[pygame.K_a]:  # Sinistra
				self.player.rect.x -= self.player.speed
				self.player.direction = "left"
				self.player.collision("horizontal")
				moving = True
			elif keys[pygame.K_s]:  # Giù
				self.player.rect.y += self.player.speed
				self.player.direction = "down"
				self.player.collision("vertical")
				moving = True
			elif keys[pygame.K_w]:  # Su
				self.player.rect.y -= self.player.speed
				self.player.direction = "up"
				self.player.collision("vertical")
				moving = True
			elif keys[pygame.K_e]: #raccogli oggetto
				for item in self.pickup_items_grups:
					if self.player.rect.colliderect(item):
						if len(self.player.bag) <= 15:
							self.player.bag.append(item)
							item.kill()						
						else:
							print("inventario pieno")



			# Attacco con il tasto F
			if keys[pygame.K_f] and not self.player.hit:
				current_time = pygame.time.get_ticks()
				if current_time - self.player.last_hit > 400:
					self.player.hit = True
					self.player.last_hit = current_time


		if self.game_state == "inventory":
			current_time = pygame.time.get_ticks()
			cooldown = 200
			if current_time - self.inventory.move_time > cooldown:			
				if keys[pygame.K_d]:  # Destra
					self.inventory.handle_input("right")
					self.inventory.move_time = current_time
				if keys[pygame.K_a]:  # Destra
					self.inventory.handle_input("left")
					self.inventory.move_time = current_time
				if keys[pygame.K_e]:  # togli oggetto
					remove_cooldown = 200
					current_time_remove = pygame.time.get_ticks()
					if current_time_remove - self.inventory.last_remove_time > remove_cooldown:
						self.inventory.remove_item()
						self.inventory.last_remove_time = current_time_remove
				if keys[pygame.K_f]:  # togli oggetto
					use_cooldown = 200
					current_time_use = pygame.time.get_ticks()
					if current_time_use - self.inventory.last_use_time > use_cooldown:
						item = self.inventory.use_item()
						self.apply_item_to_player(item)
						self.inventory.last_use_time = current_time_use
				
		if not self.player.hit:
			self.player.animation_walk(moving,self.player.walk_right,self.player.walk_back,self.player.walk_front)


	def setup(self):
		#svuota i gruppi di sprites
		self.collision_sprites.empty()
		self.all_sprites.empty()
		self.monster_sprites.empty() 
		self.market_sprites.empty()

		for x, y, surf in self.tmx_map.get_layer_by_name("ground").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

		for x, y, surf in self.tmx_map.get_layer_by_name("cant_pass").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.collision_sprites))

		for x, y, surf in self.tmx_map.get_layer_by_name("buildings").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.market_sprites))
		
		for x, y, surf in self.tmx_map.get_layer_by_name("objects").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

		for x, y, surf in self.tmx_map.get_layer_by_name("life_powerUp").tiles():
			Item((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.pickup_items_grups),"apple")


		for x, y, surf in self.tmx_map.get_layer_by_name("shield_powerUp").tiles():
			Item((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.pickup_items_grups),"shield")

		for x, y, surf in self.tmx_map.get_layer_by_name("slime").tiles():
			self.monster = Monster((x * TILE_SIZE, y * TILE_SIZE),  (self.all_sprites,self.monster_sprites), self.player)


	def setup_market(self, market_path):
		self.collision_sprites.empty()
		self.all_sprites.empty()
		self.monster_sprites.empty() 
		self.market_sprites.empty()

		tmx_map = pytmx.load_pygame(market_path)

		for x, y, surf in tmx_map.get_layer_by_name("ground").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

		for x, y, surf in tmx_map.get_layer_by_name("cant_pass").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.collision_sprites))

		for x, y, surf in tmx_map.get_layer_by_name("seller").tiles():
			self.seller = Seller((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

		self.market_on = True


		self.player.rect.x = 30
		self.player.rect.y = 400






	def market(self):
		if self.market_on:
			#entra in shop con tasto G
			if self.player.g_pressed:
				self.seller.display_market(self.game_surface)

	def change_map(self):

		if self.player.rect.x > WIDTH:
			self.update_position(0, 1)
			self.player.rect.x = 10

		if self.player.rect.x < 0:
			self.update_position(0, -1)
			self.player.rect.x = WIDTH - 10

		if self.player.rect.y > HEIGHT:
			self.update_position(1, 0)
			self.player.rect.y = 10

		if self.player.hitbox.y < 0:
			self.update_position(-1, 0)
			self.player.rect.y = HEIGHT -10


		for sprites in self.market_sprites:
			if sprites.rect.colliderect(self.player.hitbox):
				self.player.remove(self.all_sprites) 
				self.setup_market(self.market_map_path)
				self.player.add(self.all_sprites) 

	def update_position(self, row_change, col_change):
		#Aggiorna la posizione della mappa e ricarica gli elementi 
		self.current_row += row_change
		self.current_col += col_change
		self.current_map_key = self.map_grid[self.current_row][self.current_col]
		self.tmx_map = pytmx.load_pygame(self.map_files[self.current_map_key])

		self.player.remove(self.all_sprites)  # per non far coprire il personaggio dalla mappa
		self.setup()
		self.player.add(self.all_sprites)

	def update_shield(self):
		current_time = pygame.time.get_ticks()

		# Se è passato il tempo limite, lo scudo si disattiva
		if self.player.shield and (current_time - self.player.last_shield > 5000):
			self.player.shield = False	

	#collsione del player con i mostri
	def collide_player_to_monster(self):
 	# Se il player sta attaccando
			collided_monsters = pygame.sprite.spritecollide(self.player, self.monster_sprites, False)
			for monster in collided_monsters:
				if self.player.hit: 
					monster.life -= 1  # Riduci la vita del mostro colpito
					self.player.coin_count +=0.5

	def run(self):
		self.game_surface.fill((0, 0, 0))
		self.all_sprites.update()
		self.handle_input()
		self.change_map()
		self.market()
		self.all_sprites.draw(self.game_surface)
		self.hud.draw(self.game_surface)
		self.collide_player_to_monster()
		self.update_shield()
		self.monster.check_player_shield(self.player.shield)

		if self.game_state == "inventory":
			self.inventory.update()

		if self.player.shield:
			self.hud.draw_item_text("shield")



		# pygame.draw.rect(self.game_surface, (255, 0, 0), self.player.hitbox, 2)
		# for monster in self.monster_sprites:
		# 	pygame.draw.rect(self.game_surface, (255, 0, 0), monster.activate_rect, 2)



