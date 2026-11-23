import pygame
from constants import TILE_SIZE

# Terrains proches de la capture de référence : herbe, route, terre, sable, glace.
TERRAINS = {
    "grass": {"color": (35, 170, 75), "traction": 0.58, "label": "Herbe"},
    "road": {"color": (75, 76, 82), "traction": 1.00, "label": "Route"},
    "dirt": {"color": (135, 66, 22), "traction": 0.72, "label": "Terre"},
    "sand": {"color": (190, 177, 126), "traction": 0.66, "label": "Sable"},
    "ice": {"color": (145, 205, 220), "traction": 0.28, "label": "Glace"},
    "void": {"color": (28, 30, 38), "traction": 0.0, "label": "Vide"},
}

class RoadTile:
    def __init__(self, col, row, terrain="sand", block=""):
        self.col = col
        self.row = row
        self.terrain = terrain
        self.block = block
        self.sprite = None

    def properties(self):
        return TERRAINS.get(self.terrain, TERRAINS["sand"])

    def get_sprite(self, tile_size=TILE_SIZE):
        if self.sprite is not None and self.sprite.get_size() == (tile_size, tile_size):
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(self.properties()["color"])
        # Trame discrète, similaire à une grille de cases.
        edge = tuple(max(0, c - 18) for c in self.properties()["color"])
        pygame.draw.rect(surface, edge, surface.get_rect(), 1)
        if self.terrain == "road":
            for x in range(8, tile_size, 16):
                pygame.draw.line(surface, (62, 63, 68), (x, 0), (x, tile_size), 1)
        if self.block:
            font = pygame.font.Font(None, 25)
            label = font.render(self.block, True, (255, 255, 255))
            surface.blit(label, label.get_rect(center=(tile_size // 2, tile_size // 2)))
        self.sprite = surface
        return surface
