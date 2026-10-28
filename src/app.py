import tkinter as tk
from tkinter import ttk
from src.models.animation_model import SolarSystemModel
from src.renderers.renderer import Renderer

class App:
    # Главный класс приложения: окна, кнопки, слайдеры и цикл анимации.
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Солнечная система")
        self.root.geometry("1000x750")
        self.root.resizable(False, False)

        self.is_paused = False
        self.time_scale = 1.0
        self.trail_intensity = 1.0
        self.show_orbits_var = tk.BooleanVar(value=True)

        self.model = SolarSystemModel(750, 750)
        self._setup_ui()
        self.renderer = Renderer(self.canvas, self.model)

        # Горячие клавиши (Пробел — пауза, R — сброс)
        self.root.bind("<space>", self._toggle_pause)
        self.root.bind("<r>", self._reset_simulation)
        self.root.bind("<R>", self._reset_simulation)

        self._animate()

    def _setup_ui(self) -> None:
        # Создаем темный холст для космоса слева
        self.canvas = tk.Canvas(self.root, width=750, height=750, bg="#05050A")
        self.canvas.grid(row=0, column=0)

        # Создаем боковую панель управления справа
        control_frame = ttk.Frame(self.root, padding=15)
        control_frame.grid(row=0, column=1, sticky="ns")

        ttk.Label(control_frame, text="Скорость времени:").pack(anchor="w")
        ttk.Scale(control_frame, from_=0.0, to_=3.0, value=1.0, command=lambda v: setattr(self, 'time_scale', float(v))).pack(fill="x", pady=10)

        ttk.Label(control_frame, text="Эффект шлейфа:").pack(anchor="w")
        ttk.Scale(control_frame, from_=0.1, to_=1.0, value=1.0, command=lambda v: setattr(self, 'trail_intensity', float(v))).pack(fill="x", pady=10)

        ttk.Checkbutton(control_frame, text="Показывать орбиты", variable=self.show_orbits_var).pack(anchor="w", pady=10)
        ttk.Label(control_frame, text="[Space] — Пауза\n[R] — Перемешать углы", foreground="gray").pack(side="bottom")

    def _toggle_pause(self, event=None) -> None:
        self.is_paused = not self.is_paused

    def _reset_simulation(self, event=None) -> None:
        import random
        # Перемешиваем углы у всех планет
        for p in self.model.planets:
            p.angle = random.uniform(0, 6.28)
            # Перемешиваем углы и у их спутников
            for moon in p.moons:
                moon.angle = random.uniform(0, 6.28)
                
        # Перемешиваем углы у всех астероидов
        for ast in self.model.asteroids:
            ast.angle = random.uniform(0, 6.28)

        self.model.update(0)
        
        self.renderer.render_system(self.show_orbits_var.get(), self.trail_intensity)


    def _animate(self) -> None:
        # Если паузы нет — пересчитываем математику шага
        if not self.is_paused:
            self.model.update(self.time_scale)

        # Перерисовываем систему графически
        self.renderer.render_system(self.show_orbits_var.get(), self.trail_intensity)

        # Рекурсивный вызов этого же метода каждые 16 миллисекунд (целевые 60 FPS)
        self.root.after(16, self._animate)

    def run(self) -> None:
        self.root.mainloop()