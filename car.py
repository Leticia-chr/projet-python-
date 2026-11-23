import math
import pygame
from constants import CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, GRIP_SCALE

class Car:
    MAX_SPEED = 5.0
    MAX_REVERSE_SPEED = -2.0
    AIR_FRICTION = 0.012
    DRIFT_FRICTION = 0.025
    BRAKE_POWER = 0.09
    TURN_SPEED = 2.8

    def __init__(self, start_col, start_row, player=1, color=None):
        self.x = float(start_col * TILE_SIZE + TILE_SIZE // 2)
        self.y = float(start_row * TILE_SIZE + TILE_SIZE // 2)
        self.speed = 0.0
        self.angle = 0.0
        self.player = player
        self.item_count = 1
        self.boost_timer = 0
        self.color = color or ((220, 40, 50) if player == 1 else (35, 100, 230))
        self.sprite = self.build_sprite()

    def accelerate(self): self.speed = min(self.MAX_SPEED, self.speed + CAR_ACCELERATION)
    def brake(self):
        if self.speed > 0: self.speed = max(0.0, self.speed - self.BRAKE_POWER)
        elif self.speed < 0: self.speed = min(0.0, self.speed + self.BRAKE_POWER)
    def reverse(self): self.speed = max(self.MAX_REVERSE_SPEED, self.speed - CAR_ACCELERATION)

    def steer(self, direction, traction=1.0):
        if abs(self.speed) < 0.05: return
        grip = max(0.12, min(1.0, float(traction) * GRIP_SCALE))
        factor = min(1.0, abs(self.speed) / 1.5)
        reverse_sign = 1 if self.speed >= 0 else -1
        self.angle = (self.angle + direction * self.TURN_SPEED * grip * factor * reverse_sign) % 360

    def apply_boost(self):
        self.speed = min(self.MAX_SPEED + 1.5, self.speed + 1.2)
        self.boost_timer = 60

    def update_position(self, traction=1.0):
        friction = self.DRIFT_FRICTION if traction < 0.6 else self.AIR_FRICTION
        if self.speed > 0: self.speed = max(0.0, self.speed - friction)
        elif self.speed < 0: self.speed = min(0.0, self.speed + friction)
        angle = math.radians(self.angle)
        self.x += self.speed * math.sin(angle)
        self.y -= self.speed * math.cos(angle)

    def build_sprite(self):
        surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (1, 1, CAR_WIDTH-2, CAR_HEIGHT-2), border_radius=5)
        pygame.draw.rect(surface, (190, 225, 245), (5, 7, CAR_WIDTH-10, 9), border_radius=2)
        pygame.draw.rect(surface, (35, 35, 40), (4, 27, CAR_WIDTH-8, 5), border_radius=2)
        return surface

    def get_rotated_sprite(self):
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        return rotated, rotated.get_rect(center=(round(self.x), round(self.y)))
