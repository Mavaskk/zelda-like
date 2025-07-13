from settings import *
from player import *
from monster import *
from map_setup import *
from hud import *
from seller import *


class Level():
	def __init__(self, game_surface):

		self.game_surface = game_surface


		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.monster_sprites = pygame.sprite.Group()
		self.market_sprites = pygame.sprite.Group()

		self.map_grid = [
			["overworld_room1", "overworld_room2","overworld_room3"],
			["overworld_room4", "overworld_room5","overworld_room6"],
			["overworld_room7", "overworld_room8","overworld_room9"]

		]

		self.map_files = {
			"overworld_room1": '../game_settembre/assets/tileset/file_tmx/overworld_room1.tmx',
			"overworld_room2": '../game_settembre/assets/tileset/file_tmx/overworld_room2.tmx',
			"overworld_room3": '../game_settembre/assets/tileset/file_tmx/overworld_room3.tmx',
			"overworld_room4": '../game_settembre/assets/tileset/file_tmx/overworld_room4.tmx',
			"overworld_room5": '../game_settembre/assets/tileset/file_tmx/overworld_room5.tmx',
			"overworld_room6": '../game_settembre/assets/tileset/file_tmx/overworld_room6.tmx',
			"overworld_room7": '../game_settembre/assets/tileset/file_tmx/overworld_room7.tmx',
			"overworld_room8": '../game_settembre/assets/tileset/file_tmx/overworld_room8.tmx',
			"overworld_room9": '../game_settembre/assets/tileset/file_tmx/overworld_room9.tmx',
		}

		self.current_row = 0
		self.current_col = 0
		self.market_on = False
		self.current_map_key = self.map_grid[self.current_row][self.current_col]
		self.tmx_map = pytmx.load_pygame(self.map_files[self.current_map_key])
		
		self.market_map_path =  "../game_settembre/assets/tileset/file_tmx/market_1.tmx"

		self.player = Player(self.collision_sprites) 
		self.hud = Hud(self.player)
		self.setup()
		# self.setup_market(self.market_map_path)
		self.all_sprites.add(self.player)

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
		self.collide_player_to_monster()
		self.change_map()
		self.market()

		self.all_sprites.draw(self.game_surface)
		self.hud.draw(self.game_surface)
		#pygame.draw.rect(self.game_surface, (255, 0, 0), self.player.hitbox, 2)
		# for monster in self.monster_sprites:
		# 	pygame.draw.rect(self.game_surface, (255, 0, 0), monster.activate_rect, 2)



