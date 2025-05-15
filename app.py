import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from recommendation_engine import RecommendationEngine
from visualization import Visualizer

class IngredientHealthSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Kesehatan Berdasarkan Bahan")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Create main frames
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        self.result_frame = ttk.Frame(root, padding="10")
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create style
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        
        # Create input widgets
        ttk.Label(self.input_frame, text="Masukkan Nutrisi Bahan:", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10, sticky="w")
        
        # Create sliders for nutritional preferences with their variables
        self.sliders = {}
        
        self.sliders["Kalori Maksimum"] = self.create_slider(self.input_frame, "Kalori Maksimum", 0, 600, 300, 1, 0)
        self.sliders["Gula Maksimum (g)"] = self.create_slider(self.input_frame, "Gula Maksimum (g)", 0, 50, 25, 2, 0)
        self.sliders["Karbohidrat Maksimum (g)"] = self.create_slider(self.input_frame, "Karbohidrat Maksimum (g)", 0, 100, 50, 3, 0)
        self.sliders["Protein Minimum (g)"] = self.create_slider(self.input_frame, "Protein Minimum (g)", 0, 50, 10, 1, 2)
        self.sliders["Lemak Maksimum (g)"] = self.create_slider(self.input_frame, "Lemak Maksimum (g)", 0, 50, 20, 2, 2)
        self.sliders["Serat Minimum (g)"] = self.create_slider(self.input_frame, "Serat Minimum (g)", 0, 10, 2, 3, 2)
        self.sliders["Vitamin C Minimum (mg)"] = self.create_slider(self.input_frame, "Vitamin C Minimum (mg)", 0, 100, 15, 4, 0)
        
        # Button to calculate health score
        ttk.Button(self.input_frame, text="Hitung Skor Kesehatan", command=self.generate_health_score).grid(row=8, column=3, pady=20, padx=5)
        
        # Initialize visualizer for charts
        self.visualizer = Visualizer(self.result_frame)
        
        # Result display (health score category)
        self.result_label = ttk.Label(self.result_frame, text="Kategori Kesehatan: ", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=10)
    
    def create_slider(self, parent, label_text, min_val, max_val, default_val, row, col_offset):
        """Create a slider with a label showing its current value"""
        ttk.Label(parent, text=label_text).grid(row=row, column=col_offset, padx=5, pady=5, sticky="w")
        var = tk.IntVar(value=default_val)
        slider = ttk.Scale(parent, from_=min_val, to=max_val, variable=var, orient="horizontal", length=200)
        slider.grid(row=row, column=col_offset+1, padx=5, pady=5)
        
        # Add a label to show the current value
        value_label = ttk.Label(parent, text=str(default_val))
        value_label.grid(row=row, column=col_offset+1, padx=(210, 0), pady=5, sticky="w")
        
        # Update the label when the slider changes
        def update_label(event):
            value_label.config(text=str(int(slider.get())))
        
        slider.bind("<Motion>", update_label)
        slider.bind("<ButtonRelease-1>", update_label)
        
        return var
    
    def generate_health_score(self):
        """Calculate health score based on user input"""
        # Collect nutritional input
        preferences = {
            "Kalori Maksimum": self.sliders["Kalori Maksimum"].get(),
            "Gula Maksimum (g)": self.sliders["Gula Maksimum (g)"].get(),
            "Karbohidrat Maksimum (g)": self.sliders["Karbohidrat Maksimum (g)"].get(),
            "Protein Minimum (g)": self.sliders["Protein Minimum (g)"].get(),
            "Lemak Maksimum (g)": self.sliders["Lemak Maksimum (g)"].get(),
            "Serat Minimum (g)": self.sliders["Serat Minimum (g)"].get(),
            "Vitamin C Minimum (mg)": self.sliders["Vitamin C Minimum (mg)"].get()
        }
        
        # Calculate health score using the RecommendationEngine
        score = RecommendationEngine.calculate_health_score(preferences)
        category = RecommendationEngine.categorize_health(score)
        
        # Display the health category
        self.result_label.config(text=f"Kategori Kesehatan: {category}")
        
        # Update the visualization
        self.visualizer.update_charts([(category, score, category)])