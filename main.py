import tkinter as tk
from app import IngredientHealthSystem  # Updated to match the new class name

if __name__ == "__main__":
    root = tk.Tk()
    app = IngredientHealthSystem(root)  # Updated to initialize the new system class
    root.mainloop()
