import pygame.font

import theme


class Button():
    """The Play button. Its size, colors and text come from theme.py."""

    def __init__(self, settings, screen, msg=None):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = theme.BUTTON_SIZE
        self.button_color = theme.BUTTON_COLOR
        self.text_color = theme.BUTTON_TEXT_COLOR
        self.font = pygame.font.SysFont(None, theme.FONT_BUTTON)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery + 100

        self.prep_msg(msg or theme.TEXTS["play_button"])

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)