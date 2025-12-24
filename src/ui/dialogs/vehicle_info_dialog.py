import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from constants import COLORS, FONT_FAMILY
from src.ui.styled_button import StyledButton


class VehicleInfoDialog(tk.Toplevel):
    """Araç sigorta ve kasko bilgilerini gösteren dialog."""

    def __init__(self, parent, vehicle, data_manager):
        super().__init__(parent)
        self.title("Araç Bilgileri")
        self.geometry("450x420")
        self.resizable(True, True)
        self.minsize(400, 380)
        self.transient(parent)
        self.grab_set()

        self.configure(bg=COLORS['bg_primary'])

        self.vehicle = vehicle
        self.data_manager = data_manager
        self._create_widgets()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        main = tk.Frame(self, bg=COLORS['bg_primary'])
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # Başlık
        tk.Label(main, text="ℹ️ Araç Bilgileri",
                 font=(FONT_FAMILY, 18, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(pady=(0, 5))

        # Araç bilgisi
        info_text = f"{self.vehicle.marka} {self.vehicle.model}"
        tk.Label(main, text=info_text,
                 font=(FONT_FAMILY, 14, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['accent']).pack(pady=(0, 3))

        tk.Label(main, text=self.vehicle.plaka,
                 font=(FONT_FAMILY, 12),
                 bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack(pady=(0, 20))

        # Sigorta Kartı
        sigorta_card = tk.Frame(main, bg=COLORS['bg_card'], padx=15, pady=12)
        sigorta_card.pack(fill=tk.X, pady=(0, 10))

        sigorta_header = tk.Frame(sigorta_card, bg=COLORS['bg_card'])
        sigorta_header.pack(fill=tk.X)

        tk.Label(sigorta_header, text="Sigorta Bitiş Tarihi",
                 font=(FONT_FAMILY, 12, "bold"),
                 bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(side=tk.LEFT)

        sigorta_tarih = self.vehicle.sigorta_bitis if self.vehicle.sigorta_bitis else "Belirlenmedi"
        sigorta_color = self._get_date_color(self.vehicle.sigorta_bitis)

        self.sigorta_label = tk.Label(sigorta_card, text=sigorta_tarih,
                                      font=(FONT_FAMILY, 14, "bold"),
                                      bg=COLORS['bg_card'], fg=sigorta_color)
        self.sigorta_label.pack(pady=(8, 5))

        StyledButton(sigorta_card, "Sigorta Yenile", self._renew_sigorta,
                     COLORS['accent'], '#ffffff', font_size=10, padx=15, pady=6).pack()

        # Kasko Kartı
        kasko_card = tk.Frame(main, bg=COLORS['bg_card'], padx=15, pady=12)
        kasko_card.pack(fill=tk.X, pady=(0, 15))

        kasko_header = tk.Frame(kasko_card, bg=COLORS['bg_card'])
        kasko_header.pack(fill=tk.X)

        tk.Label(kasko_header, text="Kasko Bitiş Tarihi",
                 font=(FONT_FAMILY, 12, "bold"),
                 bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(side=tk.LEFT)

        kasko_tarih = self.vehicle.kasko_bitis if self.vehicle.kasko_bitis else "Belirlenmedi"
        kasko_color = self._get_date_color(self.vehicle.kasko_bitis)

        self.kasko_label = tk.Label(kasko_card, text=kasko_tarih,
                                    font=(FONT_FAMILY, 14, "bold"),
                                    bg=COLORS['bg_card'], fg=kasko_color)
        self.kasko_label.pack(pady=(8, 5))

        StyledButton(kasko_card, "🔄 Kasko Yenile", self._renew_kasko,
                     COLORS['accent'], '#ffffff', font_size=10, padx=15, pady=6).pack()

        # Kapat butonu
        StyledButton(main, "✓ KAPAT", self.destroy,
                     COLORS['bg_secondary'], COLORS['text_primary'],
                     font_size=11, padx=30, pady=10).pack(pady=(5, 0))

        self.bind("<Escape>", lambda e: self.destroy())

    def _get_date_color(self, date_str):
        """Tarih durumuna göre renk döndür."""
        if not date_str:
            return COLORS['text_secondary']

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            days_left = (date - today).days

            if days_left < 0:
                return COLORS['danger']  # Süresi geçmiş
            elif days_left <= 30:
                return COLORS['warning']  # 30 gün içinde
            else:
                return COLORS['success']  # İyi durumda
        except ValueError:
            return COLORS['text_secondary']

    def _renew_sigorta(self):
        """Sigorta yenileme diyalogu aç."""
        self._open_renew_dialog("sigorta", self._update_sigorta)

    def _renew_kasko(self):
        """Kasko yenileme diyalogu aç."""
        self._open_renew_dialog("kasko", self._update_kasko)

    def _open_renew_dialog(self, insurance_type, callback):
        """Yenileme diyalogu aç."""
        dialog = RenewalDialog(self, insurance_type)
        self.wait_window(dialog)

        if dialog.result:
            callback(dialog.result)

    def _update_sigorta(self, new_date):
        """Sigorta tarihini güncelle."""
        self.data_manager.update_vehicle(self.vehicle.plaka, {'sigorta_bitis': new_date})
        self.vehicle.sigorta_bitis = new_date
        self.sigorta_label.config(text=new_date, fg=self._get_date_color(new_date))
        messagebox.showinfo("Başarılı", f"Sigorta bitiş tarihi {new_date} olarak güncellendi.")

    def _update_kasko(self, new_date):
        """Kasko tarihini güncelle."""
        self.data_manager.update_vehicle(self.vehicle.plaka, {'kasko_bitis': new_date})
        self.vehicle.kasko_bitis = new_date
        self.kasko_label.config(text=new_date, fg=self._get_date_color(new_date))
        messagebox.showinfo("Başarılı", f"Kasko bitiş tarihi {new_date} olarak güncellendi.")


class RenewalDialog(tk.Toplevel):
    """Sigorta/Kasko yenileme için tarih girişi diyalogu."""

    def __init__(self, parent, insurance_type):
        super().__init__(parent)
        self.title(f"{'Sigorta' if insurance_type == 'sigorta' else 'Kasko'} Yenile")
        self.geometry("350x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.configure(bg=COLORS['bg_primary'])
        self.insurance_type = insurance_type
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
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        type_name = "Sigorta" if self.insurance_type == "sigorta" else "Kasko"

        tk.Label(main, text=f"{type_name} Yenile",
                 font=(FONT_FAMILY, 16, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(pady=(0, 20))

        tk.Label(main, text="Yeni Bitiş Tarihi (YYYY-MM-DD):",
                 font=(FONT_FAMILY, 11),
                 bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack(anchor=tk.W)

        # Varsayılan tarih: 1 yıl sonra
        default_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

        self.date_entry = tk.Entry(main, font=(FONT_FAMILY, 12),
                                   bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                                   insertbackground=COLORS['text_primary'], relief='flat',
                                   highlightthickness=2, highlightbackground=COLORS['bg_card'],
                                   highlightcolor=COLORS['accent'])
        self.date_entry.pack(fill=tk.X, pady=(5, 20), ipady=8)
        self.date_entry.insert(0, default_date)
        self.date_entry.select_range(0, tk.END)
        self.date_entry.focus()

        # Butonlar
        btn_frame = tk.Frame(main, bg=COLORS['bg_primary'])
        btn_frame.pack()

        StyledButton(btn_frame, "✓ KAYDET", self._on_save,
                     COLORS['success'], '#ffffff', padx=25, pady=10).pack(side=tk.LEFT, padx=5)

        StyledButton(btn_frame, "✗ İPTAL", self._on_cancel,
                     COLORS['danger'], '#ffffff', padx=25, pady=10).pack(side=tk.LEFT, padx=5)

        self.bind("<Return>", lambda e: self._on_save())
        self.bind("<Escape>", lambda e: self._on_cancel())

    def _on_save(self):
        date_str = self.date_entry.get().strip()

        # Tarih formatı kontrolü
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            self.result = date_str
            self.destroy()
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih formatı!\nLütfen YYYY-MM-DD formatında girin.")

    def _on_cancel(self):
        self.result = None
        self.destroy()
