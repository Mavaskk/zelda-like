import pygame
import pytmx
import random
import math

WIDTH = 512
HEIGHT = 448
FPS = 60
TILE_SIZE = 16
WINDOW_WIDTH = WIDTH * 2  # 1024
WINDOW_HEIGHT = HEIGHT * 2  # 896



pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)  # Prendi il primo joystick disponibile
    joystick.init()

