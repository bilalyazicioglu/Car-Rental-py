import tkinter as tk
from tkinter import ttk
from constants import COLORS, FONT_FAMILY
from src.ui.styled_button import StyledButton


class RentalHistoryDialog(tk.Toplevel):
    """Kiralama geçmişi diyalogu (Modern Tasarımlı Filtre Paneli ile)."""

    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.title("Kiralama Geçmişi")
        self.geometry("1000x700")
        self.resizable(True, True)
        self.minsize(900, 600)
        self.transient(parent)
        self.grab_set()

        self.configure(bg=COLORS['bg_primary'])
        self.data_manager = data_manager

        self._create_widgets()
        self._load_history()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        main = tk.Frame(self, bg=COLORS['bg_primary'])
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        # 1. Başlık Bölümü
        header = tk.Frame(main, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 15))

        tk.Label(header, text="📋 Kiralama Geçmişi",
                 font=(FONT_FAMILY, 22, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)

        self.summary_label = tk.Label(header, text="",
                                      font=(FONT_FAMILY, 11),
                                      bg=COLORS['bg_primary'], fg=COLORS['text_secondary'])
        self.summary_label.pack(side=tk.RIGHT, pady=(10, 0))

        # 2. MODERN FİLTRELEME ÇUBUĞU
        filter_bar = tk.Frame(main, bg=COLORS['bg_card'], padx=20, pady=15)
        filter_bar.pack(fill=tk.X, pady=(0, 20))

        tk.Label(filter_bar, text="🗓️ Filtre:", font=(FONT_FAMILY, 11, "bold"),
                 bg=COLORS['bg_card'], fg=COLORS['accent']).pack(side=tk.LEFT, padx=(0, 15))

        # Başlangıç Girişi
        tk.Label(filter_bar, text="Başlangıç:", font=(FONT_FAMILY, 9),
                 bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(side=tk.LEFT, padx=2)

        self.start_date_ent = tk.Entry(filter_bar, width=12, font=(FONT_FAMILY, 10),
                                       bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                                       insertbackground="white", relief="flat", highlightthickness=1,
                                       highlightbackground=COLORS['bg_primary'])
        self.start_date_ent.insert(0, "2025-01-01")
        self.start_date_ent.pack(side=tk.LEFT, padx=5, ipady=3)

        # Bitiş Girişi
        tk.Label(filter_bar, text="Bitiş:", font=(FONT_FAMILY, 9),
                 bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(side=tk.LEFT, padx=2)

        self.end_date_ent = tk.Entry(filter_bar, width=12, font=(FONT_FAMILY, 10),
                                     bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                                     insertbackground="white", relief="flat", highlightthickness=1,
                                     highlightbackground=COLORS['bg_primary'])
        self.end_date_ent.insert(0, "2025-12-31")
        self.end_date_ent.pack(side=tk.LEFT, padx=5, ipady=3)

        # Butonları sağa itmek için boşluk
        tk.Label(filter_bar, bg=COLORS['bg_card']).pack(side=tk.LEFT, expand=True)

        # Listele Butonu (Label bazlı buton tasarımı)
        filter_btn = tk.Label(filter_bar, text="🔍 Listele", font=(FONT_FAMILY, 10, "bold"),
                              bg=COLORS['accent'], fg="white", padx=15, pady=7, cursor="hand2")
        filter_btn.pack(side=tk.LEFT, padx=5)
        filter_btn.bind("<Button-1>", lambda e: self._apply_filter())

        # Temizle Butonu
        reset_btn = tk.Label(filter_bar, text="🔄 Temizle", font=(FONT_FAMILY, 10, "bold"),
                             bg=COLORS['bg_secondary'], fg=COLORS['text_primary'], padx=15, pady=7, cursor="hand2")
        reset_btn.pack(side=tk.LEFT, padx=5)
        reset_btn.bind("<Button-1>", lambda e: self._load_history())

        # 3. Treeview (Liste) Bölümü
        tree_frame = tk.Frame(main, bg=COLORS['bg_secondary'])
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("plaka", "kiralayan", "baslangic", "bitis", "iade", "ucret")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                 yscrollcommand=scrollbar_y.set,
                                 style="Custom.Treeview")

        headings = {
            "plaka": ("Plaka", 100),
            "kiralayan": ("Müşteri", 150),
            "baslangic": ("Başlangıç", 120),
            "bitis": ("Bitiş", 120),
            "iade": ("Durum / İade", 130),
            "ucret": ("Toplam Ücret", 120)
        }

        for col, (text, width) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, minwidth=100, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar_y.config(command=self.tree.yview)

        # 4. Alt Buton Bölümü
        btn_frame = tk.Frame(main, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        StyledButton(btn_frame, "✓ KAPAT", self.destroy,
                     COLORS['bg_card'], COLORS['text_primary'], padx=40, pady=12).pack()

    def _apply_filter(self):
        """Kullanıcının girdiği tarihlere göre filtreleme yapar."""
        start = self.start_date_ent.get()
        end = self.end_date_ent.get()
        filtered_history = self.data_manager.get_rental_history_by_date(start, end)
        self._load_history(data=filtered_history)

    def _load_history(self, data=None):
        """Listeyi verilerle doldurur."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        history = data if data is not None else self.data_manager.get_rental_history()

        total_income = 0
        for h in history:
            self.tree.insert("", tk.END, values=(
                h.plaka,
                h.kiralayan,
                h.baslangic_tarihi,
                h.bitis_tarihi,
                h.iade_tarihi,
                f"{h.toplam_ucret:,.0f}₺"
            ))
            total_income += h.toplam_ucret

        self.summary_label.config(
            text=f"Toplam: {len(history)} işlem | Hasılat: {total_income:,.0f}₺"
        )