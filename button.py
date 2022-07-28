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