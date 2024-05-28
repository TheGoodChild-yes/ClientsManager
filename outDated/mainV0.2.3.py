import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
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
        name, command_name = self.get_element_details(is_button=True)
        if name :
            command = self.get_command(command_name)
            button = tk.Button(self.root, text=name, command=command)
            button.place(x=100, y=100)  # Initial placement
            self.elements.append((button, command_name))
            self.make_draggable(button)
            self.make_deletable(button)

    def add_label_element(self) :
        name, _ = self.get_element_details(is_button=False)
        if name :
            label = tk.Label(self.root, text=name)
            label.place(x=100, y=100)  # Initial placement
            self.elements.append((label, None))
            self.make_draggable(label)
            self.make_deletable(label)

    def get_element_details(self, is_button) :
        popup = tk.Toplevel(self.root)
        popup.geometry('300x200')
        popup.title("Element Details")

        tk.Label(popup, text="Enter name:").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack(pady=5)

        command_var = tk.StringVar(popup)
        command_var.set("None")

        if is_button :
            tk.Label(popup, text="Select command:").pack(pady=5)
            commands = ["None", "Say Hello", "Show Info"]
            command_menu = tk.OptionMenu(popup, command_var, *commands)
            command_menu.pack(pady=5)

        def on_submit() :
            name = name_entry.get()
            command_name = command_var.get() if is_button else None
            popup.destroy()
            popup.result = (name, command_name)

        submit_button = tk.Button(popup, text="Submit", command=on_submit)
        submit_button.pack(pady=10)

        self.root.wait_window(popup)
        return getattr(popup, 'result', (None, None))

    def get_command(self, command_name) :
        if command_name == "Say Hello" :
            return lambda : messagebox.showinfo("Hello", "Hello, world!")
        elif command_name == "Show Info" :
            return lambda : messagebox.showinfo("Info", "This is a button.")
        else :
            return None

    def make_draggable(self, widget) :
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def make_deletable(self, widget) :
        widget.bind("<Button-3>", self.on_right_click)

    def on_drag_start(self, event) :
        widget = event.widget
        widget._drag_data = {'x' : event.x, 'y' : event.y}

    def on_drag_motion(self, event) :
        widget = event.widget
        x = widget.winfo_x() - widget._drag_data['x'] + event.x
        y = widget.winfo_y() - widget._drag_data['y'] + event.y
        widget.place(x=x, y=y)

    def on_right_click(self, event) :
        widget = event.widget
        result = messagebox.askyesno("Delete Element", "Do you want to delete this element?")
        if result :
            self.elements = [el for el in self.elements if el[0] != widget]
            widget.destroy()

    def save_layout(self) :
        layout = []
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        print(width, height)
        for element, command_name in self.elements :
            x = element.winfo_x() / width
            y = element.winfo_y() / height
            elem_type = type(element).__name__
            text = element.cget("text")
            layout.append({"type" : elem_type, "x" : x, "y" : y, "height" : height, "width" : width,"text" : text, "command" : command_name})

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path :
            with open(file_path, 'w') as f :
                json.dump(layout, f)

    def load_layout(self) :
        try:
            file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if file_path :
                with open(file_path, 'r') as f :
                    layout = json.load(f)

                for element, _ in self.elements :
                    element.destroy()
                self.elements.clear()

                width = self.root.winfo_width()
                height = self.root.winfo_height()

                for elem in layout :
                    if elem["type"] == "Button" :
                        command = self.get_command(elem["command"])
                        widget = tk.Button(self.root, text=elem["text"], command=command)
                    elif elem["type"] == "Label" :
                        widget = tk.Label(self.root, text=elem["text"])
                    else :
                        continue

                    x = elem["x"] * width
                    y = elem["y"] * height
                    widget.place(x=x, y=y)
                    self.elements.append((widget, elem["command"]))
                    self.make_draggable(widget)
                    self.make_deletable(widget)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load layout: {e}")

if __name__ == "__main__" :
    root = tk.Tk()
    app = ElementPlacer(root)
    root.mainloop()
