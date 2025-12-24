import tkinter as tk
from constants import COLORS, FONT_FAMILY
from src.ui.styled_button import StyledButton


class ExpiryNotificationDialog(tk.Toplevel):
    """Sigorta/Kasko süresi dolan araçlar için bildirim diyalogu."""

    def __init__(self, parent, expiry_data, data_manager=None, on_vehicle_click=None):
        super().__init__(parent)
        self.title("Bildirimler")
        self.geometry("500x450")
        self.resizable(True, True)
        self.minsize(450, 400)
        self.transient(parent)
        self.grab_set()

        self.configure(bg=COLORS['bg_primary'])
        self.expiry_data = expiry_data
        self.failed_rentals = expiry_data.get('failed_rentals', [])
        self.data_manager = data_manager
        self.on_vehicle_click = on_vehicle_click
        self._create_widgets()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        main = tk.Frame(self, bg=COLORS['bg_primary'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Başlık
        tk.Label(main, text="Bildirimler",
                 font=(FONT_FAMILY, 18, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(pady=(0, 15))

        # Scrollable frame
        canvas = tk.Canvas(main, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_primary'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Süresi geçmiş
        expired = self.expiry_data.get('expired', [])
        if expired:
            self._create_section(scrollable_frame, "Süresi Geçenler", expired, COLORS['danger'])

        # Süresi yaklaşan
        expiring = self.expiry_data.get('expiring_soon', [])
        if expiring:
            self._create_section(scrollable_frame, "30 Gün İçinde Bitecek", expiring, COLORS['warning'])

        # Başarısız kiralama girişimleri
        if self.failed_rentals:
            self._create_failed_section(scrollable_frame, "Başarısız Kiralama Girişimleri", self.failed_rentals, COLORS['danger'])

        # Bildirim yoksa
        if not expired and not expiring and not self.failed_rentals:
            tk.Label(scrollable_frame, text="Bildirim yok",
                     font=(FONT_FAMILY, 12),
                     bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack(pady=20)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Kapat butonu
        StyledButton(main, "KAPAT", self.destroy,
                     COLORS['bg_secondary'], COLORS['text_primary'],
                     font_size=11, padx=30, pady=10).pack(pady=(15, 0))

        self.bind("<Escape>", lambda e: self.destroy())

    def _create_section(self, parent, title, items, color):
        """Bildirim bölümü oluştur."""
        section = tk.Frame(parent, bg=COLORS['bg_primary'])
        section.pack(fill=tk.X, pady=(0, 15))

        # Başlık
        header = tk.Frame(section, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 8))

        tk.Label(header, text=title,
                 font=(FONT_FAMILY, 13, "bold"),
                 bg=COLORS['bg_primary'], fg=color).pack(side=tk.LEFT)

        tk.Label(header, text=f"({len(items)})",
                 font=(FONT_FAMILY, 11),
                 bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack(side=tk.LEFT, padx=5)

        # Öğeler
        for item in items:
            self._create_item(section, item, color)

    def _create_item(self, parent, item, color):
        """Tek bir bildirim öğesi oluştur."""
        v = item['vehicle']
        card = tk.Frame(parent, bg=COLORS['bg_card'], padx=12, pady=10)
        card.pack(fill=tk.X, pady=3)

        # Sol - Araç bilgisi
        left = tk.Frame(card, bg=COLORS['bg_card'])
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(left, text=f"{v.marka} {v.model}",
                 font=(FONT_FAMILY, 11, "bold"),
                 bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(anchor=tk.W)

        tk.Label(left, text=v.plaka,
                 font=(FONT_FAMILY, 10),
                 bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor=tk.W)

        # Sağ - Tür ve tarih
        right = tk.Frame(card, bg=COLORS['bg_card'])
        right.pack(side=tk.RIGHT)

        tk.Label(right, text=item['type'],
                 font=(FONT_FAMILY, 10, "bold"),
                 bg=COLORS['bg_card'], fg=color).pack(anchor=tk.E)

        tk.Label(right, text=item['date'],
                 font=(FONT_FAMILY, 10),
                 bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor=tk.E)

    def _create_failed_section(self, parent, title, items, color):
        """Başarısız kiralama bölümü oluştur."""
        section = tk.Frame(parent, bg=COLORS['bg_primary'])
        section.pack(fill=tk.X, pady=(0, 15))

        # Başlık
        header = tk.Frame(section, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 8))

        tk.Label(header, text=title,
                 font=(FONT_FAMILY, 13, "bold"),
                 bg=COLORS['bg_primary'], fg=color).pack(side=tk.LEFT)

        tk.Label(header, text=f"({len(items)})",
                 font=(FONT_FAMILY, 11),
                 bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack(side=tk.LEFT, padx=5)

        # Öğeler
        for item in items:
            self._create_failed_item(section, item, color)

    def _create_failed_item(self, parent, item, color):
        """Başarısız kiralama öğesi oluştur."""
        card = tk.Frame(parent, bg=COLORS['bg_card'], padx=12, pady=10)
        card.pack(fill=tk.X, pady=3)

        # Sol - Araç bilgisi
        left = tk.Frame(card, bg=COLORS['bg_card'])
        left.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(left, text=f"{item['marka']} {item['model']}",
                 font=(FONT_FAMILY, 11, "bold"),
                 bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(anchor=tk.W)

        tk.Label(left, text=item['plaka'],
                 font=(FONT_FAMILY, 10),
                 bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor=tk.W)

        # Sağ - Tarih ve sebep
        right = tk.Frame(card, bg=COLORS['bg_card'])
        right.pack(side=tk.RIGHT)

        tk.Label(right, text=item['tarih'],
                 font=(FONT_FAMILY, 9),
                 bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor=tk.E)

        # Sebep kısalt
        sebep = item['sebep'][:40] + "..." if len(item['sebep']) > 40 else item['sebep']
        tk.Label(right, text=sebep,
                 font=(FONT_FAMILY, 9),
                 bg=COLORS['bg_card'], fg=color).pack(anchor=tk.E)

        # Okundu butonu
        if self.data_manager:
            btn_frame = tk.Frame(card, bg=COLORS['bg_card'])
            btn_frame.pack(side=tk.RIGHT, padx=(10, 0))
            
            okundu_btn = tk.Label(btn_frame, text="✓", 
                                  font=(FONT_FAMILY, 12, "bold"),
                                  bg=COLORS['success'], fg="white",
                                  padx=8, pady=2, cursor="hand2")
            okundu_btn.pack()
            okundu_btn.bind("<Button-1>", lambda e, id=item['id'], c=card: self._mark_as_read(id, c))

    def _mark_as_read(self, rental_id, card_widget):
        """Bildirimi okundu olarak işaretle ve kaldır."""
        if self.data_manager:
            self.data_manager.delete_failed_rental(rental_id)
            card_widget.destroy()
