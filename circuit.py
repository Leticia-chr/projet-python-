from constants import TILE_SIZE, GRID_COLS, GRID_ROWS
from model.road_tile import RoadTile

class Circuit:
    def __init__(self, grid, name="Circuit classique"):
        self.grid = grid
        self.name = name
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    @classmethod
    def create(cls, track_index=0):
        # Circuit en grille avec zones de terrain colorées et route sinueuse.
        grid = [[RoadTile(c, r, "sand") for c in range(GRID_COLS)] for r in range(GRID_ROWS)]
        # Grandes zones d'herbe et de terre, comme la figure de l'énoncé.
        for r in range(7, GRID_ROWS):
            for c in range(8, GRID_COLS): grid[r][c].terrain = "grass"
        for r in range(1, 8):
            for c in range(1, 12):
                if (r + c + track_index) % 4 in (0, 1): grid[r][c].terrain = "dirt"
        # Route grise sinueuse : ligne de départ en bas à gauche, boucle vers le haut.
        route = set()
        for c in range(0, 8): route.add((c, 10))
        for r in range(7, 11): route.add((7, r))
        for c in range(4, 8): route.add((c, 7))
        for r in range(5, 8): route.add((4, r))
        for c in range(2, 5): route.add((c, 5))
        for r in range(3, 6): route.add((2, r))
        for c in range(2, 7): route.add((c, 3))
        for r in range(1, 4): route.add((6, r))
        for c in range(6, 10): route.add((c, 1))
        for r in range(1, 7): route.add((9, r))
        for c in range(6, 10): route.add((c, 6))
        for c, r in route:
            grid[r][c].terrain = "road"
        # Blocs / repères requis par le sujet.
        for c, r, label in [(0,11,"1"),(1,11,"2"),(2,5,"?"),(3,5,"?"),(6,1,"C"),(11,2,"B"),(12,2,"B"),(11,3,"B"),(12,3,"B"),(10,8,"F"),(10,10,"F"),(10,11,"F"),(12,10,"B"),(12,11,"B")]:
            if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
                grid[r][c].block = label
        return cls(grid, "Circuit désert" if track_index else "Circuit classique")

    def get_tile(self, col, row):
        if 0 <= row < self.rows and 0 <= col < self.cols: return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px, py):
        return self.get_tile(int(px // TILE_SIZE), int(py // TILE_SIZE))

    def pixel_width(self): return self.cols * TILE_SIZE
    def pixel_height(self): return self.rows * TILE_SIZE
