from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, item_type):
        super().__init__(groups)
        self.power = None
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.icon = None
        self.type = item_type  # 'potion' o 'shield'
        if self.type == 'apple':
            self.power = +1
        elif self.type == 'shield':
            self.power = 2000  
