from settings import *

class Seller(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.item_list = []
        self.rect = self.image.get_rect(topleft = pos)

    def trade(self):
        pass

    def display_market(self,screen):
        pygame.draw.rect(screen,(0,0,0),(200,150,100,50))

        