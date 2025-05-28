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
        }

        # Ссылки на виджеты
        self.buttons = {}

        # Создаём ABXY
        self.create_buttons()


        # Аналоговые оси и триггеры
        self.left_stick_x = 0
        self.left_stick_y = 0
        self.right_stick_x = 0
        self.right_stick_y = 0
        self.left_trigger = 0
        self.right_trigger = 0

        self.create_widgets()
        self.update_loop()

    def create_buttons(self):
        container = tk.Frame(self.root)
        container.pack(pady=10, padx=10)

        # Левая часть: бампер и дпад
        left_frame = tk.Frame(container)
        left_frame.grid(row=0, column=0, sticky="n")

        # Левый бампер над дпадом
        lb_frame = tk.Frame(left_frame)
        lb_frame.pack()
        lb_label = tk.Label(lb_frame, text="LB", width=6, height=2, relief='raised', bg='lightgray')
        lb_label.pack(pady=(0, 5))
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
            lbl.grid(row=r, column=c, padx=3, pady=3)
            lbl.bind("<Button-1>", lambda e, n=name: self.press_button(n))
            lbl.bind("<ButtonRelease-1>", lambda e, n=name: self.release_button(n))
            lbl.bind("<Button-3>", lambda e, n=name: self.toggle_button_rclck(n))
            self.buttons[name] = lbl


        # Правая часть: бампер и ABXY
        right_frame = tk.Frame(container)
        right_frame.grid(row=0, column=1, sticky="n", padx=30)

        # Правый бампер над ABXY
        rb_frame = tk.Frame(right_frame)
        rb_frame.pack()
        rb_label = tk.Label(rb_frame, text="RB", width=6, height=2, relief='raised', bg='lightgray')
        rb_label.pack(pady=(0, 5))
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
            lbl.grid(row=r, column=c, padx=3, pady=3)
            lbl.bind("<Button-1>", lambda e, n=name: self.press_button(n))
            lbl.bind("<ButtonRelease-1>", lambda e, n=name: self.release_button(n))
            lbl.bind("<Button-3>", lambda e, n=name: self.toggle_button_rclck(n))
            self.buttons[name] = lbl


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

        # Левая сторона: LT + LB
        frame_left_top = ttk.Frame(frame_top)
        frame_left_top.pack(side=tk.LEFT, padx=10)

        ttk.Label(frame_left_top, text="LT").pack()
        self.slider_lt = ttk.Scale(frame_left_top, from_=0, to=255, orient=tk.HORIZONTAL,
                                   command=self.on_left_trigger, length=100)
        self.slider_lt.pack()

        self.btn_lb = ttk.Checkbutton(frame_left_top, text="LB",
                                      command=lambda: self.toggle_button("LB"))
        self.btn_lb.pack()

        # Правая сторона: RT + RB
        frame_right_top = ttk.Frame(frame_top)
        frame_right_top.pack(side=tk.RIGHT, padx=10)

        ttk.Label(frame_right_top, text="RT").pack()
        self.slider_rt = ttk.Scale(frame_right_top, from_=0, to=255, orient=tk.HORIZONTAL,
                                   command=self.on_right_trigger, length=100)
        self.slider_rt.pack()

        self.btn_rb = ttk.Checkbutton(frame_right_top, text="RB",
                                      command=lambda: self.toggle_button("RB"))
        self.btn_rb.pack()

        # Основной фрейм для кнопок
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(padx=10, pady=5, fill=tk.X)

        # Слева D-Pad
        frame_dpad = ttk.Frame(frame_buttons)
        frame_dpad.pack(side=tk.LEFT, padx=20)
        ttk.Label(frame_dpad, text="D-Pad").pack()

        dpad_frame = ttk.Frame(frame_dpad)
        dpad_frame.pack()

        btn_up = ttk.Checkbutton(dpad_frame, text="Up",
                                 command=lambda: self.toggle_button("DPAD_UP"))
        btn_up.grid(row=0, column=1)

        btn_left = ttk.Checkbutton(dpad_frame, text="Left",
                                   command=lambda: self.toggle_button("DPAD_LEFT"))
        btn_left.grid(row=1, column=0)

        btn_right = ttk.Checkbutton(dpad_frame, text="Right",
                                    command=lambda: self.toggle_button("DPAD_RIGHT"))
        btn_right.grid(row=1, column=2)

        btn_down = ttk.Checkbutton(dpad_frame, text="Down",
                                  command=lambda: self.toggle_button("DPAD_DOWN"))
        btn_down.grid(row=2, column=1)

        # Справа ромб из A, B, X, Y
        frame_abxy = ttk.Frame(frame_buttons)
        frame_abxy.pack(side=tk.RIGHT, padx=20)

        ttk.Label(frame_abxy, text="Buttons").grid(row=0, column=1)

        btn_y = ttk.Checkbutton(frame_abxy, text="Y",
                                command=lambda: self.toggle_button("Y"))
        btn_y.grid(row=1, column=1)

        btn_x = ttk.Checkbutton(frame_abxy, text="X",
                                command=lambda: self.toggle_button("X"))
        btn_x.grid(row=2, column=0)


        btn_a = ttk.Label(frame_abxy, text="A", relief="raised", width=3, anchor="center")
        btn_a.grid(row=2, column=2, padx=5, pady=5)

        self.a_toggled = False

        def update_a_visual(state):
            if state:
                btn_a.config(relief="sunken")
            else:
                btn_a.config(relief="raised")

        def on_a_press(event):
            self.buttons_state["A"] = True
            if not self.a_toggled:
                update_a_visual(True)

        def on_a_release(event):
            if not self.a_toggled:
                self.buttons_state["A"] = False
                update_a_visual(False)

        def on_a_toggle(event):
            self.a_toggled = not self.a_toggled
            self.buttons_state["A"] = self.a_toggled
            update_a_visual(self.a_toggled)

        btn_a.bind("<ButtonPress-1>", on_a_press)
        btn_a.bind("<ButtonRelease-1>", on_a_release)
        btn_a.bind("<Button-3>", on_a_toggle)




        btn_b = ttk.Checkbutton(frame_abxy, text="B",
                                command=lambda: self.toggle_button("B"))
        btn_b.grid(row=3, column=1)


        
        # Контейнер для стиков: левый и правый
        frame_sticks = ttk.Frame(self.root)
        frame_sticks.pack(padx=10, pady=5, fill=tk.X)

        # Левый стик
        self.frame_left_stick = ttk.Frame(frame_sticks)
        self.frame_left_stick.pack(side=tk.LEFT, padx=10)

        ttk.Label(self.frame_left_stick, text="Left Stick X").pack()
        self.slider_left_x = ttk.Scale(self.frame_left_stick, from_=-1.0, to=1.0, orient=tk.HORIZONTAL,
                                       command=self.on_left_stick_x, length=150)
        self.slider_left_x.pack()

        self.frame_left_y = ttk.Frame(self.frame_left_stick)
        self.frame_left_y.pack()
        ttk.Label(self.frame_left_y, text="Y").pack()
        self.slider_left_y = ttk.Scale(self.frame_left_y, from_=-1.0, to=1.0, orient=tk.VERTICAL,
                                       command=self.on_left_stick_y, length=100)
        self.slider_left_y.pack()

        # Размеры и параметры площадки левого стика
        self.left_stick_size = 150
        self.left_stick_padding = 5
        self.left_stick_dot_radius = 4
        self.left_cx = self.left_cy = self.left_stick_size / 2
        self.left_radius = (self.left_stick_size - 2 * self.left_stick_padding) / 2

        # Canvas для левого стика
        self.canvas_left = tk.Canvas(self.frame_left_stick, width=self.left_stick_size, height=self.left_stick_size, bg='gray85')
        self.canvas_left.pack()

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




        # Правый стик
        frame_right_stick = ttk.Frame(frame_sticks)
        frame_right_stick.pack(side=tk.RIGHT, padx=10)

        ttk.Label(frame_right_stick, text="Right Stick X").pack()
        self.slider_right_x = ttk.Scale(frame_right_stick, from_=-1.0, to=1.0, orient=tk.HORIZONTAL,
                                        command=self.on_right_stick_x, length=150)
        self.slider_right_x.pack()

        frame_right_y = ttk.Frame(frame_right_stick)
        frame_right_y.pack()
        ttk.Label(frame_right_y, text="Y").pack()
        self.slider_right_y = ttk.Scale(frame_right_y, from_=-1.0, to=1.0, orient=tk.VERTICAL,
                                        command=self.on_right_stick_y, length=100)
        self.slider_right_y.pack()

        # Canvas для правого стика
        self.right_stick_size = 150
        self.right_stick_padding = 5
        self.right_stick_canvas = tk.Canvas(frame_right_stick, width=self.right_stick_size, height=self.right_stick_size, bg='gray85')
        self.right_stick_canvas.pack(pady=5)
        self.right_stick_dot_radius = 4

        # Центр и радиус площадки
        self.right_cx = self.right_cy = self.right_stick_size / 2
        self.right_radius = (self.right_stick_size - 2 * self.right_stick_padding) / 2

        # Нарисуем площадку и точку центра
        self.right_stick_canvas.create_oval(
            self.right_stick_padding, self.right_stick_padding,
            self.right_stick_size - self.right_stick_padding,
            self.right_stick_size - self.right_stick_padding,
            outline="black", width=2)

        self.right_center_dot = self.right_stick_canvas.create_oval(
            self.right_cx - 3, self.right_cy - 3,
            self.right_cx + 3, self.right_cy + 3,
            fill="black")

        # Точка стика
        self.right_stick_dot = self.right_stick_canvas.create_oval(
            self.right_cx - self.right_stick_dot_radius,
            self.right_cy - self.right_stick_dot_radius,
            self.right_cx + self.right_stick_dot_radius,
            self.right_cy + self.right_stick_dot_radius,
            fill="red")

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


    def toggle_button(self, name):
        self.buttons_state[name] = not self.buttons_state[name]


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
