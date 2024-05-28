


import tkinter as tk
from tkinter import filedialog, messagebox
import json

class client:
    def __init__(self):
        pass


class contractor:
    def __init__(self):
        pass


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
            file_path = self.layout_file
            if file_path :
                with open(file_path, 'r') as f :
                    layout = json.load(f)

                for element, _ in self.elements :
                    element.destroy()
                self.elements.clear()



                for elem in layout :
                    if elem["type"] == "Button" :
                        command = self.get_command(elem["command"])
                        widget = tk.Button(self.root, text=elem["text"], command=command)
                    elif elem["type"] == "Label" :
                        widget = tk.Label(self.root, text=elem["text"])
                    else :
                        continue
                    width = elem["width"]
                    height = elem["height"]
                    x = elem["x"] * width
                    y = elem["y"] * height
                    widget.place(x=x, y=y)
        except Exception as e :
            messagebox.showerror("Error", f"Failed to load layout: {e}")






if __name__ == "__main__" :
    layout_file = "layouts/test for loading new commands V0.2.5.json"  # Specify your layout file here
    root = tk.Tk()
    app = ElementViewer(root, layout_file)
    root.mainloop()
