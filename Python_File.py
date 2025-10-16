import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

class SemanticNetworkEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор семантической сети и фреймов")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Стили для элементов
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 9))
        self.style.configure('TCombobox', font=('Arial', 9))
        self.style.configure('TEntry', font=('Arial', 9))
        
        self.nodes = {}
        self.relations = []
        self.frames = {}
        
        self.network_canvas_width = 1200
        self.network_canvas_height = 700
        self.frames_canvas_width = 1200
        self.frames_canvas_height = 700
        self.node_radius = 60
        
        # Сохраняем пример сети для восстановления
        self.example_nodes = {}
        self.example_relations = []
        self.example_frames = {}
        self.load_example_network()
        
        self.create_widgets()
        self.draw_network()
        self.draw_frames()
    
    def load_example_network(self):
        """Загрузка примера семантической сети и фреймов"""
        # Узлы
        self.example_nodes = {
            "птица": {"type": "class", "x": 450, "y": 100},
            "животные": {"type": "class", "x": 450, "y": 50},
            "страус": {"type": "object", "x": 200, "y": 200},
            "канарейка": {"type": "object", "x": 400, "y": 200},
            "дрозд": {"type": "object", "x": 600, "y": 200},
            "пингвин": {"type": "object", "x": 800, "y": 200},
            "летать": {"type": "property", "x": 700, "y": 300},
            "ходить": {"type": "property", "x": 100, "y": 300},
            "петь": {"type": "property", "x": 500, "y": 300},
            "оперенье": {"type": "property", "x": 200, "y": 50},
            "желтый": {"type": "property", "x": 300, "y": 450},
            "черный": {"type": "property", "x": 700, "y": 450},
            "коричневый": {"type": "property", "x": 500, "y": 450},
        }
        
        # Отношения
        self.example_relations = [
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
        
        # Фреймы
        self.example_frames = {
            "Фрейм: Птица": {
                "type": "class_frame",
                "x": 300, 
                "y": 200,
                "slots": {
                    "Класс": "Птица",
                    "Наследует": "Животные",
                    "Имеет": "Оперенье",
                    "Умеет": "Летать, Петь",
                    "Примеры": "Страус, Канарейка, Дрозд, Пингвин"
                }
            },
            "Фрейм: Канарейка": {
                "type": "object_frame", 
                "x": 600, 
                "y": 200,
                "slots": {
                    "Объект": "Канарейка",
                    "Тип": "Птица",
                    "Цвет": "Желтый",
                    "Умеет": "Летать, Петь",
                    "Особенности": "Маленькая, Певчая"
                }
            },
            "Фрейм: Пингвин": {
                "type": "object_frame",
                "x": 900, 
                "y": 200,
                "slots": {
                    "Объект": "Пингвин",
                    "Тип": "Птица",
                    "Цвет": "Черный",
                    "Умеет": "Ходить, Плавать",
                    "Особенности": "Не летает, Живет в Антарктиде"
                }
            },
            "Фрейм: Страус": {
                "type": "object_frame",
                "x": 300, 
                "y": 400,
                "slots": {
                    "Объект": "Страус",
                    "Тип": "Птица",
                    "Цвет": "Коричневый",
                    "Умеет": "Ходить, Бегать",
                    "Особенности": "Не летает, Самая большая птица"
                }
            }
        }
        
        # Загружаем пример в текущую сеть
        self.nodes = self.example_nodes.copy()
        self.relations = self.example_relations.copy()
        self.frames = self.example_frames.copy()
    
    def restore_network(self):
        """Восстановление примера сети"""
        self.nodes = self.example_nodes.copy()
        self.relations = self.example_relations.copy()
        self.frames = self.example_frames.copy()
        self.update_comboboxes()
        self.draw_network()
        self.draw_frames()
        messagebox.showinfo("Успех", "Сеть восстановлена до исходного состояния")
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Создаем Notebook для переключения между сетью и фреймами
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка для семантической сети
        self.network_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.network_tab, text="Семантическая сеть")
        
        # Вкладка для фреймов
        self.frames_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.frames_tab, text="Фреймы")
        
        # ===== ВКЛАДКА СЕМАНТИЧЕСКОЙ СЕТИ =====
        self.create_network_tab()
        
        # ===== ВКЛАДКА ФРЕЙМОВ =====
        self.create_frames_tab()
    
    def create_network_tab(self):
        """Создание вкладки семантической сети"""
        # Главный контейнер с разделением на две части
        main_paned = ttk.PanedWindow(self.network_tab, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Левая панель - canvas сети
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=3)
        
        # Правая панель - управление сетью
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # Область отрисовки сети
        canvas_frame = ttk.LabelFrame(left_frame, text="Визуализация семантической сети", padding=10)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Добавляем прокрутку для canvas
        canvas_container = ttk.Frame(canvas_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.network_canvas = tk.Canvas(
            canvas_container, 
            bg="white", 
            width=self.network_canvas_width, 
            height=self.network_canvas_height,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            scrollregion=(0, 0, self.network_canvas_width, self.network_canvas_height)
        )
        self.network_canvas.pack(fill=tk.BOTH, expand=True)
        
        v_scrollbar.config(command=self.network_canvas.yview)
        h_scrollbar.config(command=self.network_canvas.xview)
        
        # Добавляем возможность масштабирования и перемещения
        self.network_canvas.bind("<MouseWheel>", self.zoom_network)
        self.network_canvas.bind("<ButtonPress-1>", self.scroll_start_network)
        self.network_canvas.bind("<B1-Motion>", self.scroll_move_network)
        
        self.network_zoom_level = 1.0
        
        # Панель управления сетью
        self.create_network_controls(right_frame)
    
    def create_frames_tab(self):
        """Создание вкладки фреймов"""
        # Главный контейнер с разделением на две части
        main_paned = ttk.PanedWindow(self.frames_tab, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Левая панель - canvas фреймов
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=3)
        
        # Правая панель - управление фреймами
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # Область отрисовки фреймов
        canvas_frame = ttk.LabelFrame(left_frame, text="Визуализация фреймов", padding=10)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Добавляем прокрутку для canvas
        canvas_container = ttk.Frame(canvas_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.frames_canvas = tk.Canvas(
            canvas_container, 
            bg="white", 
            width=self.frames_canvas_width, 
            height=self.frames_canvas_height,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            scrollregion=(0, 0, self.frames_canvas_width, self.frames_canvas_height)
        )
        self.frames_canvas.pack(fill=tk.BOTH, expand=True)
        
        v_scrollbar.config(command=self.frames_canvas.yview)
        h_scrollbar.config(command=self.frames_canvas.xview)
        
        # Добавляем возможность масштабирования и перемещения
        self.frames_canvas.bind("<MouseWheel>", self.zoom_frames)
        self.frames_canvas.bind("<ButtonPress-1>", self.scroll_start_frames)
        self.frames_canvas.bind("<B1-Motion>", self.scroll_move_frames)
        
        self.frames_zoom_level = 1.0
        
        # Панель управления фреймами
        self.create_frame_controls(right_frame)
    
    def create_network_controls(self, parent):
        """Создание элементов управления сетью"""
        # Панель добавления узлов
        node_frame = ttk.LabelFrame(parent, text="Добавить узел", padding=10)
        node_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(node_frame, text="Имя узла:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.node_name = ttk.Entry(node_frame, width=20)
        self.node_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(node_frame, text="Тип:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.node_type = ttk.Combobox(node_frame, values=["класс", "объект", "свойство"], width=12, state="readonly")
        self.node_type.grid(row=0, column=3, padx=5, pady=5)
        self.node_type.set("объект")
        
        ttk.Button(node_frame, text="Добавить узел", command=self.add_node).grid(row=0, column=4, padx=10, pady=5)
        
        # Панель добавления связей
        relation_frame = ttk.LabelFrame(parent, text="Добавить связь", padding=10)
        relation_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(relation_frame, text="От:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.relation_from = ttk.Combobox(relation_frame, values=list(self.nodes.keys()), width=15)
        self.relation_from.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(relation_frame, text="К:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.relation_to = ttk.Combobox(relation_frame, values=list(self.nodes.keys()), width=15)
        self.relation_to.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(relation_frame, text="Тип связи:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.relation_type = ttk.Combobox(relation_frame, values=["является", "имеет", "умеет", "имеет цвет"], width=12, state="readonly")
        self.relation_type.grid(row=0, column=5, padx=5, pady=5)
        self.relation_type.set("является")
        
        ttk.Button(relation_frame, text="Добавить связь", command=self.add_relation).grid(row=0, column=6, padx=10, pady=5)
        
        # Панель управления сетью
        management_frame = ttk.LabelFrame(parent, text="Управление сетью", padding=10)
        management_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(management_frame, text="Обновить отображение", command=self.draw_network).pack(side=tk.LEFT, padx=5)
        ttk.Button(management_frame, text="Авторазмещение", command=self.auto_layout_network).pack(side=tk.LEFT, padx=5)
        ttk.Button(management_frame, text="Очистить сеть", command=self.clear_network).pack(side=tk.LEFT, padx=5)
        ttk.Button(management_frame, text="Восстановить сеть", command=self.restore_network).pack(side=tk.LEFT, padx=5)
        
        # Информационная панель
        info_frame = ttk.LabelFrame(parent, text="Информация о сети", padding=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        self.network_info_label = ttk.Label(info_frame, text="Узлов: 0, Связей: 0")
        self.network_info_label.pack(anchor=tk.W)
        
        # Легенда
        legend_frame = ttk.LabelFrame(parent, text="Легенда сети", padding=10)
        legend_frame.pack(fill=tk.X, pady=5)
        
        legend_canvas = tk.Canvas(legend_frame, height=50, bg='#f0f0f0', highlightthickness=0)
        legend_canvas.pack(fill=tk.X)
        
        # Элементы легенды
        legend_items = [
            ("Класс", "lightblue"),
            ("Объект", "lightgreen"), 
            ("Свойство", "lightyellow"),
            ("является", "blue"),
            ("имеет", "green"),
            ("умеет", "red"),
            ("имеет цвет", "black")
        ]
        
        x_pos = 10
        for text, color in legend_items:
            if text in ["Класс", "Объект", "Свойство"]:
                legend_canvas.create_oval(x_pos, 15, x_pos+20, 35, fill=color, outline='black')
                legend_canvas.create_text(x_pos+25, 25, text=text, anchor=tk.W, font=('Arial', 9))
                x_pos += 80
            else:
                legend_canvas.create_line(x_pos, 25, x_pos+20, 25, fill=color, width=2, arrow=tk.LAST)
                legend_canvas.create_text(x_pos+25, 25, text=text, anchor=tk.W, font=('Arial', 9))
                x_pos += 90
    
    def create_frame_controls(self, parent):
        """Создание элементов управления фреймами"""
        # Основной фрейм для управления фреймами
        frame_control = ttk.LabelFrame(parent, text="Управление фреймами", padding=15)
        frame_control.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Добавление фреймов
        add_frame = ttk.LabelFrame(frame_control, text="Создать фрейм", padding=10)
        add_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(add_frame, text="Имя фрейма:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.frame_name = ttk.Entry(add_frame, width=20)
        self.frame_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Тип фрейма:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.frame_type = ttk.Combobox(add_frame, values=["фрейм класса", "фрейм объекта"], width=15, state="readonly")
        self.frame_type.grid(row=0, column=3, padx=5, pady=5)
        self.frame_type.set("фрейм объекта")
        
        ttk.Button(add_frame, text="Создать фрейм", command=self.create_frame).grid(row=0, column=4, padx=10, pady=5)
        
        # Добавление слотов к фрейму
        slot_frame = ttk.LabelFrame(frame_control, text="Добавить слот к фрейму", padding=10)
        slot_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(slot_frame, text="Фрейм:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.slot_frame_name = ttk.Combobox(slot_frame, values=list(self.frames.keys()), width=20)
        self.slot_frame_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(slot_frame, text="Имя слота:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.slot_name = ttk.Entry(slot_frame, width=20)
        self.slot_name.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(slot_frame, text="Значение:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.slot_value = ttk.Entry(slot_frame, width=20)
        self.slot_value.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(slot_frame, text="Добавить слот", command=self.add_slot).grid(row=2, column=2, padx=10, pady=5)
        
        # Панель управления фреймами
        management_frame = ttk.LabelFrame(frame_control, text="Управление фреймами", padding=10)
        management_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(management_frame, text="Обновить отображение", command=self.draw_frames).pack(side=tk.LEFT, padx=5)
        ttk.Button(management_frame, text="Авторазмещение", command=self.auto_layout_frames).pack(side=tk.LEFT, padx=5)
        ttk.Button(management_frame, text="Очистить фреймы", command=self.clear_frames).pack(side=tk.LEFT, padx=5)
        
        # Информационная панель
        info_frame = ttk.LabelFrame(frame_control, text="Информация о фреймах", padding=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.frames_info_label = ttk.Label(info_frame, text="Фреймов: 0")
        self.frames_info_label.pack(anchor=tk.W)
        
        # Легенда фреймов
        legend_frame = ttk.LabelFrame(frame_control, text="Легенда фреймов", padding=10)
        legend_frame.pack(fill=tk.X, pady=10)
        
        legend_canvas = tk.Canvas(legend_frame, height=40, bg='#f0f0f0', highlightthickness=0)
        legend_canvas.pack(fill=tk.X)
        
        # Элементы легенды
        legend_items = [
            ("Фрейм класса", "#ffcc99"),
            ("Фрейм объекта", "#ccffcc")
        ]
        
        x_pos = 10
        for text, color in legend_items:
            legend_canvas.create_rectangle(x_pos, 10, x_pos+20, 30, fill=color, outline='black')
            legend_canvas.create_text(x_pos+25, 20, text=text, anchor=tk.W, font=('Arial', 9))
            x_pos += 150
        
        # Просмотр и редактирование фреймов
        view_frame = ttk.LabelFrame(frame_control, text="Просмотр фреймов", padding=10)
        view_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Список фреймов
        ttk.Label(view_frame, text="Доступные фреймы:").pack(anchor=tk.W, pady=5)
        
        frame_list_frame = ttk.Frame(view_frame)
        frame_list_frame.pack(fill=tk.X, pady=5)
        
        self.frames_listbox = tk.Listbox(frame_list_frame, height=8, font=('Arial', 9))
        self.frames_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_list_frame, orient=tk.VERTICAL, command=self.frames_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.frames_listbox.config(yscrollcommand=scrollbar.set)
        
        # Кнопки управления фреймами
        frame_buttons = ttk.Frame(view_frame)
        frame_buttons.pack(fill=tk.X, pady=10)
        
        ttk.Button(frame_buttons, text="Показать фрейм", command=self.show_frame).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Удалить фрейм", command=self.delete_frame).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Обновить список", command=self.update_frames_list).pack(side=tk.LEFT, padx=5)
        
        # Область отображения фрейма
        ttk.Label(view_frame, text="Содержимое фрейма:").pack(anchor=tk.W, pady=(10, 5))
        
        self.frame_display = tk.Text(view_frame, height=12, width=40, font=('Arial', 9), wrap=tk.WORD)
        self.frame_display.pack(fill=tk.BOTH, expand=True)
        
        # Обновляем список фреймов
        self.update_frames_list()
    
    def update_frames_list(self):
        """Обновление списка фреймов"""
        self.frames_listbox.delete(0, tk.END)
        for frame_name in self.frames.keys():
            self.frames_listbox.insert(tk.END, frame_name)
    
    def show_frame(self):
        """Отображение выбранного фрейма"""
        selection = self.frames_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите фрейм для просмотра")
            return
        
        frame_name = self.frames_listbox.get(selection[0])
        frame_data = self.frames[frame_name]
        
        # Формируем текст для отображения
        display_text = f"Фрейм: {frame_name}\n"
        display_text += f"Тип: {frame_data['type']}\n"
        display_text += f"Позиция: ({frame_data['x']}, {frame_data['y']})\n\n"
        display_text += "Слоты:\n"
        
        for slot_name, slot_value in frame_data['slots'].items():
            display_text += f"  {slot_name}: {slot_value}\n"
        
        self.frame_display.delete(1.0, tk.END)
        self.frame_display.insert(1.0, display_text)
    
    def create_frame(self):
        """Создание нового фрейма"""
        frame_name = self.frame_name.get().strip()
        frame_type = self.frame_type.get()
        
        if not frame_name:
            messagebox.showerror("Ошибка", "Введите имя фрейма")
            return
        
        if frame_name in self.frames:
            messagebox.showerror("Ошибка", "Фрейм с таким именем уже существует")
            return
        
        # Находим свободную позицию для фрейма
        x, y = self.find_free_position_frames(200, 200)
        
        # Создаем фрейм
        self.frames[frame_name] = {
            "type": frame_type,
            "x": x,
            "y": y,
            "slots": {}
        }
        
        self.update_frames_list()
        self.slot_frame_name['values'] = list(self.frames.keys())
        self.draw_frames()
        
        self.frame_name.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Фрейм '{frame_name}' создан")
    
    def add_slot(self):
        """Добавление слота к фрейму"""
        frame_name = self.slot_frame_name.get()
        slot_name = self.slot_name.get().strip()
        slot_value = self.slot_value.get().strip()
        
        if not frame_name or not slot_name or not slot_value:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if frame_name not in self.frames:
            messagebox.showerror("Ошибка", "Выбранный фрейм не существует")
            return
        
        # Добавляем слот
        self.frames[frame_name]['slots'][slot_name] = slot_value
        
        self.draw_frames()
        
        self.slot_name.delete(0, tk.END)
        self.slot_value.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Слот '{slot_name}' добавлен к фрейму '{frame_name}'")
    
    def delete_frame(self):
        """Удаление выбранного фрейма"""
        selection = self.frames_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите фрейм для удаления")
            return
        
        frame_name = self.frames_listbox.get(selection[0])
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить фрейм '{frame_name}'?"):
            del self.frames[frame_name]
            self.update_frames_list()
            self.slot_frame_name['values'] = list(self.frames.keys())
            self.frame_display.delete(1.0, tk.END)
            self.draw_frames()
            messagebox.showinfo("Успех", f"Фрейм '{frame_name}' удален")
    
    def clear_frames(self):
        """Очистка всех фреймов"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить все фреймы?"):
            self.frames.clear()
            self.update_frames_list()
            self.slot_frame_name['values'] = list(self.frames.keys())
            self.frame_display.delete(1.0, tk.END)
            self.draw_frames()
            messagebox.showinfo("Успех", "Все фреймы очищены")
    
    def zoom_network(self, event):
        """Масштабирование canvas сети"""
        scale_factor = 1.1
        if event.delta > 0:
            self.network_zoom_level *= scale_factor
        else:
            self.network_zoom_level /= scale_factor
        
        self.network_canvas.scale("all", event.x, event.y, 
                         scale_factor if event.delta > 0 else 1/scale_factor, 
                         scale_factor if event.delta > 0 else 1/scale_factor)
    
    def scroll_start_network(self, event):
        """Начало перемещения canvas сети"""
        self.network_canvas.scan_mark(event.x, event.y)
    
    def scroll_move_network(self, event):
        """Перемещение canvas сети"""
        self.network_canvas.scan_dragto(event.x, event.y, gain=1)
    
    def zoom_frames(self, event):
        """Масштабирование canvas фреймов"""
        scale_factor = 1.1
        if event.delta > 0:
            self.frames_zoom_level *= scale_factor
        else:
            self.frames_zoom_level /= scale_factor
        
        self.frames_canvas.scale("all", event.x, event.y, 
                         scale_factor if event.delta > 0 else 1/scale_factor, 
                         scale_factor if event.delta > 0 else 1/scale_factor)
    
    def scroll_start_frames(self, event):
        """Начало перемещения canvas фреймов"""
        self.frames_canvas.scan_mark(event.x, event.y)
    
    def scroll_move_frames(self, event):
        """Перемещение canvas фреймов"""
        self.frames_canvas.scan_dragto(event.x, event.y, gain=1)
    
    def find_free_position_network(self, center_x, center_y, max_attempts=100):
        """Поиск свободной позиции для нового узла в сети"""
        for attempt in range(max_attempts):
            radius = self.node_radius * (attempt // 10 + 1)
            angle = attempt * 0.5 
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            if (x < self.node_radius or x > self.network_canvas_width - self.node_radius or
                y < self.node_radius or y > self.network_canvas_height - self.node_radius):
                continue
            
            collision = False
            for node_name, node_data in self.nodes.items():
                distance = math.sqrt((x - node_data["x"])**2 + (y - node_data["y"])**2)
                if distance < self.node_radius * 2.2: 
                    collision = True
                    break
            
            if not collision:
                return x, y
        
        return (random.randint(self.node_radius, self.network_canvas_width - self.node_radius),
                random.randint(self.node_radius, self.network_canvas_height - self.node_radius))
    
    def find_free_position_frames(self, center_x, center_y, max_attempts=100):
        """Поиск свободной позиции для нового фрейма"""
        frame_width = 200
        frame_height = 150
        
        for attempt in range(max_attempts):
            radius = 150 * (attempt // 10 + 1)
            angle = attempt * 0.5 
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            if (x < frame_width/2 or x > self.frames_canvas_width - frame_width/2 or
                y < frame_height/2 or y > self.frames_canvas_height - frame_height/2):
                continue
            
            collision = False
            for frame_name, frame_data in self.frames.items():
                distance = math.sqrt((x - frame_data["x"])**2 + (y - frame_data["y"])**2)
                if distance < 250:  # Минимальное расстояние между фреймами
                    collision = True
                    break
            
            if not collision:
                return x, y
        
        return (random.randint(frame_width//2, self.frames_canvas_width - frame_width//2),
                random.randint(frame_height//2, self.frames_canvas_height - frame_height//2))
    
    def add_node(self):
        """Добавление нового узла"""
        name = self.node_name.get().strip()
        node_type = self.node_type.get()
        
        if not name:
            messagebox.showerror("Ошибка", "Введите имя узла")
            return
        
        if name in self.nodes:
            messagebox.showerror("Ошибка", "Узел с таким именем уже существует")
            return
        
        x, y = self.find_free_position_network(self.network_canvas_width // 2, self.network_canvas_height // 2)
        
        self.nodes[name] = {
            "type": node_type,
            "x": x,
            "y": y
        }
        
        self.update_comboboxes()
        self.draw_network()
        
        self.node_name.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Узел '{name}' добавлен")
    
    def add_relation(self):
        """Добавление новой связи"""
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
        
        self.relations.append({
            "from": from_node,
            "to": to_node,
            "type": relation_type
        })
        
        self.draw_network()
        messagebox.showinfo("Успех", f"Связь '{relation_type}' добавлена")
    
    def auto_layout_network(self):
        """Автоматическое размещение узлов в сети"""
        # Группируем узлы по типам
        classes = [name for name, data in self.nodes.items() if data["type"] == "класс"]
        objects = [name for name, data in self.nodes.items() if data["type"] == "объект"]
        properties = [name for name, data in self.nodes.items() if data["type"] == "свойство"]
        
        # Размещаем классы вверху
        class_y = 80
        class_spacing = self.network_canvas_width / (len(classes) + 1)
        for i, class_name in enumerate(classes):
            self.nodes[class_name]["x"] = class_spacing * (i + 1)
            self.nodes[class_name]["y"] = class_y
        
        # Размещаем объекты посередине
        object_y = self.network_canvas_height / 2
        object_spacing = self.network_canvas_width / (len(objects) + 1)
        for i, object_name in enumerate(objects):
            self.nodes[object_name]["x"] = object_spacing * (i + 1)
            self.nodes[object_name]["y"] = object_y
        
        # Размещаем свойства внизу
        property_y = self.network_canvas_height - 80
        property_spacing = self.network_canvas_width / (len(properties) + 1)
        for i, property_name in enumerate(properties):
            self.nodes[property_name]["x"] = property_spacing * (i + 1)
            self.nodes[property_name]["y"] = property_y
        
        # Применяем force-directed layout для улучшения размещения
        self.apply_force_directed_layout_network()
        
        self.draw_network()
        messagebox.showinfo("Успех", "Авторазмещение сети выполнено")
    
    def auto_layout_frames(self):
        """Автоматическое размещение фреймов"""
        if not self.frames:
            messagebox.showinfo("Информация", "Нет фреймов для размещения")
            return
        
        # Размещаем фреймы в виде сетки
        cols = int(math.ceil(math.sqrt(len(self.frames))))
        rows = int(math.ceil(len(self.frames) / cols))
        
        frame_width = 200
        frame_height = 150
        
        col_spacing = self.frames_canvas_width / (cols + 1)
        row_spacing = self.frames_canvas_height / (rows + 1)
        
        for i, (frame_name, frame_data) in enumerate(self.frames.items()):
            col = i % cols
            row = i // cols
            
            frame_data["x"] = col_spacing * (col + 1)
            frame_data["y"] = row_spacing * (row + 1)
        
        self.draw_frames()
        messagebox.showinfo("Успех", "Авторазмещение фреймов выполнено")
    
    def apply_force_directed_layout_network(self, iterations=50):
        """Применяет алгоритм force-directed для улучшения размещения узлов в сети"""
        for _ in range(iterations):
            for node1_name, node1_data in self.nodes.items():
                fx, fy = 0, 0
                
                # Отталкивание от других узлов
                for node2_name, node2_data in self.nodes.items():
                    if node1_name != node2_name:
                        dx = node1_data["x"] - node2_data["x"]
                        dy = node1_data["y"] - node2_data["y"]
                        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
                        
                        # Сила отталкивания
                        force = 1000 / (distance * distance)
                        fx += force * dx / distance
                        fy += force * dy / distance
                
                # Притяжение к связанным узлам
                for relation in self.relations:
                    if relation["from"] == node1_name:
                        other_node = self.nodes[relation["to"]]
                    elif relation["to"] == node1_name:
                        other_node = self.nodes[relation["from"]]
                    else:
                        continue
                    
                    dx = other_node["x"] - node1_data["x"]
                    dy = other_node["y"] - node1_data["y"]
                    distance = max(math.sqrt(dx*dx + dy*dy), 0.1)

                    # Сила притяжения
                    force = distance * 0.1
                    fx += force * dx / distance
                    fy += force * dy / distance

                # Ограничиваем максимальное перемещение
                max_move = 10
                move_x = min(max(fx * 0.1, -max_move), max_move)
                move_y = min(max(fy * 0.1, -max_move), max_move)
                
                # Обновляем позицию с учетом границ canvas
                new_x = max(self.node_radius, min(self.network_canvas_width - self.node_radius, node1_data["x"] + move_x))
                new_y = max(self.node_radius, min(self.network_canvas_height - self.node_radius, node1_data["y"] + move_y))
                
                node1_data["x"] = new_x
                node1_data["y"] = new_y
    
    def clear_network(self):
        """Очистка сети"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю сеть?"):
            self.nodes.clear()
            self.relations.clear()
            self.update_comboboxes()
            self.draw_network()
            messagebox.showinfo("Успех", "Сеть очищена")
    
    def update_comboboxes(self):
        """Обновление значений в комбобоксах"""
        nodes_list = list(self.nodes.keys())
        self.relation_from['values'] = nodes_list
        self.relation_to['values'] = nodes_list
        
        # Обновляем информацию о сети и фреймах
        self.network_info_label.config(text=f"Узлов: {len(self.nodes)}, Связей: {len(self.relations)}")
        self.frames_info_label.config(text=f"Фреймов: {len(self.frames)}")
    
    def draw_network(self):
        """Отрисовка семантической сети"""
        self.network_canvas.delete("all")

        # Рисуем связи
        for relation in self.relations:
            from_node = self.nodes[relation["from"]]
            to_node = self.nodes[relation["to"]]

            # Цвета для разных типов связей
            color = "black"
            if relation["type"] == "является":
                color = "blue"
            elif relation["type"] == "имеет":
                color = "green"
            elif relation["type"] == "умеет":
                color = "red"
            elif relation["type"] == "имеет цвет":
                color = "black"

            # Рисуем линию связи
            self.network_canvas.create_line(
                from_node["x"], from_node["y"], 
                to_node["x"], to_node["y"],
                fill=color, width=2, arrow=tk.LAST, smooth=True
            )
            
            # Добавляем текст типа связи
            mid_x = (from_node["x"] + to_node["x"]) / 2
            mid_y = (from_node["y"] + to_node["y"]) / 2
            
            # Фон для текста для лучшей читаемости
            text_bg = self.network_canvas.create_rectangle(
                mid_x-30, mid_y-10, mid_x+30, mid_y+10, 
                fill="white", outline="white"
            )
            self.network_canvas.tag_lower(text_bg)  # Перемещаем фон под текст
            
            self.network_canvas.create_text(
                mid_x, mid_y, 
                text=relation["type"], 
                fill=color, 
                font=("Arial", 9, "bold")
            )
        
        # Рисуем узлы
        for name, node in self.nodes.items():
            # Цвета для разных типов узлов
            color = "lightblue"
            if node["type"] == "объект":
                color = "lightgreen"
            elif node["type"] == "свойство":
                color = "lightyellow"
            
            # Рисуем узел
            node_id = self.network_canvas.create_oval(
                node["x"] - self.node_radius, node["y"] - 20,
                node["x"] + self.node_radius, node["y"] + 20,
                fill=color, outline="black", width=2
            )
            
            # Добавляем текст имени узла
            self.network_canvas.create_text(
                node["x"], node["y"], 
                text=name, 
                font=("Arial", 10, "bold"),
                width=self.node_radius * 1.8  # Ограничение ширины текста
            )
        
        # Обновляем область прокрутки
        self.network_canvas.configure(scrollregion=self.network_canvas.bbox("all"))
    
    def draw_frames(self):
        """Отрисовка фреймов"""
        self.frames_canvas.delete("all")

        # Рисуем фреймы
        for frame_name, frame_data in self.frames.items():
            # Определяем цвет фрейма в зависимости от типа
            frame_color = "#ffcc99"  # фрейм класса
            if frame_data["type"] == "фрейм объекта":
                frame_color = "#ccffcc"
            
            # Вычисляем размеры фрейма на основе количества слотов
            slot_count = len(frame_data["slots"])
            frame_width = 200
            frame_height = 80 + slot_count * 20
            
            # Рисуем прямоугольник фрейма
            x1 = frame_data["x"] - frame_width // 2
            y1 = frame_data["y"] - frame_height // 2
            x2 = frame_data["x"] + frame_width // 2
            y2 = frame_data["y"] + frame_height // 2
            
            # Основной прямоугольник
            self.frames_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=frame_color, outline="black", width=2
            )
            
            # Заголовок фрейма
            self.frames_canvas.create_rectangle(
                x1, y1, x2, y1 + 30,
                fill="#e6e6e6", outline="black", width=1
            )
            
            # Текст заголовка
            self.frames_canvas.create_text(
                frame_data["x"], y1 + 15,
                text=frame_name,
                font=("Arial", 10, "bold"),
                width=frame_width - 10
            )
            
            # Слоты фрейма
            y_offset = y1 + 45
            for i, (slot_name, slot_value) in enumerate(frame_data["slots"].items()):
                slot_text = f"{slot_name}: {slot_value}"
                self.frames_canvas.create_text(
                    x1 + 10, y_offset,
                    text=slot_text,
                    font=("Arial", 8),
                    anchor=tk.W,
                    width=frame_width - 20
                )
                y_offset += 20
        
        # Обновляем область прокрутки
        self.frames_canvas.configure(scrollregion=self.frames_canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SemanticNetworkEditor(root)
    root.mainloop()