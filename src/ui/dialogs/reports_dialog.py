import tkinter as tk
from constants import COLORS, FONT_FAMILY


class ReportsDialog(tk.Toplevel):

    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.title("📊 Raporlama ve Analiz")
        self.geometry("600x500")
        self.configure(bg=COLORS['bg_primary'])
        self.dm = data_manager

        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        main = tk.Frame(self, bg=COLORS['bg_primary'], padx=30, pady=25)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main, text="📈 İşletme Analizi", font=(FONT_FAMILY, 20, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(pady=(0, 20))

        stats_frame = tk.Frame(main, bg=COLORS['bg_primary'])
        stats_frame.pack(fill=tk.BOTH, expand=True)

        stats = self._calculate_stats()

        self._create_stat_card(stats_frame, "💰 Toplam Gelir", f"{stats['revenue']:,.0f} ₺", 0)
        self._create_stat_card(stats_frame, "🚗 Kiradaki Araçlar", f"{stats['rented_count']} Adet", 1)
        self._create_stat_card(stats_frame, "🏆 En Popüler Marka", stats['top_brand'], 2)
        self._create_stat_card(stats_frame, "🛠 Bakımdaki Araçlar", f"{stats['maintenance_count']} Adet", 3)

    def _create_stat_card(self, parent, title, value, row):
        card = tk.Frame(parent, bg=COLORS['bg_secondary'], padx=15, pady=15,
                        highlightthickness=1, highlightbackground=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=5)

        tk.Label(card, text=title, font=(FONT_FAMILY, 11),
                 bg=COLORS['bg_secondary'], fg=COLORS['text_secondary']).pack(side=tk.LEFT)
        tk.Label(card, text=value, font=(FONT_FAMILY, 13, "bold"),
                 bg=COLORS['bg_secondary'], fg=COLORS['accent']).pack(side=tk.RIGHT)

    def _calculate_stats(self):
        vehicles = self.dm.get_all_vehicles()
        history = self.dm.get_rental_history()

        # Gelir Hesapla
        total_revenue = sum(h.toplam_ucret for h in history)

        # Kiradaki ve Bakımdaki Sayısı
        rented = len([v for v in vehicles if v.durum.lower() == 'kirada'])
        maintenance = len([v for v in vehicles if v.durum.lower() == 'bakımda'])

        # En çok kiralanan marka
        brand_counts = {}
        for h in history:
            brand_counts[h.plaka[:2]] = brand_counts.get(h.plaka[:2], 0) + 1  # Örnek mantık

        top_brand = "Veri Yetersiz"
        if history:
            top_brand = max(set([h.plaka for h in history]), key=[h.plaka for h in history].count)
            top_brand = f"Plaka: {top_brand}"

        return {
            "revenue": total_revenue,
            "rented_count": rented,
            "maintenance_count": maintenance,
            "top_brand": top_brand
        }