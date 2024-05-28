import tkinter as tk
from tkinter import filedialog
import json


class ElementPlacer :
    def __init__(self, root) :
        self.root = root
        self.elements = []
        self.root.geometry('800x600')

        # Add buttons to add elements
        self.add_button = tk.Button(self.root, text="Add Button", command=self.add_button_element)
        self.add_button.pack(side=tk.LEFT)

        self.add_label = tk.Button(self.root, text="Add Label", command=self.add_label_element)
        self.add_label.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.root, text="Save Layout", command=self.save_layout)
        self.save_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.root, text="Load Layout", command=self.load_layout)
        self.load_button.pack(side=tk.LEFT)

    def add_button_element(self) :
        button = tk.Button(self.root, text="Button")
        button.place(x=100, y=100)  # Initial placement
        self.elements.append(button)
        self.make_draggable(button)

    def add_label_element(self) :
        label = tk.Label(self.root, text="Label")
        label.place(x=100, y=100)  # Initial placement
        self.elements.append(label)
        self.make_draggable(label)

    def make_draggable(self, widget) :
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event) :
        widget = event.widget
        widget._drag_data = {'x' : event.x, 'y' : event.y}

    def on_drag_motion(self, event) :
        widget = event.widget
        x = widget.winfo_x() - widget._drag_data['x'] + event.x
        y = widget.winfo_y() - widget._drag_data['y'] + event.y
        widget.place(x=x, y=y)

    def save_layout(self) :
        layout = []
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        for element in self.elements :
            x = element.winfo_x() / width
            y = element.winfo_y() / height
            elem_type = type(element).__name__
            text = element.cget("text")
            layout.append({"type" : elem_type, "x" : x, "y" : y, "text" : text})

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path :
            with open(file_path, 'w') as f :
                json.dump(layout, f)

    def load_layout(self) :
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path :
            with open(file_path, 'r') as f :
                layout = json.load(f)

            for element in self.elements :
                element.destroy()
            self.elements.clear()

            width = self.root.winfo_width()
            height = self.root.winfo_height()

            for elem in layout :
                if elem["type"] == "Button" :
                    widget = tk.Button(self.root, text=elem["text"])
                elif elem["type"] == "Label" :
                    widget = tk.Label(self.root, text=elem["text"])
                else :
                    continue

                x = elem["x"] * width
                y = elem["y"] * height
                widget.place(x=x, y=y)
                self.elements.append(widget)
                self.make_draggable(widget)


if __name__ == "__main__" :
    root = tk.Tk()
    app = ElementPlacer(root)
    root.mainloop()
