import tkinter as tk
from src.models.animation_model import SolarSystemModel

class Renderer:
    # Класс для отрисовки графики на холсте Canvas.
    def __init__(self, canvas: tk.Canvas, model: SolarSystemModel):
        self.canvas = canvas
        self.model = model

    def draw_background_effect(self, trail_intensity: float) -> None:
        # Если слайдер шлейфа на максимуме — полностью стираем холст каждый кадр
        if trail_intensity >= 0.95:
            self.canvas.delete("all")
            self._draw_sun()
        else:
            # Иначе стираем только динамические объекты, оставляя старый след (эффект хвоста)
            self.canvas.delete("dynamic")

    def _draw_sun(self) -> None:
        # Рисуем статичное Солнце по центру
        mx, my = self.model.sun_x, self.model.sun_y
        r = self.model.sun_radius
        self.canvas.create_oval(mx - r, my - r, mx + r, my + r, fill="#FFD54F", outline="#FF9800", tags="sun")

    def render_system(self, show_orbits: bool, trail_intensity: float) -> None:
        self.draw_background_effect(trail_intensity)

        # Отрисовка серых колец орбит (если чекбокс включен)
        if show_orbits:
            for planet in self.model.planets:
                mx, my = self.model.sun_x, self.model.sun_y
                self.canvas.create_oval(
                    mx - planet.distance, my - planet.distance,
                    mx + planet.distance, my + planet.distance,
                    outline="#232328", tags="dynamic"
                )

        # Рисуем все астероиды
        for ast in self.model.asteroids:
            self.canvas.create_oval(ast.x - ast.radius, ast.y - ast.radius, ast.x + ast.radius, ast.y + ast.radius, fill=ast.color, outline="", tags="dynamic")

        # Рисуем планеты и их спутники
        for planet in self.model.planets:
            self.canvas.create_oval(planet.x - planet.radius, planet.y - planet.radius, planet.x + planet.radius, planet.y + planet.radius, fill=planet.color, outline="#FFFFFF", tags="dynamic")
            for moon in planet.moons:
                self.canvas.create_oval(moon.x - moon.radius, moon.y - moon.radius, moon.x + moon.radius, moon.y + moon.radius, fill=moon.color, outline="", tags="dynamic")