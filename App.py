import math
import time
import tkinter as tk
from functools import partial
from IGA import IGA
from PIL import Image, ImageTk, ImageGrab
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self, name, iga):
        super(App, self).__init__()

        self.name = name
        self.iga = iga
        self.title(self.name)
        self.geometry('%dx%d+0+0' % (self.winfo_screenwidth(), self.winfo_screenheight()))
        self.resizable(False, False)
        self.selected_character = [0] * iga.population_size
        self.component_index = {
            2: { "name": "lower_body", "width": 75, "height": 100, "x": 150, "y":255 },
            3: { "name": "right_hand", "width": 20, "height": 70, "x": 180, "y":160 },
            4: { "name": "left_hand", "width": 20, "height": 70, "x": 120, "y":160 },
            5: { "name": "upper_body", "width": 75, "height": 100, "x": 150, "y":165 },
            6: { "name": "hair", "width": 60, "height": 38, "x": 151, "y":76 },
            7: { "name": "shape_of_face", "width": 50, "height": 50, "x": 150, "y":95 },
            8: { "name": "eyes", "width": 35, "height": 20, "x": 150, "y":90 },
            9: { "name": "nose", "width": 10, "height": 10, "x": 150, "y":100 },
            10: { "name": "mouth", "width": 30, "height": 10, "x": 150, "y":113 },
            11: { "name": "ears", "width": 70, "height": 20, "x": 150, "y":90 }
        }

    def _set_top_menu_bar(self):
        # Top menu bar
        self.menubar = tk.Menu(self)
        self.operation_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Program', menu=self.operation_menu)
        self.operation_menu.add_separator()
        self.operation_menu.add_command(label='Exit', command=self.quit)
        self.configure(menu=self.menubar)

    def _set_left_frame(self):
        # Left frame show images
        self.left_frame = tk.Frame(self)
        self.canvas1 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=350, highlightthickness=0)
        self.canvas1.grid(row=0, column=0, columnspan=2, padx=3, pady=3)
        self.canvas2 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=350, highlightthickness=0)
        self.canvas2.grid(row=0, column=2, columnspan=2, padx=3, pady=3)
        self.canvas3 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=350, highlightthickness=0)
        self.canvas3.grid(row=0, column=4, columnspan=2, padx=3, pady=3)
        self.canvas4 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=350, highlightthickness=0)
        self.canvas4.grid(row=2, column=0, columnspan=2, padx=3, pady=3)
        self.canvas5 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=350, highlightthickness=0)
        self.canvas5.grid(row=2, column=2, columnspan=2, padx=3, pady=3)
        self.canvas6 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=350, highlightthickness=0)
        self.canvas6.grid(row=2, column=4, columnspan=2, padx=3, pady=3)
        self.canvas_index = { 0: self.canvas1, 1: self.canvas2, 2: self.canvas3,
                              3: self.canvas4, 4: self.canvas5, 5: self.canvas6 }

        left_frame_buttons = {
            "Select": { "bg": "#AAF05A", "fg": "#000000" },
            "Save as PNG": { "bg": "#33B5E5", "fg": "#FFFFFF" }
        }
        self.canvas_btns = []
        for i in range(0, 12):
            if i % 2 == 0:
                btn_name = "Select"
            else:
                btn_name = "Save as PNG"
            btn = left_frame_buttons.get(btn_name, "Index Error")
            self.canvas_btns.append(tk.Label(self.left_frame, text=btn_name, bg=btn['bg'],
                                      fg=btn['fg'], width=16, cursor="X_cursor"))
            row = (math.ceil((i + 1) / 6) - 1) * 2 + 1
            self.canvas_btns[-1].grid(row=row, column=i%6)
        self.left_frame.pack_propagate(0)
        self.left_frame.pack(side=tk.LEFT, fill="both")

    def _enable_canvas_btns(self):
        for btn_index, btn in enumerate(self.canvas_btns):
            btn.configure(cursor="right_ptr")
            if btn_index % 2 == 0:
                btn.bind("<Button-1>", lambda e, x=btn_index/2: self._select_character(int(x)))
                btn.bind("<Enter>", lambda e: self._hover_button(e, "#94CA55"))
                btn.bind("<Leave>", lambda e: self._hover_button(e, "#AAF05A"))
            else:
                btn.bind("<Button-1>", lambda e, x=btn_index/2-0.5: self._save_Canvas(int(x)))
                btn.bind("<Enter>", lambda e: self._hover_button(e, "#51A5C3"))
                btn.bind("<Leave>", lambda e: self._hover_button(e, "#33B5E5"))

    def _hover_button(self, event, color):
        event.widget.configure(bg=color)

    def _set_right_frame(self):
        # Right frame show info and operation
        self.right_frame = tk.Frame(self, width=300, height=800)
        self.right_frame.pack_propagate(0)

        title_box = tk.Label(self.right_frame, text=self.name, wraplength=200,
                             bg="black", fg="white", padx=10, pady=10)
        title_box.pack(side=tk.TOP, fill=tk.X, padx=10)

        self.info = tk.StringVar(self.right_frame)
        self.info_box = tk.Label(self.right_frame, textvar=self.info, bg="black",
                                 fg="white", padx=10, pady=20)
        self.info_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        menu_title = tk.Label(self.right_frame, text="Menu", background="grey",
                              foreground="white")

        menu_space = tk.Frame(self.right_frame, width=300, height=600)
        menu_space.pack_propagate(0)

        menu_space.pack(side=tk.BOTTOM)
        menu_title.pack(side=tk.BOTTOM, fill=tk.X)

        # Set up the menu buttons
        self.buttons = {
            "Start": { "bg": "#AAF05A", "command": lambda e: self._start() },
            "Exit": { "bg": "#FFFFFF", "command": quit }
        }
        self.menu_btn = []
        for btn_name in self.buttons:
            btn = self.buttons.get(btn_name, "Index Error")
            self.menu_btn.append(tk.Label(menu_space, text=btn_name, width=300,
                                           bg=btn['bg'], height=2, bd=1, cursor="right_ptr"))
            self.menu_btn[-1].pack(side=tk.TOP)
            self.menu_btn[-1].bind("<Button-1>", btn['command'])
        self.menu_btn[0].bind("<Enter>", lambda e: self._hover_button(e, "#94CA55"))
        self.menu_btn[0].bind("<Leave>", lambda e: self._hover_button(e, "#AAF05A"))
        self.menu_btn[1].bind("<Enter>", lambda e: self.menu_btn[1].configure(bg="#B7B7B7"))
        self.menu_btn[1].bind("<Leave>", lambda e: self.menu_btn[1].configure(bg="#FFFFFF"))

        self.right_frame.pack(side=tk.RIGHT)

    def _next_generation_button(self):
        self.menu_btn[0].configure(cursor="right_ptr", text="Next Generation")
        self.menu_btn[0].bind("<Button-1>", lambda e: self._show_next_generation())

    def _show_info(self):
        self.info.set("Population Size: " + str(self.iga.population_size) + "\n" +
                      "Generation: " + str(self.iga.generation) + "\n" +
                      "Mutation Probability: " + str(self.iga.mutation_prob) + "\n" +
                      "Version: v1.2.4")

    def _show_characters(self):
        self.img = []
        for character_id, character in enumerate(self.iga.population):
            canvas = self.canvas_index.get(character_id, "Index Error")
            for component_id, component in enumerate(character[2:]):
                part = self.component_index.get(component_id+2, "Index Error")
                width = int(part["width"] * (1.1 + 0.5*(int(character[1], 2)-1)))
                height = int(part["height"] * (1 + 0.1*(int(character[0], 2)-1)))
                x = int(part["x"] * (1.1 + 0.5*(int(character[1], 2)-1)))
                if character[1] == '0':
                    x += 50
                y = int(part["y"] * (1 + 0.1*(int(character[0], 2)-1)))
                image = Image.open("components/" + part["name"] + "/" + component + ".png")
                image = image.resize((width, height), Image.ANTIALIAS)
                self.img.append(ImageTk.PhotoImage(image))
                canvas.create_image(x, y, image=self.img[-1])

    def _save_Canvas(self, canvas_id):
        x = 5 + canvas_id % 3 * 610
        y = 50 + math.floor(canvas_id / 3) * 750
        x1 = x + 600
        y1 = y + 700
        box = (x, y, x1, y1)
        path = "character" + str(canvas_id + 1) + "_" + str(int(time.time())) + ".png"
        ImageGrab.grab(bbox=box).save(path, "PNG")
        messagebox.showinfo("Export the image", "Saved the image as " + path)

    def _select_character(self, canvas_id):
        cv = self.canvas_index.get(canvas_id, "Index Error")
        self.selected_character[canvas_id] = 1 - self.selected_character[canvas_id]
        cv.configure(highlightthickness= 3 - int(cv['highlightthickness']), highlightbackground="black")

    def _start(self):
        self.iga._initial_population()
        self._show_info()
        self._show_characters()
        self._enable_canvas_btns()
        self._next_generation_button()

    def _show_next_generation(self):
        self.iga._next_generation(self.selected_character)
        for selected_index, value in enumerate(self.selected_character):
            if value == 1:
                self._select_character(selected_index)
        self._show_characters()
        self._show_info()

if __name__ == "__main__":
    iga = IGA(population_size=6, mutation_prob=0.01,
              number_of_data=[3, 2, 12, 5, 5, 5, 13, 12, 22, 10, 104, 6])
    app = App("Interactive Genetic Algorithm Cartoon Design", iga)
    app._set_top_menu_bar()
    app._set_left_frame()
    app._set_right_frame()
    app._show_info()

    app.mainloop()
