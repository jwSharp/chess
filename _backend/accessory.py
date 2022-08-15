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
            
            
class Two_Line(Button):
    def __init__(self, image, position: (int, int), name_text1: str, name_text2: str, font_type, base_color, hover_color):
        self.image = image
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.font = font_type
        self.base_color, self.hovering_color = base_color, hover_color
        self.name1 = name_text1
        self.name2 = name_text2
        self.name = name_text1 + name_text2
        self.text1 = self.font.render(self.name1, True, self.base_color)
        self.text2 = self.font.render(self.name2, True, self.base_color)
        self.text = self.font.render(self.name, True, self.base_color)

        if self.image is None:
            self.image = self.text
        else:
            self.image = image

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect1 = self.text1.get_rect(midtop=(self.x_pos, self.y_pos - 30))
        self.text_rect2 = self.text2.get_rect(midbottom=(self.x_pos, self.y_pos + 30))

    def update(self, screen):

        screen.blit(self.text1, self.text_rect1)
        screen.blit(self.text2, self.text_rect2)

    def input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def set_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text1 = self.font.render(self.name1, True, self.hovering_color)
            self.text2 = self.font.render(self.name2, True, self.hovering_color)

        else:
            self.text1 = self.font.render(self.name1, True, self.base_color)
            self.text2 = self.font.render(self.name2, True, self.base_color)


class Timer:
    def __init__(self, manager, minute, additional):
        self.minute = minute
        self.additional_seconds = additional
        self.second = 0
        self.manager = manager
        self.format_time()
        
    def draw(self, screen, pos, size):
        #TODO Move to constructor
        font = GET_FONT("Timer", size)
        timer = font.render(self.timer, True, WHITE)
        
        screen.blit(timer, timer.get_rect(center=pos))
    
    def update(self):
        self.time_mechanics()
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

    def add_additional(self, additional_seconds):
        self.minute = int(self.minute)
        self.second = int(self.second)
        self.second += additional_seconds
        if self.second > 59:
            self.minute += 1
            self.second = self.second - 59
        self.format_time()