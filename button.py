import pygame
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)

class Button:
    def __init__(self, x, y, width, height, color, color_hover, color_selected, label, font_size, radius, selected = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.color_hover = color_hover
        self.color_selected = color_selected
        self.label = label
        self.font_size = font_size
        self.radius = radius
        self.selected = selected


    def draw_button(self, win):
        pos = pygame.mouse.get_pos()
        button_space = Rect(self.x, self.y, self.width, self.height)

        if button_space.collidepoint(pos) and not self.selected:
            pygame.draw.rect(win, self.color_hover, button_space, border_radius=self.radius)
        else:
            pygame.draw.rect(win, self.color, button_space, border_radius=self.radius)
        if self.selected:
            pygame.draw.rect(win, self.color_selected, button_space, border_radius=self.radius)

        button_font = pygame.font.SysFont('Sans Serif', self.font_size)
        text = button_font.render(self.label, True, BLACK)
        text_length = text.get_width()
        text_height = text.get_height()
        win.blit(text, (self.x + int(self.width / 2) - int(text_length / 2), self.y + int(self.height / 2) - int(text_height / 2)))
