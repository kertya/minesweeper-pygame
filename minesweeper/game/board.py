import pygame
import random
from .cell import Cell

class Board:
    def __init__(self, width, height, mine_count, cell_size=40):
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.cell_size = cell_size
        self.cells = []
        self.game_over = False
        self.font = pygame.font.SysFont('Arial', 48)  # Додано шрифт
        self.generate_board()
    
    def generate_board(self, safe_x=None, safe_y=None):
        # Створення клітинок
        self.cells = [
            [Cell(x, y, self.cell_size) for y in range(self.height)]
            for x in range(self.width)
        ]
        
        # Розміщення мін з урахуванням безпечної клітинки
        mines_placed = 0
        while mines_placed < self.mine_count:
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            if (x == safe_x and y == safe_y) or self.cells[x][y].is_mine:
                continue
            self.cells[x][y].is_mine = True
            mines_placed += 1
        
        # Підрахунок сусідніх мін
        for x in range(self.width):
            for y in range(self.height):
                if not self.cells[x][y].is_mine:
                    self.cells[x][y].neighbor_mines = self.count_adjacent_mines(x, y)
    
    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.cells[nx][ny].is_mine:
                        count += 1
        return count
    
    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

        # Малюємо повідомлення про програш
        if self.game_over:
            # Напівпрозорий чорний фон
            overlay = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Темніший фон для кращої видимості
            screen.blit(overlay, (0, 0))
            
            # Текст "ГРА ЗАКІНЧЕНА"
            text = self.font.render('ГРА ЗАКІНЧЕНА', True, (255, 50, 50))
            text_rect = text.get_rect(center=(self.width * self.cell_size // 2, self.height * self.cell_size // 2))
            screen.blit(text, text_rect)
        
    def handle_click(self, pos, right_click=False):
        if self.game_over:
            return None  # Блокуємо всі кліки після програшу
            
        clicked = False
        for row in self.cells:
            for cell in row:
                if cell.rect.collidepoint(pos):
                    if right_click and not cell.is_open:
                        cell.has_flag = not cell.has_flag
                        return "flag"
                    elif not right_click and not cell.is_open and not cell.has_flag:
                        cell.is_open = True
                        if cell.is_mine:
                            self.game_over = True
                            self.reveal_all_mines()
                            return "game_over"
                        return "open"
        return None
    
    def reveal_all_mines(self):
        """Показує всі міни на полі"""
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.is_open = True