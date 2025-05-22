import tkinter as tk
from tkinter import ttk
from recommendation_engine import RecommendationEngine
from visualization import Visualizer

class IngredientHealthSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Kesehatan Berdasarkan Bahan")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Frame input
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        # Frame hasil dan visualisasi
        self.result_frame = ttk.Frame(root, padding="10")
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Style
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        
        # Judul input
        ttk.Label(self.input_frame, text="Masukkan Nutrisi Bahan:", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10, sticky="w")
        
        # Slider nutrisi
        self.sliders = {}
        self.sliders["Kalori"] = self.create_slider(self.input_frame, "Kalori", 0, 1000, 500, 1, 0)
        self.sliders["Gula (g)"] = self.create_slider(self.input_frame, "Gula (g)", 0, 50, 25, 2, 0)
        self.sliders["Karbohidrat (g)"] = self.create_slider(self.input_frame, "Karbohidrat (g)", 0, 100, 50, 3, 0)
        self.sliders["Protein (g)"] = self.create_slider(self.input_frame, "Protein (g)", 0, 50, 25, 1, 2)
        self.sliders["Lemak (g)"] = self.create_slider(self.input_frame, "Lemak (g)", 0, 50, 25, 2, 2)
        self.sliders["Serat (g)"] = self.create_slider(self.input_frame, "Serat (g)", 0, 10, 5, 3, 2)
        self.sliders["Vitamin C (mg)"] = self.create_slider(self.input_frame, "Vitamin C (mg)", 0, 100, 50, 4, 0)
        self.sliders["Berat Badan (kg)"] = self.create_slider(self.input_frame, "Berat Badan (kg)", 0, 100, 50, 5, 0)
        self.sliders["Tinggi Badan (cm)"] = self.create_slider(self.input_frame, "Tinggi Badan (cm)", 0, 200, 160, 6, 0)
        
        # Tombol hitung
        ttk.Button(self.input_frame, text="Hitung Skor Kesehatan", command=self.generate_health_score).grid(row=8, column=3, pady=20, padx=5)
        
        # Visualizer untuk grafik
        self.visualizer = Visualizer(self.result_frame)
        
        # Label hasil kategori
        self.result_label = ttk.Label(self.result_frame, text="Kategori Kesehatan: ", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=10)
        
        # Penyimpanan hasil semua input untuk grafik distribusi
        self.all_results = []
    
    def create_slider(self, parent, label_text, min_val, max_val, default_val, row, col_offset):
        ttk.Label(parent, text=label_text).grid(row=row, column=col_offset, padx=5, pady=5, sticky="w")
        var = tk.IntVar(value=default_val)
        slider = ttk.Scale(parent, from_=min_val, to=max_val, variable=var, orient="horizontal", length=200)
        slider.grid(row=row, column=col_offset+1, padx=5, pady=5)
        
        value_label = ttk.Label(parent, text=str(default_val))
        value_label.grid(row=row, column=col_offset+1, padx=(210, 0), pady=5, sticky="w")
        
        def update_label(event):
            value_label.config(text=str(int(slider.get())))
        
        slider.bind("<Motion>", update_label)
        slider.bind("<ButtonRelease-1>", update_label)
        
        return var
    
    def generate_health_score(self):
        preferences = {
            "Kalori": self.sliders["Kalori"].get(),
            "Gula (g)": self.sliders["Gula (g)"].get(),
            "Karbohidrat (g)": self.sliders["Karbohidrat (g)"].get(),
            "Protein (g)": self.sliders["Protein (g)"].get(),
            "Lemak (g)": self.sliders["Lemak (g)"].get(),
            "Serat (g)": self.sliders["Serat (g)"].get(),
            "Vitamin C (mg)": self.sliders["Vitamin C (mg)"].get(),
            "Berat Badan (kg)": self.sliders["Berat Badan (kg)"].get(),
            "Tinggi Badan (cm)": self.sliders["Tinggi Badan (cm)"].get()
        }
        
        # Sesuaikan skor berdasarkan tabel untuk perempuan 19-29 tahun
        ideal_calories = 1900
        ideal_protein = 29
        ideal_fat = 29
        ideal_carbs = 300
        ideal_sugar = 65
        ideal_fiber = 2
        ideal_vitamin_c = 15
        
        weight = preferences["Berat Badan (kg)"]
        height = preferences["Tinggi Badan (cm)"]
        bmi = weight / ((height / 100) ** 2)
        
        # Penyesuaian skor berdasarkan BMI dan nilai ideal dari tabel
        adjusted_score = RecommendationEngine.calculate_health_score(preferences)
        if 18.5 <= bmi <= 24.9:  # Rentang BMI normal
            adjusted_score += 10  # Bonus untuk BMI normal
        elif bmi < 18.5 or bmi > 24.9:
            adjusted_score -= 10  # Penalti untuk BMI di luar rentang normal
        
        # Pastikan skor tetap dalam rentang 0-100
        adjusted_score = max(0, min(100, adjusted_score))
        
        # Dapatkan kategori tunggal dari skor real
        category = RecommendationEngine.categorize_health(adjusted_score)
        
        # Tampilkan kategori tunggal
        self.result_label.config(text=f"Kategori Kesehatan: {category}")
        
        # Simpan hasil dan update grafik
        self.all_results.append((category, adjusted_score))
        self.visualizer.update_charts(self.all_results)

if __name__ == "__main__":
    root = tk.Tk()
    app = IngredientHealthSystem(root)
    root.mainloop()