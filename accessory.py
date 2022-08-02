import pygame

from config import *


class Button:
    def __init__(self, image, position: (int, int), name_text: str, font_type, base_color, hover_color):
        self.image = image
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.font = font_type
        self.base_color, self.hovering_color = base_color, hover_color
        self.name = name_text
        self.text = self.font.render(self.name, True, self.base_color)

        if self.image is None:
            self.image = self.text
        else:
            self.image = image
        
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        
        screen.blit(self.text, self.text_rect)

    def input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def set_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.name, True, self.hovering_color)
        else:
            self.text = self.font.render(self.name, True, self.base_color)

class Timer:
    def __init__(self, manager, minute, additional):
        self.manager = manager
        
        self.minute = minute
        self.additional_seconds = additional
        self.second = 0
        
        self.format_time()

    def time_mechanics(self):
        self.minute = int(self.minute)
        self.second = int(self.second)
        if self.minute > 0:
            if self.second > 0:
                self.second -= 1
                return (self.minute, self.second)
            self.minute -= 1
            self.second = 59
            return (self.minute, self.second)
        if self.second > 0:
            self.second -= 1
            return (self.minute, self.second)
        return (0, 0)

    def format_time(self):
        if (self.minute, self.second) == (0, 0):
            self.timer = "Time's Up!"
            return
        if self.minute < 10:
            self.minute = str(0) + str(self.minute)
        if self.second < 10:
            self.second = str(0) + str(self.second)
        self.timer = f"{self.minute}:{self.second}"

    def update(self):
        self.time_mechanics()
        self.format_time()

    def add_additional(self):
        pass #TODO: Add additional seconds

    def draw(self, pos, size, screen):
        font = GET_FONT("Timer", size)
        timer = font.render(self.timer, True, (255, 255, 255))
        timer_rect = timer.get_rect()
        timer_rect.center = pos
        screen.blit(timer, timer_rect)
        
