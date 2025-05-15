import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Visualizer:
    def __init__(self, master):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def update_charts(self, results):
        """Update the visualization charts"""
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Extract data
        categories = [r[0] for r in results]  # Health categories
        scores = [r[1] for r in results]      # Health scores
        
        # Bar chart of health score
        if categories and scores:
            bars = self.ax1.barh(categories, scores)
            self.ax1.set_xlabel('Skor Kesehatan')
            self.ax1.set_title('Skor Kesehatan Berdasarkan Kategori')
            
            # Add score labels
            for bar, score in zip(bars, scores):
                self.ax1.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                             f'{score:.1f}', va='center')
        else:
            self.ax1.text(0.5, 0.5, 'Tidak ada data', ha='center', va='center')
        
        # Pie chart of health categories
        if categories:
            category_counts = {}
            for cat in categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            labels = list(category_counts.keys())
            sizes = list(category_counts.values())
            
            # Define colors for health categories
            colors = {
                'Sangat Sehat': 'green',
                'Cukup Sehat': 'lightgreen',
                'Sehat': 'yellow',
                'Tidak Sehat': 'orange',
                'Sangat Tidak Sehat': 'red'
            }
            
            # Use only colors for categories that exist in our data
            pie_colors = [colors[label] for label in labels]
            
            self.ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=pie_colors)
            self.ax2.set_title('Distribusi Kategori Kesehatan')
        else:
            self.ax2.text(0.5, 0.5, 'Tidak ada data', ha='center', va='center')
        
        self.fig.tight_layout()
        self.canvas.draw()