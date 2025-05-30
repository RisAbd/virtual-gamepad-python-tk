import tkinter as tk
from tkinter import ttk
import vgamepad

class VirtualGamepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Virtual Gamepad (tkinter)")

        self.gamepad = vgamepad.VX360Gamepad()

        # Состояния кнопок
        self.buttons_state = {
            "A": False,
            "B": False,
            "X": False,
            "Y": False,
            "DPAD_UP": False,
            "DPAD_DOWN": False,
            "DPAD_LEFT": False,
            "DPAD_RIGHT": False,
            "LB": False,
            "RB": False,
            "L3": False,
            "R3": False,
            "START": False,
            "BACK": False,
            "GUIDE": False,
        }

        # Ссылки на виджеты
        self.buttons = {}

        # Аналоговые оси и триггеры
        self.left_stick_x = 0
        self.left_stick_y = 0
        self.right_stick_x = 0
        self.right_stick_y = 0
        self.left_trigger = 0
        self.right_trigger = 0

        self.create_widgets()
        self.update_loop()

    def press_button(self, name):
        self.buttons_state[name] = True
        self.update_button_visual(name)
        print(f"Pressed {name} -> {self.buttons_state[name]}")

    def release_button(self, name):
        self.buttons_state[name] = False
        self.update_button_visual(name)
        print(f"Released {name} -> {self.buttons_state[name]}")

    def toggle_button_rclck(self, name):
        self.buttons_state[name] = not self.buttons_state[name]
        self.update_button_visual(name)
        print(f"Toggled {name} -> {self.buttons_state[name]}")

    def update_button_visual(self, name):
        state = self.buttons_state[name]
        self.buttons[name].config(
            relief='sunken' if state else 'raised',
            bg='lightgreen' if state else 'lightgray'
        )


    def create_widgets(self):

        # Верхняя панель: Триггеры и Бамперы
        frame_top = ttk.Frame(self.root)
        frame_top.pack(padx=10, pady=5, fill=tk.X)

        # Левая сторона: LT
        frame_left_top = ttk.Frame(frame_top)
        frame_left_top.pack(side=tk.LEFT, padx=10)

        ttk.Label(frame_left_top, text="LT").pack()
        self.slider_lt = ttk.Scale(frame_left_top, from_=-1.0, to=1.0, orient=tk.HORIZONTAL,
                                   command=self.on_left_trigger, length=100)
        self.slider_lt.pack()

        # Правая сторона: RT
        frame_right_top = ttk.Frame(frame_top)
        frame_right_top.pack(side=tk.RIGHT, padx=10)

        ttk.Label(frame_right_top, text="RT").pack()
        self.slider_rt = ttk.Scale(frame_right_top, from_=-1.0, to=1.0, orient=tk.HORIZONTAL,
                                   command=self.on_right_trigger, length=100)
        self.slider_rt.pack()


        # BUTTONS
        container = tk.Frame(self.root)
        container.pack(pady=10, padx=10)

        # Левая часть: бампер и дпад
        left_frame = tk.Frame(container)
        left_frame.grid(row=0, column=0, sticky="n")

        # Правая часть: бампер и ABXY
        right_frame = tk.Frame(container)
        right_frame.grid(row=0, column=2, sticky="n", padx=10)

        # Центр: кнопки START, BACK, GUIDE
        center_frame = tk.Frame(container)
        center_frame.grid(row=0, column=1, sticky="n", padx=10, pady=30)

        # Рамка для Start и Back в ряд
        top_buttons_frame = tk.Frame(center_frame)
        top_buttons_frame.pack(pady=1)  # небольшой отступ сверху

        for name in ["BACK", "START"]:
            lbl = tk.Label(top_buttons_frame, text=name, width=5, height=1, relief='raised', bg='lightgray')
            lbl.pack(side=tk.LEFT, padx=3)
            lbl.bind("<Button-1>", lambda e, n=name: self.press_button(n))
            lbl.bind("<ButtonRelease-1>", lambda e, n=name: self.release_button(n))
            lbl.bind("<Button-3>", lambda e, n=name: self.toggle_button_rclck(n))
            self.buttons[name] = lbl

        # Создаем еще один фрейм для GUIDE, чтобы его отобразить снизу и с теми же размерами и отступами
        guide_frame = tk.Frame(center_frame)
        guide_frame.pack(pady=(10, 3))  # сверху 10 пикселей, снизу 3 пикселя


        lbl_guide = tk.Label(guide_frame, text="GUIDE", width=5, height=2, relief='raised', bg='lightgray')
        lbl_guide.pack(padx=3, pady=3)
        lbl_guide.bind("<Button-1>", lambda e, n="GUIDE": self.press_button(n))
        lbl_guide.bind("<ButtonRelease-1>", lambda e, n="GUIDE": self.release_button(n))
        lbl_guide.bind("<Button-3>", lambda e, n="GUIDE": self.toggle_button_rclck(n))
        self.buttons["GUIDE"] = lbl_guide



        # Левый бампер над дпадом
        lb_frame = tk.Frame(left_frame)
        lb_frame.pack()
        lb_label = tk.Label(lb_frame, text="LB", width=6, height=2, relief='raised', bg='lightgray')
        lb_label.pack(pady=(0, 3))
        lb_label.bind("<Button-1>", lambda e, n="LB": self.press_button(n))
        lb_label.bind("<ButtonRelease-1>", lambda e, n="LB": self.release_button(n))
        lb_label.bind("<Button-3>", lambda e, n="LB": self.toggle_button_rclck(n))
        self.buttons["LB"] = lb_label

        # D-Pad — крестовина из 4 кнопок (UP сверху, LEFT слева, RIGHT справа, DOWN снизу)
        dpad_frame = tk.Frame(left_frame)
        dpad_frame.pack()

        dpad_layout = [
            ('DPAD_UP', 0, 1),
            ('DPAD_LEFT', 1, 0),
            ('DPAD_RIGHT', 1, 2),
            ('DPAD_DOWN', 2, 1),
        ]

        for name, r, c in dpad_layout:
            lbl = tk.Label(dpad_frame, text=name[5:], width=4, height=2, relief='raised', bg='lightgray')
            lbl.grid(row=r, column=c, padx=3, pady=1)
            lbl.bind("<Button-1>", lambda e, n=name: self.press_button(n))
            lbl.bind("<ButtonRelease-1>", lambda e, n=name: self.release_button(n))
            lbl.bind("<Button-3>", lambda e, n=name: self.toggle_button_rclck(n))
            self.buttons[name] = lbl


        # Правый бампер над ABXY
        rb_frame = tk.Frame(right_frame)
        rb_frame.pack()
        rb_label = tk.Label(rb_frame, text="RB", width=6, height=2, relief='raised', bg='lightgray')
        rb_label.pack(pady=(0, 3))
        rb_label.bind("<Button-1>", lambda e, n="RB": self.press_button(n))
        rb_label.bind("<ButtonRelease-1>", lambda e, n="RB": self.release_button(n))
        rb_label.bind("<Button-3>", lambda e, n="RB": self.toggle_button_rclck(n))
        self.buttons["RB"] = rb_label

        # ABXY — крестовина из 4 кнопок (Y сверху, X слева, B справа, A снизу)
        abxy_frame = tk.Frame(right_frame)
        abxy_frame.pack()

        abxy_layout = [
            ('Y', 0, 1),
            ('X', 1, 0),
            ('B', 1, 2),
            ('A', 2, 1),
        ]

        for name, r, c in abxy_layout:
            lbl = tk.Label(abxy_frame, text=name, width=4, height=2, relief='raised', bg='lightgray')
            lbl.grid(row=r, column=c, padx=3, pady=1)
            lbl.bind("<Button-1>", lambda e, n=name: self.press_button(n))
            lbl.bind("<ButtonRelease-1>", lambda e, n=name: self.release_button(n))
            lbl.bind("<Button-3>", lambda e, n=name: self.toggle_button_rclck(n))
            self.buttons[name] = lbl



        # sticks

        frame_sticks = ttk.Frame(self.root)
        frame_sticks.pack(padx=10, pady=5, fill=tk.X)


        # Левый стик
        self.frame_left_stick = ttk.Frame(frame_sticks)
        self.frame_left_stick.pack(side=tk.LEFT, padx=10)

        # L3 — кнопка в точке пересечения слайдеров
        lbl_l3 = tk.Label(self.frame_left_stick, text="L3", width=4, height=2,
                          relief='raised', bg='lightgray')
        lbl_l3.grid(row=1, column=0, padx=5, pady=5)
        lbl_l3.bind("<Button-1>", lambda e, n="L3": self.press_button(n))
        lbl_l3.bind("<ButtonRelease-1>", lambda e, n="L3": self.release_button(n))
        lbl_l3.bind("<Button-3>", lambda e, n="L3": self.toggle_button_rclck(n))
        self.buttons["L3"] = lbl_l3

        # Используем .grid() вместо .pack()
        # Горизонтальный слайдер — сверху, по центру
        self.slider_left_x = ttk.Scale(self.frame_left_stick, from_=-1.0, to=1.0,
                                       orient=tk.HORIZONTAL, command=self.on_left_stick_x, length=150)
        self.slider_left_x.grid(row=1, column=1)

        # Вертикальный слайдер — слева от площадки
        self.slider_left_y = ttk.Scale(self.frame_left_stick, from_=-1.0, to=1.0,
                                       orient=tk.VERTICAL, command=self.on_left_stick_y, length=150)
        self.slider_left_y.grid(row=3, column=0, padx=(0, 5))

        # Площадка стика — по центру
        self.left_stick_size = 150
        self.left_stick_padding = 5
        self.left_stick_dot_radius = 4
        self.left_cx = self.left_cy = self.left_stick_size / 2
        self.left_radius = (self.left_stick_size - 2 * self.left_stick_padding) / 2

        self.canvas_left = tk.Canvas(self.frame_left_stick, width=self.left_stick_size,
                                     height=self.left_stick_size, bg='gray85')
        self.canvas_left.grid(row=3, column=1, padx=5, pady=5)

        # Нарисуем круг площадки с паддингом
        self.canvas_left.create_oval(
            self.left_stick_padding, self.left_stick_padding,
            self.left_stick_size - self.left_stick_padding,
            self.left_stick_size - self.left_stick_padding,
            outline="black", width=2)

        # Центр — маленькая точка радиусом 3 пикселя
        center_dot_radius = 3
        self.canvas_left.create_oval(
            self.left_cx - center_dot_radius, self.left_cy - center_dot_radius,
            self.left_cx + center_dot_radius, self.left_cy + center_dot_radius,
            fill="black")

        # Точка стика (красная)
        r = self.left_stick_dot_radius
        self.left_stick_dot = self.canvas_left.create_oval(
            self.left_cx - r, self.left_cy - r,
            self.left_cx + r, self.left_cy + r,
            fill="red")

        # Привязка событий
        self.canvas_left.bind("<B1-Motion>", self.on_left_canvas_drag)
        self.canvas_left.bind("<Button-1>", self.on_left_canvas_drag)



        # Правый стик: компоновка с гридом
        self.frame_right_stick = ttk.Frame(frame_sticks)
        self.frame_right_stick.pack(side=tk.RIGHT, padx=10)

        frame_r_stick_grid = tk.Frame(self.frame_right_stick)
        frame_r_stick_grid.pack()

        # Кнопка R3 (в углу)
        r3_btn = tk.Label(frame_r_stick_grid, text="R3", width=4, height=2, relief='raised', bg='lightgray')
        r3_btn.grid(row=0, column=0, padx=2, pady=2)
        r3_btn.bind("<Button-1>", lambda e, n="R3": self.press_button(n))
        r3_btn.bind("<ButtonRelease-1>", lambda e, n="R3": self.release_button(n))
        r3_btn.bind("<Button-3>", lambda e, n="R3": self.toggle_button_rclck(n))
        self.buttons["R3"] = r3_btn

        # Горизонтальный слайдер (X)
        self.slider_right_x = ttk.Scale(frame_r_stick_grid, from_=-1.0, to=1.0, orient=tk.HORIZONTAL,
                                        command=self.on_right_stick_x, length=150)
        self.slider_right_x.grid(row=0, column=1, padx=2, pady=2)

        # Вертикальный слайдер (Y)
        self.slider_right_y = ttk.Scale(frame_r_stick_grid, from_=-1.0, to=1.0, orient=tk.VERTICAL,
                                        command=self.on_right_stick_y, length=150)
        self.slider_right_y.grid(row=1, column=0, padx=2, pady=2)

        # Площадка стика (Canvas)
        self.right_stick_size = 150
        self.right_stick_padding = 5
        self.right_stick_dot_radius = 4
        self.right_cx = self.right_cy = self.right_stick_size / 2
        self.right_radius = (self.right_stick_size - 2 * self.right_stick_padding) / 2

        self.right_stick_canvas = tk.Canvas(frame_r_stick_grid, width=self.right_stick_size, height=self.right_stick_size, bg='gray85')
        self.right_stick_canvas.grid(row=1, column=1, padx=5, pady=5)

        # Круг площадки
        self.right_stick_canvas.create_oval(
            self.right_stick_padding, self.right_stick_padding,
            self.right_stick_size - self.right_stick_padding,
            self.right_stick_size - self.right_stick_padding,
            outline="black", width=2)

        # Центр и точка
        self.right_stick_canvas.create_oval(
            self.right_cx - 3, self.right_cy - 3,
            self.right_cx + 3, self.right_cy + 3,
            fill="black")

        self.right_stick_dot = self.right_stick_canvas.create_oval(
            self.right_cx - self.right_stick_dot_radius,
            self.right_cy - self.right_stick_dot_radius,
            self.right_cx + self.right_stick_dot_radius,
            self.right_cy + self.right_stick_dot_radius,
            fill="red")

        # Привязка событий
        self.right_stick_canvas.bind("<B1-Motion>", self.on_right_canvas_drag)
        self.right_stick_canvas.bind("<Button-1>", self.on_right_canvas_drag)



    def on_left_canvas_drag(self, event):
        dx = event.x - self.left_cx
        dy = event.y - self.left_cy
        norm_x = dx / self.left_radius
        norm_y = dy / self.left_radius
        length = (norm_x ** 2 + norm_y ** 2) ** 0.5
        if length > 1:
            norm_x /= length
            norm_y /= length

        self.left_stick_x = norm_x
        self.left_stick_y = norm_y

        self.slider_left_x.set(norm_x)
        self.slider_left_y.set(norm_y)

        self.update_left_stick_dot()


    def update_left_stick_dot(self):
        x = self.left_cx + self.left_stick_x * self.left_radius
        y = self.left_cy + self.left_stick_y * self.left_radius

        r = self.left_stick_dot_radius
        self.canvas_left.coords(self.left_stick_dot,
                               x - r, y - r,
                               x + r, y + r)


    def on_left_stick_x(self, val):
        self.left_stick_x = float(val)
        self.update_left_stick_dot()

    def on_left_stick_y(self, val):
        self.left_stick_y = float(val)
        self.update_left_stick_dot()



    def on_right_canvas_drag(self, event):
        # Конвертируем координаты курсора в нормализованные [-1..1]
        dx = event.x - self.right_cx
        dy = event.y - self.right_cy
        norm_x = dx / self.right_radius
        norm_y = dy / self.right_radius
        # Ограничение по радиусу (окружность)
        length = (norm_x ** 2 + norm_y ** 2) ** 0.5
        if length > 1:
            norm_x /= length
            norm_y /= length

        # Инвертируем Y если надо (в зависимости от логики)
        self.right_stick_x = norm_x
        self.right_stick_y = norm_y

        # Обновляем слайдеры
        self.slider_right_x.set(norm_x)
        self.slider_right_y.set(norm_y)

        # Обновляем позицию точки
        self.update_right_stick_dot()


    def update_right_stick_dot(self):
        x = self.right_cx + self.right_stick_x * self.right_radius
        y = self.right_cy + self.right_stick_y * self.right_radius

        r = self.right_stick_dot_radius
        self.right_stick_canvas.coords(self.right_stick_dot,
                                      x - r, y - r,
                                      x + r, y + r)


    # Также обнови обработчики слайдеров, чтобы они меняли dot:

    def on_right_stick_x(self, val):
        self.right_stick_x = float(val)
        self.update_right_stick_dot()

    def on_right_stick_y(self, val):
        self.right_stick_y = float(val)
        self.update_right_stick_dot()


    def on_left_trigger(self, val):
        self.left_trigger = float(val)

    def on_right_trigger(self, val):
        self.right_trigger = float(val)

    def update_loop(self):
        # Обработка кнопок A,B,X,Y
        if self.buttons_state["A"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)

        if self.buttons_state["B"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B)

        if self.buttons_state["X"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X)

        if self.buttons_state["Y"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y)

        # D-Pad
        if self.buttons_state["DPAD_UP"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)

        if self.buttons_state["DPAD_DOWN"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)

        if self.buttons_state["DPAD_LEFT"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)

        if self.buttons_state["DPAD_RIGHT"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

        if self.buttons_state["LB"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

        if self.buttons_state["RB"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

        if self.buttons_state["L3"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)

        if self.buttons_state["R3"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

        if self.buttons_state["START"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START)

        if self.buttons_state["BACK"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

        if self.buttons_state["GUIDE"]:
            self.gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
        else:
            self.gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)



        # Аналоговые стики
        self.gamepad.left_joystick_float(x_value_float=self.left_stick_x, y_value_float=self.left_stick_y)
        self.gamepad.right_joystick_float(x_value_float=self.right_stick_x, y_value_float=self.right_stick_y)

        # Триггеры
        self.gamepad.left_trigger_float(value_float=self.left_trigger)
        self.gamepad.right_trigger_float(value_float=self.right_trigger)

        self.gamepad.update()

        self.root.after(20, self.update_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualGamepadApp(root)
    root.mainloop()
