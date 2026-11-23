import pygame

class InputHandler:
    """Centralise les commandes clavier des deux joueurs."""
    def get_inputs(self):
        keys = pygame.key.get_pressed()
        return [
            {"accelerate": keys[pygame.K_w] or keys[pygame.K_z],
             "brake": keys[pygame.K_s],
             "left": keys[pygame.K_a] or keys[pygame.K_q],
             "right": keys[pygame.K_d],
             "item": keys[pygame.K_SPACE]},
            {"accelerate": keys[pygame.K_UP], "brake": keys[pygame.K_DOWN],
             "left": keys[pygame.K_LEFT], "right": keys[pygame.K_RIGHT],
             "item": keys[pygame.K_RETURN]},
        ]
