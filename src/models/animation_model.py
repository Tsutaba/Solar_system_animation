import math
import random
from typing import List

class CelestialBody:
    # Базовый класс для любого космического тела (орбита, позиция, скорость).
    def __init__(self, name: str, distance: float, radius: float, speed: float, color: str):
        self.name = name
        self.distance = distance  # Радиус орбиты (расстояние до центра)
        self.radius = radius      # Размер самого объекта
        self.speed = speed        # Скорость вращения
        self.color = color
        self.angle = random.uniform(0, 2 * math.pi)  # Случайный стартовый угол
        self.x = 0.0
        self.y = 0.0

    def update_position(self, center_x: float, center_y: float, time_scale: float) -> None:
        # Расчет движения по кругу (перевод из полярных координат в декартовы X и Y)
        self.angle += self.speed * time_scale
        self.x = center_x + self.distance * math.cos(self.angle)
        self.y = center_y + self.distance * math.sin(self.angle)

class Planet(CelestialBody):
    # Класс планеты, которая может содержать спутники.
    def __init__(self, name: str, distance: float, radius: float, speed: float, color: str):
        super().__init__(name, distance, radius, speed, color)
        self.moons: List[CelestialBody] = []  # Список спутников планеты

    def add_moon(self, name: str, distance: float, radius: float, speed: float, color: str) -> None:
        self.moons.append(CelestialBody(name, distance, radius, speed, color))

    def update_all_positions(self, sun_x: float, sun_y: float, time_scale: float) -> None:
        # Сначала двигаем саму планету вокруг Солнца
        self.update_position(sun_x, sun_y, time_scale)
        # Затем двигаем её спутники вокруг текущих координат планеты
        for moon in self.moons:
            moon.update_position(self.x, self.y, time_scale)

class SolarSystemModel:
    # Модель всей системы: Солнце, планеты, астероиды.
    def __init__(self, width: int, height: int):
        self.sun_x = width / 2
        self.sun_y = height / 2
        self.sun_radius = 25
        self.planets: List[Planet] = []
        self.asteroids: List[CelestialBody] = []
        
        self._init_planets()
        self._init_asteroid_belt()

    def _init_planets(self) -> None:
        # Добавляем планеты и их спутники (расстояние, размер, скорость, цвет)
        self.planets.append(Planet("Меркурий", 60, 5, 0.04, "#9E9E9E"))
        self.planets.append(Planet("Венера", 95, 9, 0.025, "#E6B570"))
        
        earth = Planet("Земля", 140, 10, 0.015, "#2196F3")
        earth.add_moon("Луна", 18, 3, 0.08, "#BDBDBD")
        self.planets.append(earth)
        
        mars = Planet("Марс", 190, 8, 0.01, "#FF5722")
        mars.add_moon("Фобос", 14, 2, 0.07, "#795548")
        mars.add_moon("Деймос", 20, 1.5, 0.05, "#9E9E9E")
        self.planets.append(mars)
        
        jupiter = Planet("Юпитер", 280, 18, 0.005, "#FFCC80")
        jupiter.add_moon("Ио", 26, 3.5, 0.04, "#E0F7FA")
        self.planets.append(jupiter)

    def _init_asteroid_belt(self) -> None:
        # Генерируем 150 астероидов на орбитах между Марсом и Юпитером
        for i in range(150):
            dist = random.uniform(220, 250)
            speed = random.uniform(0.006, 0.009)
            radius = random.uniform(1, 2.5)
            self.asteroids.append(CelestialBody(f"Астероид_{i}", dist, radius, speed, "#757575"))

    def update(self, time_scale: float) -> None:
        # Обновляем координаты всего, что движется
        for planet in self.planets:
            planet.update_all_positions(self.sun_x, self.sun_y, time_scale)
        for asteroid in self.asteroids:
            asteroid.update_position(self.sun_x, self.sun_y, time_scale)