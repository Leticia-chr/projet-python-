import pygame
from constants import GameState

class RaceExtras:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0.0
        self.font = None

    def handle_keydown(self, key, model=None):
        # Objet spécial conservé : Maj accélère brièvement le joueur 1.
        if model is not None and getattr(model, "cars", None) and key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
            model.cars[0].apply_boost()

    def update(self, model, keys=None):
        if model.state != GameState.RACING:
            return
        if self.start_time is None: self.start_time = pygame.time.get_ticks()
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0

    def draw(self, screen, model):
        if model.state != GameState.RACING: return
        if self.font is None: self.font = pygame.font.Font(None, 28)
        text = self.font.render("Chrono : {:.1f} s".format(self.elapsed_time), True, (255,255,255))
        # Fond lisible en haut à gauche.
        pygame.draw.rect(screen, (35, 35, 45), (8, 8, 155, 34), border_radius=5)
        screen.blit(text, (15, 14))

    def reset(self): self.start_time = None; self.elapsed_time = 0.0
