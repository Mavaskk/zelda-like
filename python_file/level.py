from settings import *
from player import *
from monster import *
from map_setup import *
from hud import *
from seller import *
from Item import *
from Inventory import Inventory
from Key import *
from Boss import *



class Level():
	def __init__(self, game_surface):
		super().__init__()


		self.game_surface = game_surface
		


		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.monster_sprites = pygame.sprite.Group()
		self.market_sprites = pygame.sprite.Group()
		self.pickup_items_grups = pygame.sprite.Group()
		self.portal_sprites = pygame.sprite.Group()

		#keys drop from monsters
		self.key = Key()
		self.last_monster_death_rect = None
		self.key_spawn_time = None

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

		self.picked_items = [] 

		self.current_row = 0
		self.current_col = 0

		#bol
		self.market_status = False
		self.inventory_key = False 
		self.g_pressed = False
		self.key_drop_status = False



		self.current_map_key = self.map_grid[self.current_row][self.current_col]
		self.tmx_map = pytmx.load_pygame(self.map_files[self.current_map_key])
		
		self.market_map_path =  "../zelda-like/assets/tileset/file_tmx/market_1.tmx"
		self.dungeon_map_path =  "../zelda-like/assets/tileset/file_tmx/dungeon_room1.tmx"
		self.potion = pygame.image.load('../zelda-like/assets/market/potions/speed_potion.png').convert_alpha()


		self.player = Player(self.collision_sprites) 
		self.boss = Boss(self.player)
		self.hud = Hud(self.player,self.game_surface,self.boss)
		self.inventory = Inventory(self.player,self.game_surface)
		self.game_state = "gameplay"
		self.setup()
		# self.setup_market(self.market_map_path) #accedi direttamente al market
		self.setup_dungeon(self.dungeon_map_path) #accedi direttamente al market
		self.all_sprites.add(self.player) #aggiungi il player alle sprite per ultimo cosi non c'è niente sopra

		

	def apply_item_to_player(self,item):
		if item is not None:
			if item.type == "apple":
				self.player.life += item.power
			if item.type == "shield":
				# self.activate_shield(item.power)
				self.player.shield = True
				self.player.last_shield = pygame.time.get_ticks()
			if item.type == "speed":
				self.player.speed_boost = True
				self.player.last_speed_boost = pygame.time.get_ticks()

		else:
			print("item non utilizzabile") #fai apparire messaggio di errore

	def clear_sprites(self):
		#svuota i gruppi di sprites
		self.collision_sprites.empty()
		self.pickup_items_grups.empty()
		self.all_sprites.empty()
		self.monster_sprites.empty() 
		self.market_sprites.empty()		


	def handle_input(self):

		keys = pygame.key.get_pressed()
		moving = False

		if keys[pygame.K_g]: #apri inventario
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
				if self.market_status:
					if self.seller.talking:
						if self.player.coin_count >= 10:
							current_time_buy = pygame.time.get_ticks() 
							cooldown_buy = 400
							if len(self.player.bag) <= 15:
								if current_time_buy - self.seller.last_buy > cooldown_buy:
									potion = self.seller.trade()
									self.player.bag.append(potion)
									self.player.coin_count -= 10  
									self.seller.last_buy = current_time_buy
				else:
					for item in self.pickup_items_grups:
						if self.player.rect.colliderect(item):
							if len(self.player.bag) <= 15:
								self.player.bag.append(item)
								self.picked_items.append(item)
								item.kill()						
							else:
								print("inventario pieno")
			elif keys[pygame.K_q]: #parla con il mercante
				current_time_talk = pygame.time.get_ticks()
				cooldown_talk = 200
				if self.market_status:
					if self.player.rect.colliderect(self.seller.hitbox):
						if current_time_talk - self.seller.last_talk > cooldown_talk:
							self.seller.talking = not self.seller.talking
							
							self.seller.last_talk = current_time_talk

						
			# Attacco con il tasto F
			if keys[pygame.K_f] and not self.player.hit:
				current_time = pygame.time.get_ticks()
				if current_time - self.player.last_hit > 400:
					self.player.hit = True
					self.player.last_hit = current_time
					# self.collide_player_to_boss()


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
						if self.inventory.remove_item() == "key":
							self.player.key_counter -= 1
						self.inventory.last_remove_time = current_time_remove
				if keys[pygame.K_f]:  # usa oggetto
					use_cooldown = 200
					current_time_use = pygame.time.get_ticks()
					if current_time_use - self.inventory.last_use_time > use_cooldown:
						item = self.inventory.use_item()
						self.apply_item_to_player(item)
						self.inventory.last_use_time = current_time_use
				
		if not self.player.hit:
			self.player.animation_walk(moving,self.player.walk_right,self.player.walk_back,self.player.walk_front)



	def setup(self):
		self.clear_sprites()

		for x, y, surf in self.tmx_map.get_layer_by_name("ground").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

		for x, y, surf in self.tmx_map.get_layer_by_name("cant_pass").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.collision_sprites))

		for x, y, surf in self.tmx_map.get_layer_by_name("buildings").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.market_sprites))
		
		for x, y, surf in self.tmx_map.get_layer_by_name("objects").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

		for x, y, surf in self.tmx_map.get_layer_by_name("life_powerUp").tiles():
			self.should_render_item(x,y,surf,"apple")

		for x, y, surf in self.tmx_map.get_layer_by_name("shield_powerUp").tiles():
			self.should_render_item(x,y,surf,"shield")

		for x, y, surf in self.tmx_map.get_layer_by_name("slime").tiles():
			self.monster = Monster((x * TILE_SIZE, y * TILE_SIZE),  (self.all_sprites,self.monster_sprites), self.player)

		if self.current_col == 2 and self.current_row == 2:
			for x, y, surf in self.tmx_map.get_layer_by_name("portal").tiles():
				Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.portal_sprites))

	def setup_dungeon(self,dungeon_path):
		self.clear_sprites()
		tmx_map = pytmx.load_pygame(dungeon_path)

		for x, y, surf in tmx_map.get_layer_by_name("ground").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

		for x, y, surf in tmx_map.get_layer_by_name("cant_pass").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.collision_sprites))

		# for x, y, surf in tmx_map.get_layer_by_name("cant_pass").tiles():
		# 	Boss((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.monster_sprites))


		self.player.rect.x = 30
		self.player.rect.y = 400


		self.all_sprites.add(self.boss) #aggiungi boss alle sprite per ultimo cosi non ci sono problemi con sovrapposizioni




	def setup_market(self, market_path):
		self.clear_sprites()
		tmx_map = pytmx.load_pygame(market_path)

		for x, y, surf in tmx_map.get_layer_by_name("ground").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites))

		for x, y, surf in tmx_map.get_layer_by_name("cant_pass").tiles():
			Structures((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites,self.collision_sprites))

		for x, y, surf in tmx_map.get_layer_by_name("seller").tiles():
			self.seller = Seller((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites),self.game_surface)

		self.market_status = True


		self.player.rect.x = 30
		self.player.rect.y = 400

	def should_render_item(self,x,y,surf,type):
			already_collected = False
			for item in self.picked_items: #non uso la bag del player cosi quando uso un oggetto questo non ricompare dopo sulla mappa perchè non è più nell'invetario
				if item.rect.x == x * TILE_SIZE and item.rect.y == y * TILE_SIZE: #confronto le x e y delle sprite con quelle delle sprite
					already_collected = True
					break
			if not already_collected: #render item non ancora raccolti
				Item((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.pickup_items_grups), type)	


	def market(self):
		if self.market_status:
			self.seller.display_market(self.game_surface)
			if self.seller.talking:
				if self.player.coin_count < 10:
					self.seller.draw_no_coin_text()

				else:
					self.seller.draw_item_speed_potion()

	def change_map(self):


		if not self.market_status:	
			
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
		
		
		else:
			if self.player.rect.x > WIDTH:
				self.update_position(0,0)	
				self.market_status = False	
				self.player.remove(self.all_sprites) 
				self.player.add(self.all_sprites) 
				self.player.rect.x = 55
				self.player.rect.y = 155


		for sprites in self.market_sprites:
			if sprites.rect.colliderect(self.player.hitbox):
				self.player.remove(self.all_sprites) 
				self.setup_market(self.market_map_path)
				self.player.add(self.all_sprites) 

		for sprites in self.portal_sprites:
			if sprites.rect.colliderect(self.player.hitbox) and self.player.key_counter >= 3:
				self.player.key_counter -= 3
				self.player.remove(self.all_sprites) 
				print("entro nel void")
				print(self.player.key_counter)
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
		shield_duration = 5000

		# Se è passato il tempo limite, lo scudo si disattiva
		if self.player.shield and (current_time - self.player.last_shield > shield_duration):
			self.player.shield = False	

	def update_speed(self):
		current_time = pygame.time.get_ticks()
		speed_duration = 5000

		# Se è passato il tempo limite, lo pozione si disattiva
		if self.player.speed_boost and (current_time - self.player.last_speed_boost > speed_duration):
			self.player.speed_boost = False	
			self.player.speed = 3

	#collsione del player con i mostri
	def collide_player_to_monster(self):
 	# Se il player sta attaccando
			collided_monsters = pygame.sprite.spritecollide(self.player, self.monster_sprites, False)
			for monster in collided_monsters:
				if self.player.hit: 
					self.last_monster_death_rect = monster.rect
					monster.life -= 1  # Riduci la vita del mostro colpito
					self.player.coin_count += 0.5
					if monster.drop_key():
						self.key_drop_status = True
						self.key_spawn_time = pygame.time.get_ticks() 
						print("chiave ottenuta")
						self.player.key_counter += 1
						self.player.bag.append(self.key)

	def collide_player_to_boss(self):
		if self.player.rect.colliderect(self.boss.rect):
			if self.player.hit and not self.boss.just_hit:
				self.boss.life -= 1
				self.boss.just_hit = True
				print("player colpito boss")
				print(self.boss.life)


	def render_drop_key(self):
		if self.key_drop_status:
			self.game_surface.blit(self.key.image,self.last_monster_death_rect)			
			current_time = pygame.time.get_ticks()
			if current_time - self.key_spawn_time > 750:
				self.key_drop_status = False


	def run(self):
		self.game_surface.fill((0, 0, 0))
		self.all_sprites.update()
		self.handle_input()
		self.change_map()
		self.all_sprites.draw(self.game_surface)
		self.hud.draw(self.game_surface)
		self.collide_player_to_monster()
		self.collide_player_to_boss()
		
		if self.boss.fireball_bol:
			self.game_surface.blit(self.boss.fireball_sprite,self.boss.fireball_rect)

		self.update_shield()
		self.update_speed()
		for monster in self.monster_sprites:
			monster.check_player_shield(self.player.shield)

		self.market()



		if self.game_state == "inventory":
			self.inventory.update()

		if self.player.shield:
			self.hud.draw_item_text("shield")

		if self.player.speed_boost:
			self.hud.draw_item_text("speed")

		self.render_drop_key()

		# print(self.player.key_counter)


		# pygame.draw.rect(self.game_surface, (255, 0, 0), self.player.hitbox, 2)
		# for monster in self.monster_sprites:
		# 	pygame.draw.rect(self.game_surface, (255, 0, 0), monster.activate_rect, 2)
		pygame.draw.rect(self.game_surface, (255, 0, 0), self.boss.rect, 2)
		pygame.draw.rect(self.game_surface, (255, 0, 0), self.player.rect, 2)
		



