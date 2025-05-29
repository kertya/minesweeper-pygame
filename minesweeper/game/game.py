import pygame
from .board import Board

class Game:
    def __init__(self, width=10, height=10, mine_count=15, cell_size=40):
        pygame.init()
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.cell_size = cell_size
        self.screen_width = width * cell_size
        self.screen_height = height * cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Minesweeper")
        self.board = Board(width, height, mine_count, cell_size)
        self.running = True
        self.game_over = False
        self.font = pygame.font.SysFont('Arial', 32)
    
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    result = None
                    if event.button == 1:  # Ліва кнопка миші
                        esult = self.board.handle_click(event.pos)
                        if result == "game_over":
                            self.game_over = True
                    elif event.button == 3:  # Права кнопка миші
                        self.board.handle_click(event.pos, right_click=True)
            
            self.screen.fill((255, 255, 255))
            self.board.draw(self.screen)

            if self.game_over:
                self.draw_game_over()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

    def draw_game_over(self):
        """Відображає повідомлення про програш"""
        text = self.font.render('GAME OVER!', True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2))
        self.screen.blit(text, text_rect)