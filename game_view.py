
import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT,
    COLOR_PANEL, COLOR_PANEL_BORDER, GameState
)


class GameView:
    def __init__(self, screen):
        self.screen = screen

        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 17)
        self.title_font = pygame.font.SysFont("Arial", 58, bold=True)
        self.medium_font = pygame.font.SysFont("Arial", 32, bold=True)

        self.cyan = (0, 220, 255)
        self.blue = (35, 100, 255)
        self.orange = (255, 145, 40)
        self.white = (245, 245, 255)
        self.dark = (10, 14, 25)
        self.gray = (160, 170, 190)

        cx = WINDOW_WIDTH // 2

        # Boutons partagés avec le contrôleur
        self.play_button = pygame.Rect(cx - 150, 400, 300, 65)
        self.quit_button = pygame.Rect(cx - 150, 490, 300, 60)
        self.menu_button = pygame.Rect(cx - 150, 490, 300, 60)

    def draw(self, model):
        self.screen.fill(self.dark)

        if model.state == GameState.MENU:
            self._draw_menu(model)

        elif model.state == GameState.RACING:
            self._draw_racing(model)

        elif model.state == GameState.FINISHED:
            self._draw_finished()

    # ---------------- BACKGROUND ----------------

    def _draw_background(self):
        self.screen.fill((8, 12, 24))

        # Bandes décoratives
        for y in range(0, WINDOW_HEIGHT, 80):
            pygame.draw.line(
                self.screen,
                (15, 25, 42),
                (0, y),
                (WINDOW_WIDTH, y),
                1
            )

        # Lumières sur les côtés
        for y in range(30, WINDOW_HEIGHT, 90):
            pygame.draw.circle(self.screen, self.cyan, (40, y), 3)
            pygame.draw.circle(
                self.screen, self.orange,
                (WINDOW_WIDTH - 40, y), 3
            )

    # ---------------- BUTTONS ----------------

    def _draw_button(self, text, rect, mouse_pos, color=None):
        if color is None:
            color = self.cyan

        hovered = rect.collidepoint(mouse_pos)

        fill_color = (25, 45, 65) if hovered else (15, 22, 38)
        border_color = self.white if hovered else color
        text_color = self.white if hovered else color

        pygame.draw.rect(
            self.screen, fill_color, rect, border_radius=12
        )

        pygame.draw.rect(
            self.screen, border_color, rect,
            3, border_radius=12
        )

        label = self.font.render(text, True, text_color)
        self.screen.blit(label, label.get_rect(center=rect.center))

    # ---------------- MENU ----------------

    def _draw_menu(self, model):
        self._draw_background()

        cx = WINDOW_WIDTH // 2
        mouse_pos = pygame.mouse.get_pos()

        # Panneau central
        panel = pygame.Rect(cx - 340, 90, 680, 470)

        pygame.draw.rect(
            self.screen, (15, 20, 35),
            panel, border_radius=24
        )

        pygame.draw.rect(
            self.screen, self.cyan,
            panel, 2, border_radius=24
        )

        # Titre
        title = self.title_font.render("RACING ELITE", True, self.white)
        self.screen.blit(
            title, title.get_rect(center=(cx, 160))
        )

        # Ligne décorative
        pygame.draw.line(
            self.screen, self.orange,
            (cx - 170, 200), (cx + 170, 200), 3
        )

        subtitle = self.small_font.render(
            "2 PLAYERS  |  ARCADE RACING",
            True, self.gray
        )

        self.screen.blit(
            subtitle, subtitle.get_rect(center=(cx, 235))
        )

        # Sélection du circuit
        track_name = model.available_tracks[model.selected_circuit]

        track_rect = pygame.Rect(cx - 240, 280, 480, 65)

        pygame.draw.rect(
            self.screen, (25, 32, 50),
            track_rect, border_radius=10
        )

        pygame.draw.rect(
            self.screen, self.orange,
            track_rect, 2, border_radius=10
        )

        track_text = self.font.render(
            f"CIRCUIT : {track_name}",
            True, self.orange
        )

        self.screen.blit(
            track_text, track_text.get_rect(center=track_rect.center)
        )

        # Flèches
        left_arrow = self.medium_font.render("<", True, self.white)
        right_arrow = self.medium_font.render(">", True, self.white)

        self.screen.blit(left_arrow, (cx - 215, 294))
        self.screen.blit(right_arrow, (cx + 190, 294))

        # Boutons
        self._draw_button(
            "ENTRER  /  JOUER",
            self.play_button,
            mouse_pos,
            self.cyan
        )

        self._draw_button(
            "QUITTER",
            self.quit_button,
            mouse_pos,
            self.orange
        )

        # Instructions
        hint = self.small_font.render(
            "Fleches gauche / droite : changer de circuit",
            True, self.gray
        )

        self.screen.blit(
            hint, hint.get_rect(center=(cx, WINDOW_HEIGHT - 25))
        )

    # ---------------- RACING ----------------

    def _draw_racing(self, model):
        if model.circuit is None:
            return

        # Circuit
        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                self.screen.blit(
                    tile.get_sprite(TILE_SIZE),
                    (col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                )

        # Voitures
        for car in model.cars:
            surf, rect = car.get_rotated_sprite()
            self.screen.blit(surf, rect)

            label = self.small_font.render(
                f"J{car.player}", True, self.white
            )

            self.screen.blit(
                label, (int(car.x) - 4, int(car.y) - 8)
            )

        # Bandeau HUD
        hud = pygame.Surface((WINDOW_WIDTH, 40), pygame.SRCALPHA)
        hud.fill((5, 10, 20, 210))
        self.screen.blit(hud, (0, 0))

        title = self.small_font.render(
            "RACING ELITE", True, self.cyan
        )
        self.screen.blit(title, (15, 10))

        legend = self.small_font.render(
            "J1 : ZQSD / WASD    J2 : FLECHES    BOOST : ESPACE / ENTREE    ECHAP : MENU",
            True, self.white
        )

        footer = pygame.Surface((WINDOW_WIDTH, 30), pygame.SRCALPHA)
        footer.fill((0, 0, 0, 180))
        self.screen.blit(footer, (0, WINDOW_HEIGHT - 30))
        self.screen.blit(legend, (10, WINDOW_HEIGHT - 23))

    # ---------------- FIN ----------------

    def _draw_finished(self):
        self._draw_background()

        cx = WINDOW_WIDTH // 2

        panel = pygame.Rect(cx - 320, 150, 640, 350)

        pygame.draw.rect(
            self.screen, (15, 20, 35),
            panel, border_radius=24
        )

        pygame.draw.rect(
            self.screen, self.orange,
            panel, 3, border_radius=24
        )

        title = self.title_font.render(
            "COURSE TERMINEE", True, self.orange
        )

        self.screen.blit(
            title, title.get_rect(center=(cx, 240))
        )

        subtitle = self.medium_font.render(
            "Bravo aux pilotes !",
            True, self.white
        )

        self.screen.blit(
            subtitle, subtitle.get_rect(center=(cx, 320))
        )

        mouse_pos = pygame.mouse.get_pos()

        self._draw_button(
            "RETOUR AU MENU",
            self.menu_button,
            mouse_pos,
            self.cyan
        )
