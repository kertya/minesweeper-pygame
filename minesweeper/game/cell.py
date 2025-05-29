import pygame

class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.is_mine = False
        self.is_open = False
        self.has_flag = False
        self.neighbor_mines = 0
        self.rect = pygame.Rect(x * size, y * size, size, size)
    
    def draw(self, screen):
        color = (200, 200, 200) if not self.is_open else (150, 150, 150)
        pygame.draw.rect(screen, color, self.rect)
        
        if self.is_open and self.is_mine:
            pygame.draw.circle(screen, (0, 0, 0), self.rect.center, self.size // 3)
        elif self.is_open and self.neighbor_mines > 0:
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(self.neighbor_mines), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=self.rect.center))
        elif self.has_flag:
            pygame.draw.polygon(screen, (255, 0, 0), [
                (self.rect.centerx, self.rect.centery - 10),
                (self.rect.centerx + 10, self.rect.centery + 5),
                (self.rect.centerx - 10, self.rect.centery + 5)
            ])
    
    def handle_click(self, pos, right_click=False):
        if self.rect.collidepoint(pos):
            if right_click and not self.is_open:
                self.has_flag = not self.has_flag
                return True
            elif not self.is_open and not self.has_flag:
                self.is_open = True
                return True
        return False