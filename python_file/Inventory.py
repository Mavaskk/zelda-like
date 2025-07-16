from settings import *

class Inventory(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
    
    def add_item(self,item):
        self.player.bag.append(item)
        for item in self.player.bag:
            print(self.player.bag)

    def remove_item():
        "sdk"
    
    def draw():
        "sdadk"
            

    