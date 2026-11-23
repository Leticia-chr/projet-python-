from constants import GameState
from model.car import Car
from model.circuit import Circuit

class GameModel:
    def __init__(self):
        self.state = GameState.MENU
        self.circuit = None
        self.car = None
        self.cars = []
        self.selected_track = 0
        self.selected_circuit = 0
        self.available_tracks = ["Circuit classique", "Circuit désert"]

    def load_circuit(self):
        self.circuit = Circuit.create(self.selected_circuit)
        self.cars = [
            Car(0, 10, player=1, color=(225, 45, 55)),
            Car(1, 10, player=2, color=(35, 110, 240)),
        ]
        # Départ orienté vers la droite pour rejoindre la piste.
        for car in self.cars: car.angle = 90
        self.car = self.cars[0]
        self.state = GameState.RACING

    def spawn_car(self):
        self.cars = [Car(0, 10, 1), Car(1, 10, 2, (35, 110, 240))]
        self.car = self.cars[0]

    def update(self):
        if self.state != GameState.RACING or self.circuit is None: return
        for car in self.cars:
            tile = self.circuit.get_tile_at_pixel(car.x, car.y)
            traction = tile.properties()["traction"] if tile else 0.3
            car.update_position(traction)
            car.x = max(12, min(self.circuit.pixel_width()-12, car.x))
            car.y = max(12, min(self.circuit.pixel_height()-12, car.y))
