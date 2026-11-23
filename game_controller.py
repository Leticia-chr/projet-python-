import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GameState
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler
from addons.race_extras import RaceExtras

class GameController:
    """Coordonne le modèle, les entrées, l'affichage et les extensions."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Jeu de course 2D")
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.extras = RaceExtras()
        self.running = True

    def run(self):
        print("Race engine ready")
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.render()
                self.clock.tick(FPS)
        finally:
            pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            elif event.type == pygame.KEYDOWN: self.handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
              if event.button == 1:
                self.handle_mouse_click(event.pos)

    def handle_keydown(self, key):
        if self.model.state == GameState.MENU:
            if key in (pygame.K_LEFT, pygame.K_a, pygame.K_q):
                self.model.selected_circuit = (self.model.selected_circuit - 1) % len(self.model.available_tracks)
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.model.selected_circuit = (self.model.selected_circuit + 1) % len(self.model.available_tracks)
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self.model.load_circuit(); self.extras.reset()
            elif key == pygame.K_ESCAPE: self.running = False
        elif self.model.state == GameState.RACING:
            if key == pygame.K_ESCAPE: self.model.state = GameState.MENU
            elif key in (pygame.K_SPACE, pygame.K_RETURN):
                player_index = 0 if key == pygame.K_SPACE else 1
                if player_index < len(self.model.cars):
                    car = self.model.cars[player_index]
                    if car.item_count > 0:
                        car.item_count -= 1
                        car.apply_boost()
            self.extras.handle_keydown(key, self.model)
        elif self.model.state == GameState.FINISHED:
            if key in (pygame.K_RETURN, pygame.K_SPACE): self.model.state = GameState.MENU
            elif key == pygame.K_ESCAPE: self.running = False

    def update(self):
        if self.model.state == GameState.RACING:
            actions_by_player = self.input_handler.get_inputs()
            for car, actions in zip(self.model.cars, actions_by_player):
                tile = self.model.circuit.get_tile_at_pixel(car.x, car.y)
                traction = tile.properties()["traction"] if tile else 0.3
                if actions["accelerate"]: car.accelerate()
                if actions["brake"]: car.brake()
                if actions["left"]: car.steer(1, traction)
                if actions["right"]: car.steer(-1, traction)
                if car.boost_timer > 0: car.boost_timer -= 1
            self.model.update()
        self.extras.update(self.model, pygame.key.get_pressed())

    def render(self):
        self.view.draw(self.model)
        if self.model.state == GameState.RACING:
            self.extras.draw(self.screen, self.model)
        pygame.display.flip()
