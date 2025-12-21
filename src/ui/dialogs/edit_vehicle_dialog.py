import tkinter as tk
from constants import COLORS, FONT_FAMILY
from src.ui.styled_button import StyledButton


class EditVehicleDialog(tk.Toplevel):
    """Araç düzenleme diyalogu."""

    def __init__(self, parent, vehicle):
        super().__init__(parent)
        self.title("Araç Düzenle")
        self.geometry("550x580")
        self.resizable(True, True)
        self.minsize(500, 520)
        self.transient(parent)
        self.grab_set()

        self.configure(bg=COLORS['bg_primary'])

        self.vehicle = vehicle
        self.result = None
        self._create_widgets()
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
        tk.Label(main, text="🔧 Araç Düzenle",
                 font=(FONT_FAMILY, 18, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(pady=(0, 5))

        tk.Label(main, text=self.vehicle.plaka,
                 font=(FONT_FAMILY, 14, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['accent']).pack(pady=(0, 25))

        # Form
        form = tk.Frame(main, bg=COLORS['bg_primary'])
        form.pack(fill=tk.X)
        form.columnconfigure(1, weight=1)

        fields = [
            ("Marka:", "marka_entry", self.vehicle.marka),
            ("Model:", "model_entry", self.vehicle.model),
            ("Günlük Ücret:", "ucret_entry", str(self.vehicle.ucret)),
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

        # Durum
        tk.Label(form, text="Durum:", font=(FONT_FAMILY, 12),
                 bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).grid(
            row=3, column=0, sticky=tk.W, pady=8)

        self.durum_var = tk.StringVar(value=self.vehicle.durum)
        durum_frame = tk.Frame(form, bg=COLORS['bg_primary'])
        durum_frame.grid(row=3, column=1, pady=8, padx=(15, 0), sticky=tk.W)

        for text, value in [("Müsait", "müsait"), ("Kirada", "kirada"), ("Bakımda", "bakımda")]:
            tk.Radiobutton(
                durum_frame, text=text, variable=self.durum_var, value=value,
                font=(FONT_FAMILY, 11), bg=COLORS['bg_primary'], fg=COLORS['text_primary'],
                selectcolor=COLORS['bg_card'], activebackground=COLORS['bg_primary'],
                activeforeground=COLORS['accent'], highlightthickness=0
            ).pack(side=tk.LEFT, padx=8)

        # Butonlar
        btn_frame = tk.Frame(main, bg=COLORS['bg_primary'])
        btn_frame.pack(pady=30)

        StyledButton(btn_frame, "✓ KAYDET", self._on_save,
                     COLORS['success'], '#ffffff', padx=30, pady=12).pack(side=tk.LEFT, padx=8)

        StyledButton(btn_frame, "✗ İPTAL", self._on_cancel,
                     COLORS['danger'], '#ffffff', padx=30, pady=12).pack(side=tk.LEFT, padx=8)

        self.bind("<Return>", lambda e: self._on_save())
        self.bind("<Escape>", lambda e: self._on_cancel())

    def _on_save(self):
        self.result = {
            'marka': self.marka_entry.get(),
            'model': self.model_entry.get(),
            'ucret': self.ucret_entry.get(),
            'durum': self.durum_var.get()
        }
        self.destroy()

    def _on_cancel(self):
        self.result = None
        self.destroy()
