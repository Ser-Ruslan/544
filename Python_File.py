import tkinter as tk
from tkinter import ttk, messagebox, font
import math
import random

class SemanticNetworkEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор семантической сети")
        self.root.geometry("1200x800")

        # Основные структуры
        self.nodes = {}
        self.relations = []

        # Отрисовка и поведение
        self.node_radius = 60
        self.canvas_width = 1000
        self.canvas_height = 600

        # Трекеры canvas item -> name
        self.node_items = {}   # oval id -> node name
        self.text_items = {}   # text id -> node name
        self.edge_items = []   # список словарей с id элементов ребра и меткой
        self.dragging_node = None
        self.drag_offset = (0, 0)

        # Масштабирование / панорамирование
        self.scale = 1.0
        self.pan_start = None

        # Выделенные узлы (по клику)
        self.selected_nodes = set()

        self.load_example_network()
        self.create_widgets()
        self.update_comboboxes()
        self.draw_network()

    def load_example_network(self):
        """Загрузка примера семантической сети"""
        self.nodes = {
            "птица": {"type": "class", "x": 450, "y": 100},
            "животные": {"type": "class", "x": 450, "y": 40},
            "страус": {"type": "object", "x": 200, "y": 220},
            "канарейка": {"type": "object", "x": 400, "y": 220},
            "дрозд": {"type": "object", "x": 600, "y": 220},
            "пингвин": {"type": "object", "x": 800, "y": 220},
            "летать": {"type": "property", "x": 700, "y": 380},
            "ходить": {"type": "property", "x": 120, "y": 380},
            "петь": {"type": "property", "x": 500, "y": 360},
            "оперенье": {"type": "property", "x": 200, "y": 40},
            "желтый": {"type": "property", "x": 300, "y": 520},
            "черный": {"type": "property", "x": 700, "y": 520},
            "коричневый": {"type": "property", "x": 500, "y": 520},
        }

        self.relations = [
            {"from": "страус", "to": "птица", "type": "является"},
            {"from": "канарейка", "to": "птица", "type": "является"},
            {"from": "дрозд", "to": "птица", "type": "является"},
            {"from": "пингвин", "to": "птица", "type": "является"},
            {"from": "птица", "to": "животные", "type": "является"},
            {"from": "страус", "to": "ходить", "type": "умеет"},
            {"from": "птица", "to": "оперенье", "type": "имеет"},
            {"from": "пингвин", "to": "черный", "type": "имеет цвет"},
            {"from": "пингвин", "to": "ходить", "type": "умеет"},
            {"from": "канарейка", "to": "желтый", "type": "имеет цвет"},
            {"from": "дрозд", "to": "коричневый", "type": "имеет цвет"},
            {"from": "дрозд", "to": "петь", "type": "умеет"},
            {"from": "канарейка", "to": "петь", "type": "умеет"},
            {"from": "дрозд", "to": "летать", "type": "умеет"},
            {"from": "канарейка", "to": "летать", "type": "умеет"},
        ]

    def create_widgets(self):
        # Фреймы
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(top_frame, bg="#fafafa", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(top_frame, width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=6, pady=6)

        # Контролы справа
        controls = tk.LabelFrame(right_frame, text="Управление", padx=5, pady=5)
        controls.pack(fill=tk.X, pady=6)

        tk.Label(controls, text="Имя узла:").grid(row=0, column=0, sticky="w")
        self.node_name = tk.Entry(controls, width=20)
        self.node_name.grid(row=0, column=1, pady=4)

        tk.Label(controls, text="Тип:").grid(row=1, column=0, sticky="w")
        self.node_type = ttk.Combobox(controls, values=["класс", "объект", "свойство"], width=12, state="readonly")
        self.node_type.grid(row=1, column=1, pady=4)
        self.node_type.set("объект")

        tk.Button(controls, text="Добавить узел", command=self.add_node).grid(row=2, column=0, columnspan=2, pady=6, sticky="we")

        rel_frame = tk.LabelFrame(right_frame, text="Добавить связь", padx=5, pady=5)
        rel_frame.pack(fill=tk.X, pady=6)

        tk.Label(rel_frame, text="От:").grid(row=0, column=0, sticky="w")
        self.relation_from = ttk.Combobox(rel_frame, values=list(self.nodes.keys()), width=18)
        self.relation_from.grid(row=0, column=1, pady=2)

        tk.Label(rel_frame, text="К:").grid(row=1, column=0, sticky="w")
        self.relation_to = ttk.Combobox(rel_frame, values=list(self.nodes.keys()), width=18)
        self.relation_to.grid(row=1, column=1, pady=2)

        tk.Label(rel_frame, text="Тип:").grid(row=2, column=0, sticky="w")
        self.relation_type = ttk.Combobox(rel_frame, values=["является", "имеет", "умеет", "имеет цвет"], width=12)
        self.relation_type.grid(row=2, column=1, pady=2)
        self.relation_type.set("является")

        tk.Button(rel_frame, text="Добавить связь", command=self.add_relation).grid(row=3, column=0, columnspan=2, pady=6, sticky="we")

        layout_frame = tk.LabelFrame(right_frame, text="Размещение", padx=5, pady=5)
        layout_frame.pack(fill=tk.X, pady=6)
        tk.Button(layout_frame, text="Применить layout", command=self.auto_layout).pack(fill=tk.X, pady=2)
        tk.Button(layout_frame, text="Очистить сеть", command=self.clear_network).pack(fill=tk.X, pady=2)

        legend_frame = tk.LabelFrame(right_frame, text="Легенда", padx=5, pady=5)
        legend_frame.pack(fill=tk.X, pady=6)
        tk.Label(legend_frame, text="Классы — тёмно-голубые").pack(anchor="w")
        tk.Label(legend_frame, text="Объекты — зелёные").pack(anchor="w")
        tk.Label(legend_frame, text="Свойства — жёлтые").pack(anchor="w")

        # Bindings
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<ButtonPress-2>", self.on_middle_press)   # middle (pan)
        self.canvas.bind("<B2-Motion>", self.on_middle_drag)
        self.canvas.bind("<ButtonRelease-2>", self.on_middle_release)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)        # Windows
        self.canvas.bind("<Button-4>", self.on_mousewheel)          # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mousewheel)          # Linux scroll down

        # resize canvas on window resize
        self.root.bind("<Configure>", self.on_root_configure)

        # Fonts
        self.node_font = font.Font(family="Arial", size=10, weight="bold")
        self.edge_font = font.Font(family="Arial", size=9)

    # ----------------- UI event handlers -----------------
    def on_root_configure(self, event):
        # Обновляем внутренние размеры
        try:
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            if w > 50 and h > 50:
                self.canvas_width = w
                self.canvas_height = h
        except Exception:
            pass

    def on_canvas_press(self, event):
        # Определяем, нажали ли на узел (по тегу "node")
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        items = self.canvas.find_overlapping(x, y, x, y)
        for it in items:
            if it in self.node_items:
                name = self.node_items[it]
                node = self.nodes[name]
                self.dragging_node = name
                self.drag_offset = (node["x"] - x, node["y"] - y)
                # поднимаем узел в визуальном стеке
                self.canvas.tag_raise(it)
                # также поднимаем текст
                for t_id, n in self.text_items.items():
                    if n == name:
                        self.canvas.tag_raise(t_id)
                return
        # Если клик по пустому месту — снимаем выделение
        self.dragging_node = None

    def on_canvas_drag(self, event):
        if self.dragging_node:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            new_x = x + self.drag_offset[0]
            new_y = y + self.drag_offset[1]
            # ограничение в пределах холста
            new_x = max(self.node_radius, min(self.canvas_width - self.node_radius, new_x))
            new_y = max(self.node_radius, min(self.canvas_height - self.node_radius, new_y))
            self.nodes[self.dragging_node]["x"] = new_x
            self.nodes[self.dragging_node]["y"] = new_y
            self.draw_network()  # перерисовываем динамически

    def on_canvas_release(self, event):
        self.dragging_node = None

    def on_middle_press(self, event):
        self.pan_start = (event.x, event.y)

    def on_middle_drag(self, event):
        if self.pan_start:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.canvas.move("all", dx, dy)
            # смещаем координаты узлов, чтобы их логика совпадала (простая модель панорамирования)
            for n, data in self.nodes.items():
                data["x"] += dx
                data["y"] += dy
            self.pan_start = (event.x, event.y)

    def on_middle_release(self, event):
        self.pan_start = None

    def on_mousewheel(self, event):
        # Масштабируем всё относительно позиции мыши
        factor = 1.0
        if hasattr(event, 'delta'):
            if event.delta > 0:
                factor = 1.1
            else:
                factor = 0.9
        else:
            # Linux: Button-4 / Button-5
            if event.num == 4:
                factor = 1.1
            else:
                factor = 0.9

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", x, y, factor, factor)
        self.scale *= factor
        # После масштабирования можно скорректировать внутренние координаты узлов:
        for n, data in self.nodes.items():
            data["x"] = x + (data["x"] - x) * factor
            data["y"] = y + (data["y"] - y) * factor

    # ----------------- CRUD -----------------
    def find_free_position(self, center_x, center_y, max_attempts=100):
        """Поиск свободной позиции для нового узла"""
        for attempt in range(max_attempts):
            radius = self.node_radius * (attempt // 10 + 1)
            angle = attempt * 0.6
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            if (x < self.node_radius or x > self.canvas_width - self.node_radius or
                y < self.node_radius or y > self.canvas_height - self.node_radius):
                continue

            collision = False
            for node_name, node_data in self.nodes.items():
                distance = math.sqrt((x - node_data["x"])**2 + (y - node_data["y"])**2)
                if distance < self.node_radius * 2.2:
                    collision = True
                    break

            if not collision:
                return x, y

        return (random.randint(self.node_radius, self.canvas_width - self.node_radius),
                random.randint(self.node_radius, self.canvas_height - self.node_radius))

    def add_node(self):
        name = self.node_name.get().strip()
        node_type = self.node_type.get()

        if not name:
            messagebox.showerror("Ошибка", "Введите имя узла")
            return

        if name in self.nodes:
            messagebox.showerror("Ошибка", "Узел с таким именем уже существует")
            return

        x, y = self.find_free_position(self.canvas_width // 2, self.canvas_height // 2)
        self.nodes[name] = {"type": "class" if node_type == "класс" else ("property" if node_type == "свойство" else "object"),
                            "x": x, "y": y}
        self.update_comboboxes()
        self.draw_network()
        self.node_name.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Узел '{name}' добавлен")

    def add_relation(self):
        from_node = self.relation_from.get()
        to_node = self.relation_to.get()
        relation_type = self.relation_type.get()

        if not from_node or not to_node:
            messagebox.showerror("Ошибка", "Выберите узлы для связи")
            return

        if from_node == to_node:
            messagebox.showerror("Ошибка", "Нельзя создать связь узла с самим собой")
            return

        for relation in self.relations:
            if (relation["from"] == from_node and
                relation["to"] == to_node and
                relation["type"] == relation_type):
                messagebox.showerror("Ошибка", "Такая связь уже существует")
                return

        self.relations.append({"from": from_node, "to": to_node, "type": relation_type})
        self.update_comboboxes()
        self.apply_force_directed_layout()
        self.draw_network()
        messagebox.showinfo("Успех", f"Связь '{relation_type}' добавлена")

    def clear_network(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю сеть?"):
            self.nodes.clear()
            self.relations.clear()
            self.update_comboboxes()
            self.draw_network()

    def update_comboboxes(self):
        nodes_list = list(self.nodes.keys())
        self.relation_from['values'] = nodes_list
        self.relation_to['values'] = nodes_list

    # ----------------- Layout / Physics -----------------
    def auto_layout(self):
        """Простое выравнивание: классы сверху, объекты — в середине, свойства — внизу"""
        classes = [name for name, data in self.nodes.items() if data["type"] == "class"]
        objects = [name for name, data in self.nodes.items() if data["type"] == "object"]
        properties = [name for name, data in self.nodes.items() if data["type"] == "property"]

        if classes:
            class_y = max(60, self.node_radius)
            class_spacing = max(120, self.canvas_width / (len(classes) + 1))
            for i, class_name in enumerate(classes):
                self.nodes[class_name]["x"] = class_spacing * (i + 1)
                self.nodes[class_name]["y"] = class_y

        if objects:
            object_y = max(self.canvas_height // 2, 200)
            object_spacing = max(120, self.canvas_width / (len(objects) + 1))
            for i, object_name in enumerate(objects):
                self.nodes[object_name]["x"] = object_spacing * (i + 1)
                self.nodes[object_name]["y"] = object_y

        if properties:
            property_y = self.canvas_height - max(80, self.node_radius)
            property_spacing = max(120, self.canvas_width / (len(properties) + 1))
            for i, property_name in enumerate(properties):
                self.nodes[property_name]["x"] = property_spacing * (i + 1)
                self.nodes[property_name]["y"] = property_y

        self.apply_force_directed_layout(iterations=40)
        self.draw_network()

    def apply_force_directed_layout(self, iterations=50):
        """Применяет упрощённый алгоритм force-directed (несколько итераций)"""
        for _ in range(iterations):
            moves = {}
            for node1_name, node1_data in self.nodes.items():
                fx, fy = 0.0, 0.0
                # отталкивание
                for node2_name, node2_data in self.nodes.items():
                    if node1_name == node2_name:
                        continue
                    dx = node1_data["x"] - node2_data["x"]
                    dy = node1_data["y"] - node2_data["y"]
                    dist = math.hypot(dx, dy) + 0.01
                    rep = 20000 / (dist * dist)
                    fx += rep * (dx / dist)
                    fy += rep * (dy / dist)

                # притяжение к связанным узлам
                for rel in self.relations:
                    if rel["from"] == node1_name:
                        target = self.nodes[rel["to"]]
                        dx = target["x"] - node1_data["x"]
                        dy = target["y"] - node1_data["y"]
                        fx += 0.1 * dx
                        fy += 0.1 * dy
                    elif rel["to"] == node1_name:
                        target = self.nodes[rel["from"]]
                        dx = target["x"] - node1_data["x"]
                        dy = target["y"] - node1_data["y"]
                        fx += 0.1 * dx
                        fy += 0.1 * dy

                max_move = 10
                move_x = max(-max_move, min(max_move, 0.001 * fx))
                move_y = max(-max_move, min(max_move, 0.001 * fy))

                moves[node1_name] = (move_x, move_y)

            for node_name, (mx, my) in moves.items():
                self.nodes[node_name]["x"] = max(self.node_radius, min(self.canvas_width - self.node_radius, self.nodes[node_name]["x"] + mx))
                self.nodes[node_name]["y"] = max(self.node_radius, min(self.canvas_height - self.node_radius, self.nodes[node_name]["y"] + my))

    # ----------------- Drawing -----------------
    def draw_network(self):
        """Отрисовка сети: сначала ребра, затем узлы (чтобы узлы были поверх)"""
        self.canvas.delete("all")
        self.node_items.clear()
        self.text_items.clear()
        self.edge_items.clear()

        # Рисуем ребра (кривые) — сначала фон (тень)
        for rel in self.relations:
            from_node = self.nodes.get(rel["from"])
            to_node = self.nodes.get(rel["to"])
            if not from_node or not to_node:
                continue

            x1, y1 = from_node["x"], from_node["y"]
            x2, y2 = to_node["x"], to_node["y"]

            # цвет по типу
            color = {"является": "#2b7cff", "имеет": "#1f9e5f", "умеет": "#d74b4b", "имеет цвет": "#6b6b6b"}.get(rel["type"], "#333333")

            # вычислим контрольную точку для кривой (смещение перпендикулярно)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy) + 0.01
            # смещение зависит от длины ребра (чтобы короткие были почти прямыми)
            offset = min(120, 0.25 * dist)
            # перпендикулярный вектор
            px, py = -dy / dist, dx / dist
            cx, cy = mx + px * offset, my + py * offset

            # тень линии (слегка смещённая)
            line_shadow = self.canvas.create_line(x1, y1, cx, cy, x2, y2, smooth=True, width=8, splinesteps=36, fill="#dddddd")
            # основная линия
            line = self.canvas.create_line(x1, y1, cx, cy, x2, y2, smooth=True, width=3, splinesteps=36, fill=color)
            # стрелка (полигон) — вычислим позицию на конце линии
            vx = x2 - cx
            vy = y2 - cy
            vlen = math.hypot(vx, vy) + 0.01
            ux, uy = vx / vlen, vy / vlen
            arrow_base_x = x2 - ux * (self.node_radius * 0.9)
            arrow_base_y = y2 - uy * (self.node_radius * 0.9)
            arrow_size = 10 * max(0.6, self.scale)
            left_x = arrow_base_x - uy * arrow_size
            left_y = arrow_base_y + ux * arrow_size
            right_x = arrow_base_x + uy * arrow_size
            right_y = arrow_base_y - ux * arrow_size
            tip_x = x2 - ux * (self.node_radius * 0.12)
            tip_y = y2 - uy * (self.node_radius * 0.12)

            arrow = self.canvas.create_polygon(left_x, left_y, right_x, right_y, tip_x, tip_y, fill=color, outline=color)

            # надпись по центру кривой чуть ближе к контрольной точке
            label_x = (cx + mx) / 2
            label_y = (cy + my) / 2
            txt = self.canvas.create_text(label_x, label_y, text=rel["type"], font=self.edge_font, fill=color)

            self.edge_items.append({"line": line, "shadow": line_shadow, "arrow": arrow, "text": txt})

        # Рисуем узлы (тень + тело + текст)
        for name, node in self.nodes.items():
            x, y = node["x"], node["y"]
            t = node["type"]

            # Цвета по типу
            if t == "class":
                fill = "#bfe9ff"
                outline = "#2b7cff"
            elif t == "object":
                fill = "#c9f0d1"
                outline = "#2a9d4a"
            else:  # property
                fill = "#fff2b2"
                outline = "#caa10c"

            # Если выделен — меняем визуал (толще и другой цвет контура)
            if name in self.selected_nodes:
                outline_display = "#ff8c00"
                outline_width = 4
            else:
                outline_display = outline
                outline_width = 2

            # Тень (смещённая эллипс)
            shadow = self.canvas.create_oval(x - self.node_radius + 6, y - (self.node_radius * 0.35) + 6,
                                             x + self.node_radius + 6, y + (self.node_radius * 0.35) + 6,
                                             fill="#d9d9d9", outline="")

            # Основная форма (эллипс)
            oval = self.canvas.create_oval(x - self.node_radius, y - (self.node_radius * 0.35),
                                           x + self.node_radius, y + (self.node_radius * 0.35),
                                           fill=fill, outline=outline_display, width=outline_width, tags=("node",))
            # Текст (с переносом, если нужно)
            text = self.canvas.create_text(x, y, text=name, font=self.node_font, tags=("node_text",), width=self.node_radius*1.6)

            self.node_items[oval] = name
            self.text_items[text] = name

            # Bind hover and click per item tag
            self.canvas.tag_bind(oval, "<Enter>", lambda e, o=oval: self._on_node_enter(o))
            self.canvas.tag_bind(oval, "<Leave>", lambda e, o=oval: self._on_node_leave(o))
            self.canvas.tag_bind(oval, "<Button-1>", lambda e, o=oval: self._on_node_click(o))

            self.canvas.tag_bind(text, "<Enter>", lambda e, o=oval: self._on_node_enter(o))
            self.canvas.tag_bind(text, "<Leave>", lambda e, o=oval: self._on_node_leave(o))
            self.canvas.tag_bind(text, "<Button-1>", lambda e, o=oval: self._on_node_click(o))

        # Легенда (необязательно) — рисуем в углу канвы
        self.canvas.create_rectangle(8, 8, 180, 86, fill="#ffffff", outline="#e0e0e0")
        self.canvas.create_text(95, 18, text="Легенда", font=("Arial", 10, "bold"))
        self.canvas.create_oval(20, 36, 44, 48, fill="#bfe9ff", outline="#2b7cff")
        self.canvas.create_text(100, 42, text="Класс", anchor="w")
        self.canvas.create_oval(20, 54, 44, 66, fill="#c9f0d1", outline="#2a9d4a")
        self.canvas.create_text(100, 60, text="Объект", anchor="w")
        self.canvas.create_oval(20, 72, 44, 84, fill="#fff2b2", outline="#caa10c")
        self.canvas.create_text(100, 78, text="Свойство", anchor="w")

    # ----------------- Node hover / click -----------------
    def _on_node_enter(self, oval_id):
        # подсветка контура
        self.canvas.itemconfigure(oval_id, width=3)
        # поднять поверх
        self.canvas.tag_raise(oval_id)

    def _on_node_leave(self, oval_id):
        # Восстанавливаем ширину: если выделен — оставляем толще
        name = self.node_items.get(oval_id)
        if name in self.selected_nodes:
            self.canvas.itemconfigure(oval_id, width=4)
        else:
            self.canvas.itemconfigure(oval_id, width=2)

    def _on_node_click(self, oval_id):
        """
        Ранее здесь показывалось окно с информацией. Убрал его.
        Теперь клик просто переключает выделение узла (toggle).
        """
        name = self.node_items.get(oval_id)
        if not name:
            return

        if name in self.selected_nodes:
            self.selected_nodes.remove(name)
        else:
            self.selected_nodes.add(name)

        # Обновляем отрисовку, чтобы визуально показать выделение
        self.draw_network()

if __name__ == "__main__":
    root = tk.Tk()
    app = SemanticNetworkEditor(root)
    root.mainloop()
