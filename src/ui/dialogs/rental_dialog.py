import tkinter as tk
from datetime import date, timedelta
from constants import COLORS, FONT_FAMILY
from src.ui.styled_button import StyledButton


class RentalDialog(tk.Toplevel):
    """Kiralama bilgileri giriş diyalogu."""

    def __init__(self, parent, vehicle_info: str, customer_name: str = ""):
        super().__init__(parent)
        self.title("Kiralama Başlat")
        self.geometry("550x520")
        self.resizable(True, True)
        self.minsize(500, 480)
        self.transient(parent)
        self.grab_set()

        self.configure(bg=COLORS['bg_primary'])

        self.result = None
        self.customer_name = customer_name
        self._create_widgets(vehicle_info)
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self, vehicle_info: str):
        main = tk.Frame(self, bg=COLORS['bg_primary'])
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        # Başlık
        tk.Label(main, text="🚗 Kiralama Bilgileri",
                 font=(FONT_FAMILY, 18, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(pady=(0, 10))

        tk.Label(main, text=vehicle_info,
                 font=(FONT_FAMILY, 13, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['accent']).pack(pady=(0, 25))

        # Form
        form = tk.Frame(main, bg=COLORS['bg_primary'])
        form.pack(fill=tk.X, pady=10)
        form.columnconfigure(1, weight=1)

        fields = [
            ("Müşteri Adı:", "customer_entry", self.customer_name),
            ("Başlangıç:", "start_date_entry", date.today().strftime("%Y-%m-%d")),
            ("Bitiş:", "end_date_entry", (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")),
        ]

        for i, (label, attr, default) in enumerate(fields):
            tk.Label(form, text=label, font=(FONT_FAMILY, 12),
                     bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).grid(
                row=i, column=0, sticky=tk.W, pady=8)

            entry = tk.Entry(form, font=(FONT_FAMILY, 12),
                             bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                             insertbackground=COLORS['text_primary'], relief='flat',
                             highlightthickness=2, highlightbackground=COLORS['bg_card'],
                             highlightcolor=COLORS['accent'])
            entry.grid(row=i, column=1, pady=8, padx=(15, 0), sticky=tk.EW, ipady=8)
            entry.insert(0, default)
            setattr(self, attr, entry)

        tk.Label(main, text="📅 Format: YYYY-AA-GG", font=(FONT_FAMILY, 10),
                 bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack(pady=15)

        # Butonlar
        btn_frame = tk.Frame(main, bg=COLORS['bg_primary'])
        btn_frame.pack(pady=20)

        StyledButton(btn_frame, "✓ ONAYLA", self._on_confirm,
                     COLORS['success'], '#ffffff', padx=30, pady=12).pack(side=tk.LEFT, padx=8)

        StyledButton(btn_frame, "✗ İPTAL", self._on_cancel,
                     COLORS['danger'], '#ffffff', padx=30, pady=12).pack(side=tk.LEFT, padx=8)

        self.bind("<Return>", lambda e: self._on_confirm())
        self.bind("<Escape>", lambda e: self._on_cancel())
        self.customer_entry.focus_set()

    def _on_confirm(self):
        """Kiralama bilgilerini onayla."""
        self.result = {
            'kiralayan': self.customer_entry.get().strip(),
            'baslangic': self.start_date_entry.get().strip(),
            'bitis': self.end_date_entry.get().strip()
        }
        self.destroy()

    def _on_cancel(self):
        """İptal et ve pencereyi kapat."""
        self.result = None
        self.destroy()
