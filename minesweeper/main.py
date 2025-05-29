import argparse
from game.game import Game

def main():
    parser = argparse.ArgumentParser(description="Minesweeper Game")
    parser.add_argument("--width", type=int, default=10, help="Width of the board")
    parser.add_argument("--height", type=int, default=10, help="Height of the board")
    parser.add_argument("--mines", type=int, default=15, help="Number of mines")
    parser.add_argument("--cellsize", type=int, default=40, help="Size of each cell in pixels")
    args = parser.parse_args()

    game = Game(width=args.width, height=args.height, 
                mine_count=args.mines, cell_size=args.cellsize)
    game.run()

if __name__ == "__main__":
    main()