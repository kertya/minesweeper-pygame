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
        # Перевіряємо всіх 8 сусідів клітинки (x,y)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Пропускаємо саму клітинку (dx=0, dy=0)
                if dx == 0 and dy == 0:
                    continue
                    
                nx, ny = x + dx, y + dy  # Координати сусіда
                
                # Перевіряємо, чи сусід в межах поля
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.cells[nx][ny].is_mine:
                        count += 1
        return count
    
    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
    
    def handle_click(self, pos, right_click=False):
        for row in self.cells:
            for cell in row:
                if cell.handle_click(pos, right_click):
                    return True
        return False