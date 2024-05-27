import tkinter as tk
from tkinter import filedialog, messagebox
import json


class ElementViewer :
    def __init__(self, root, layout_file) :
        self.root = root
        self.layout_file = layout_file
        self.elements = []
        self.root.geometry('800x600')
        self.load_layout()

    def get_command(self, command_name) :
        if command_name == "Say Hello" :
            return lambda : messagebox.showinfo("Hello", "Hello, world!")
        elif command_name == "Show Info" :
            return lambda : messagebox.showinfo("Info", "This is a button.")
        else :
            return None

    def load_layout(self) :
        try :
            with open(self.layout_file, 'r') as f :
                layout = json.load(f)

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
                self.elements.append(widget)
        except Exception as e :
            messagebox.showerror("Error", f"Failed to load layout: {e}")


if __name__ == "__main__" :
    layout_file = "layout.json"  # Specify your layout file here
    root = tk.Tk()
    app = ElementViewer(root, layout_file)
    root.mainloop()
