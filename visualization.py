import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Visualizer:
    def __init__(self, master):
        self.fig, self.ax2 = plt.subplots(1, 1, figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_charts(self, results):
        self.ax2.clear()

        # Pie chart statis sebagai informasi kategori rentang skor
        labels = [
            '0-20: Sangat Tidak Sehat',
            '21-40: Tidak Sehat',
            '41-60: Cukup Sehat',
            '61-80: Sehat',
            '81-100: Sangat Sehat'
        ]
        sizes = [1, 1, 1, 1, 1]  # Sama besar sektor
        colors = ['red', 'orange', 'lightgreen', 'yellow', 'green']

        self.ax2.pie(
            sizes,
            labels=labels,
            colors=colors,
            startangle=90,
            counterclock=False,
            wedgeprops={'edgecolor': 'black'}
        )
        self.ax2.set_title('Informasi Rentang Skor Kesehatan')

        self.fig.tight_layout()
        self.canvas.draw()