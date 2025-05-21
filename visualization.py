import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Visualizer:
    def __init__(self, master):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_charts(self, results):
        self.ax1.clear()
        self.ax2.clear()

        # Bar chart berdasarkan hasil aktual (kategori dan skor real)
        categories = [r[0] for r in results]
        scores = [r[1] for r in results]

        if categories and scores:
            bars = self.ax1.barh(categories, scores)
            self.ax1.set_xlabel('Skor Kesehatan (Nilai Real)')
            self.ax1.set_title('Skor Kesehatan Berdasarkan Kategori')
            for bar, score in zip(bars, scores):
                # Tampilkan nilai skor real persis pada label
                self.ax1.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                              f'{score:.1f}', va='center')
        else:
            self.ax1.text(0.5, 0.5, 'Tidak ada data', ha='center', va='center')

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
