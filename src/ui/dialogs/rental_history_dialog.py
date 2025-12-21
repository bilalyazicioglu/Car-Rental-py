import tkinter as tk
from tkinter import ttk
from constants import COLORS, FONT_FAMILY
from src.ui.styled_button import StyledButton

class RentalHistoryDialog(tk.Toplevel):
    """Kiralama geçmişi diyalogu."""

    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.title("Kiralama Geçmişi")
        self.geometry("900x600")
        self.resizable(True, True)
        self.minsize(800, 500)
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

        # Başlık
        header = tk.Frame(main, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 20))

        tk.Label(header, text="📋 Kiralama Geçmişi",
                 font=(FONT_FAMILY, 20, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(side=tk.LEFT)

        # İstatistik özeti
        self.summary_label = tk.Label(header, text="",
                                      font=(FONT_FAMILY, 12),
                                      bg=COLORS['bg_primary'], fg=COLORS['text_secondary'])
        self.summary_label.pack(side=tk.RIGHT)

        # Treeview frame
        tree_frame = tk.Frame(main, bg=COLORS['bg_secondary'])
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        columns = ("plaka", "kiralayan", "baslangic", "bitis", "iade", "ucret")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                 yscrollcommand=scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set,
                                 style="Custom.Treeview")

        headings = {
            "plaka": ("Plaka", 100),
            "kiralayan": ("Müşteri", 150),
            "baslangic": ("Başlangıç", 110),
            "bitis": ("Bitiş", 110),
            "iade": ("İade Tarihi", 110),
            "ucret": ("Toplam Ücret", 120)
        }

        for col, (text, width) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, minwidth=80, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # Kapat butonu
        btn_frame = tk.Frame(main, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        StyledButton(btn_frame, "✓ KAPAT", self.destroy,
                     COLORS['accent'], '#ffffff', padx=40, pady=12).pack()

    def _load_history(self):
        # Mevcut verileri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Geçmiş verilerini al
        history = self.data_manager.get_rental_history()

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

        # Özet güncelle
        self.summary_label.config(
            text=f"Toplam: {len(history)} kiralama | Gelir: {total_income:,.0f}₺"
        )
