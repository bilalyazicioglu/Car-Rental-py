import tkinter as tk
from constants import COLORS, FONT_FAMILY
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsDialog(tk.Toplevel):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.title("📈 30 Günlük Gelir Analizi")
        self.geometry("1000x650")
        self.configure(bg=COLORS['bg_primary'])
        self.dm = data_manager

        self._create_widgets()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        main = tk.Frame(self, bg=COLORS['bg_primary'], padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main, text="📊 Son 30 Günlük Toplam Gelir Grafiği", font=(FONT_FAMILY, 18, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(pady=(0, 20))

        history = self.dm.get_rental_history()
        daily_data = {}

        for h in history:
            day = h.baslangic_tarihi[:10]
            daily_data[day] = daily_data.get(day, 0) + h.toplam_ucret

        if not daily_data:
            tk.Label(main, text="Grafik için yeterli veri bulunmuyor.",
                     bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack()
            return

        days = sorted(daily_data.keys())[-30:]
        revenues = [daily_data[d] for d in days]

        fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
        fig.patch.set_facecolor(COLORS['bg_primary'])
        ax.set_facecolor(COLORS['bg_secondary'])

        ax.plot(days, revenues, color=COLORS['accent'], marker='o', linewidth=2, markersize=4)
        ax.fill_between(days, revenues, color=COLORS['accent'], alpha=0.15)

        ax.set_title("Günlük Gelir Dağılımı (Son 30 Gün)", color='white', pad=20)
        ax.tick_params(axis='x', colors='white', rotation=45, labelsize=8)
        ax.tick_params(axis='y', colors='white', labelsize=9)
        ax.grid(True, linestyle=':', alpha=0.2, color='gray')

        for i, txt in enumerate(revenues):
            if txt > 0:
                ax.annotate(f"{int(txt)}₺", (days[i], revenues[i]),
                            textcoords="offset points", xytext=(0, 8),
                            ha='center', color='white', fontsize=7)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=main)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)