import tkinter as tk
from constants import COLORS, FONT_FAMILY


class DateFilterDialog(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("📅 Tarih Aralığı Seç")
        self.geometry("350x250")
        self.configure(bg=COLORS['bg_primary'])
        self.callback = callback

        main = tk.Frame(self, bg=COLORS['bg_primary'], padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main, text="Başlangıç (YYYY-AA-GG):", bg=COLORS['bg_primary'], fg="white").pack(pady=5)
        self.start_ent = tk.Entry(main)
        self.start_ent.insert(0, "2025-01-01")
        self.start_ent.pack(fill=tk.X)

        tk.Label(main, text="Bitiş (YYYY-AA-GG):", bg=COLORS['bg_primary'], fg="white").pack(pady=5)
        self.end_ent = tk.Entry(main)
        self.end_ent.insert(0, "2025-12-31")
        self.end_ent.pack(fill=tk.X)

        tk.Button(main, text="🔍 Filtrele", command=self._apply, bg=COLORS['accent'], fg="white").pack(pady=20)

    def _apply(self):
        self.callback(self.start_ent.get(), self.end_ent.get())
        self.destroy()