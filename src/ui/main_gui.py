import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

from constants import COLORS, FONT_FAMILY
from src.backend.data_manager import DataManager
from src.backend.rental_service import RentalService
from src.ui.styled_button import StyledButton

from src.ui.dialogs.edit_vehicle_dialog import EditVehicleDialog
from src.ui.dialogs.rental_dialog import RentalDialog
from src.ui.dialogs.rental_history_dialog import RentalHistoryDialog


class CarRentalApp:
    """Ana uygulama sınıfı."""

    def __init__(self, root: tk.Tk, current_user):
        self.current_user = current_user
        self.is_admin = current_user.role == "admin"
        self.root = root
        self.root.title("Araç Kiralama Sistemi")
        self.root.geometry("1300x850")
        self.root.minsize(1100, 750)
        self.root.configure(bg=COLORS['bg_primary'])

        # Veri yöneticisi
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        db_path = os.path.join(project_root, "car_rental.db")
        self.data_manager = DataManager(db_path)
        self.rental_service = RentalService(self.data_manager)

        self._running = True  # Timer kontrolü için

        self._setup_styles()
        self._create_widgets()

        self.root.after(100, self._initial_load)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _initial_load(self):
        self._refresh_vehicle_list()
        self._set_status("Veriler yüklendi")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Custom.Treeview",
                        background=COLORS['bg_secondary'],
                        foreground=COLORS['text_primary'],
                        fieldbackground=COLORS['bg_secondary'],
                        rowheight=40,
                        font=(FONT_FAMILY, 11))

        style.configure("Custom.Treeview.Heading",
                        background=COLORS['bg_card'],
                        foreground=COLORS['text_primary'],
                        font=(FONT_FAMILY, 11, "bold"))

        style.map("Custom.Treeview",
                  background=[('selected', COLORS['accent'])])

    def _create_widgets(self):
        main = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        self._create_header(main)

        content = tk.Frame(main, bg=COLORS['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, pady=15)

        # Sol panel - sabit genişlik
        left = tk.Frame(content, bg=COLORS['bg_primary'], width=280)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left.pack_propagate(False)  # Sabit genişliği koru
        self._create_form_panel(left)

        right = tk.Frame(content, bg=COLORS['bg_primary'])
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._create_list_panel(right)

        self._create_status_bar(main)

    def _create_header(self, parent):
        header = tk.Frame(parent, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 10))

        # Sol - Başlık ve Profil
        left = tk.Frame(header, bg=COLORS['bg_primary'])
        left.pack(side=tk.LEFT)

        # Üst kısım - Profil
        profile_frame = tk.Frame(left, bg=COLORS['bg_card'], padx=10, pady=5)
        profile_frame.pack(anchor=tk.W, pady=(0, 8))

        # Kullanıcı bilgisi
        role_text = "Admin" if self.is_admin else "Müşteri"
        role_color = COLORS['warning'] if self.is_admin else COLORS['text_secondary']

        tk.Label(profile_frame, text=f"{self.current_user.username}",
                 font=(FONT_FAMILY, 11, "bold"),
                 bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(profile_frame, text=role_text,
                 font=(FONT_FAMILY, 9),
                 bg=COLORS['bg_card'], fg=role_color).pack(side=tk.LEFT, padx=(0, 10))

        StyledButton(profile_frame, "Çıkış", self._logout,
                     COLORS['danger'], '#ffffff', font_size=9, padx=10, pady=3).pack(side=tk.LEFT)

        # Başlık
        tk.Label(left, text="Araç Kiralama Sistemi",
                 font=(FONT_FAMILY, 24, "bold"),
                 bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(anchor=tk.W)

        tk.Label(left, text="Filo Yönetim Platformu",
                 font=(FONT_FAMILY, 11),
                 bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack(anchor=tk.W)

        # Sağ - İstatistikler ve Butonlar
        right_frame = tk.Frame(header, bg=COLORS['bg_primary'])
        right_frame.pack(side=tk.RIGHT)

        # Kiralama Geçmişi butonu
        StyledButton(right_frame, "📋 Geçmiş", self._show_rental_history,
                     COLORS['info'], '#ffffff', font_size=10, padx=15, pady=8).pack(side=tk.LEFT, padx=(0, 15))

        stats = tk.Frame(right_frame, bg=COLORS['bg_primary'])
        stats.pack(side=tk.LEFT)

        self.stat_labels = {}
        for key, label, color in [('toplam', 'Toplam', COLORS['info']),
                                  ('musait', 'Müsait', COLORS['success']),
                                  ('kirada', 'Kirada', COLORS['warning']),
                                  ('gelir', 'Gelir', COLORS['accent'])]:
            card = tk.Frame(stats, bg=COLORS['bg_card'], padx=12, pady=8)
            card.pack(side=tk.LEFT, padx=4)

            tk.Label(card, text=label, font=(FONT_FAMILY, 9),
                     bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack()

            lbl = tk.Label(card, text="0", font=(FONT_FAMILY, 14, "bold"),
                           bg=COLORS['bg_card'], fg=color)
            lbl.pack()
            self.stat_labels[key] = lbl

    def _create_form_panel(self, parent):
        # Form kartı
        if self.is_admin:
            form_card = tk.Frame(parent, bg=COLORS['bg_card'], padx=15, pady=12)
            form_card.pack(fill=tk.X, pady=(0, 10))

            tk.Label(form_card, text="➕ Yeni Araç",
                     font=(FONT_FAMILY, 13, "bold"),
                     bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(anchor=tk.W, pady=(0, 10))

            for label, attr in [("Plaka", "plaka_entry"), ("Marka", "marka_entry"),
                                ("Model", "model_entry"), ("Ücret (TL)", "ucret_entry")]:
                tk.Label(form_card, text=label, font=(FONT_FAMILY, 10),
                         bg=COLORS['bg_card'], fg=COLORS['text_secondary']).pack(anchor=tk.W)

                entry = tk.Entry(form_card, font=(FONT_FAMILY, 10), width=22,
                                 bg=COLORS['bg_secondary'], fg=COLORS['text_primary'],
                                 insertbackground=COLORS['text_primary'], relief='flat',
                                 highlightthickness=1, highlightbackground=COLORS['bg_primary'],
                                 highlightcolor=COLORS['accent'])
                entry.pack(fill=tk.X, pady=(3, 8), ipady=5)
                setattr(self, attr, entry)

            StyledButton(form_card, "➕ EKLE", self._add_vehicle,
                         COLORS['accent'], '#ffffff', font_size=10, padx=0, pady=8).pack(fill=tk.X, pady=(3, 0))

        # Filtre kartı - daha kompakt
        filter_card = tk.Frame(parent, bg=COLORS['bg_card'], padx=15, pady=10)
        filter_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(filter_card, text="🔍 Filtre",
                 font=(FONT_FAMILY, 11, "bold"),
                 bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(anchor=tk.W, pady=(0, 6))

        self.filter_var = tk.StringVar(value="Tümü")
        for text in ["Tümü", "Müsait", "Kirada", "Bakımda"]:
            tk.Radiobutton(
                filter_card, text=text, variable=self.filter_var, value=text,
                command=self._refresh_vehicle_list,
                font=(FONT_FAMILY, 10), bg=COLORS['bg_card'], fg=COLORS['text_primary'],
                selectcolor=COLORS['bg_secondary'], activebackground=COLORS['bg_card'],
                indicatoron=0, padx=10, pady=3, width=10, relief='flat'
            ).pack(fill=tk.X, pady=1)

    def _create_list_panel(self, parent):
        card = tk.Frame(parent, bg=COLORS['bg_card'], padx=15, pady=15)
        card.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(card, bg=COLORS['bg_card'])
        header.pack(fill=tk.X, pady=(0, 10))

        tk.Label(header, text="📋 Araç Listesi",
                 font=(FONT_FAMILY, 14, "bold"),
                 bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(side=tk.LEFT)

        StyledButton(header, "🔄", self._refresh_vehicle_list,
                     COLORS['bg_secondary'], COLORS['text_primary'],
                     font_size=10, bold=False, padx=10, pady=4).pack(side=tk.RIGHT)

        # Treeview
        tree_frame = tk.Frame(card, bg=COLORS['bg_secondary'])
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("plaka", "marka", "model", "ucret", "durum", "kiralayan")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                 yscrollcommand=scrollbar.set, style="Custom.Treeview")

        for col, (text, w) in {"plaka": ("Plaka", 100), "marka": ("Marka", 100),
                               "model": ("Model", 100), "ucret": ("Ücret", 90),
                               "durum": ("Durum", 80), "kiralayan": ("Kiralayan", 120)}.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, minwidth=60, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        self.tree.bind("<<TreeviewSelect>>", self._on_selection_change)
        if self.is_admin:
            self.tree.bind("<Double-1>", lambda e: self._edit_vehicle())

        # Butonlar
        btn_frame = tk.Frame(card, bg=COLORS['bg_card'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        self.action_buttons = {}
        buttons = [
            ("🔑 KİRALA", self._start_rental, COLORS['success'], "rent"),
            ("↩️ İADE", self._end_rental, COLORS['warning'], "return"),
        ]

        if self.is_admin:
            buttons.extend([
                ("✏️ DÜZENLE", self._edit_vehicle, COLORS['info'], "edit"),
                ("🗑️ SİL", self._delete_vehicle, COLORS['danger'], "delete"),
            ])

        for text, cmd, color, key in buttons:
            btn = StyledButton(
                btn_frame, text, cmd, color, '#ffffff',
                font_size=11, padx=15, pady=10, state='disabled'
            )
            btn.pack(side=tk.LEFT, padx=(0, 8))
            self.action_buttons[key] = btn

    def _create_status_bar(self, parent):
        status = tk.Frame(parent, bg=COLORS['bg_secondary'], padx=15, pady=8)
        status.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(status, text="✓ Hazır", font=(FONT_FAMILY, 10),
                                     bg=COLORS['bg_secondary'], fg=COLORS['success'])
        self.status_label.pack(side=tk.LEFT)

        self.time_label = tk.Label(status, font=(FONT_FAMILY, 10),
                                   bg=COLORS['bg_secondary'], fg=COLORS['text_secondary'])
        self.time_label.pack(side=tk.RIGHT)
        self._update_time()

    def _update_time(self):
        if not self._running:
            return
        try:
            self.time_label.config(text=datetime.now().strftime("📅 %d.%m.%Y  🕐 %H:%M:%S"))
            self.root.after(1000, self._update_time)
        except:
            pass  # Widget yok artık

    def _refresh_vehicle_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        f = self.filter_var.get()
        if f == "Tümü":
            vehicles = self.rental_service.get_all_vehicles()
        elif f == "Müsait":
            vehicles = self.rental_service.get_available_vehicles()
        elif f == "Kirada":
            vehicles = self.rental_service.get_rented_vehicles()
        else:
            vehicles = self.data_manager.get_vehicles_by_status("bakımda")

        for v in vehicles:
            self.tree.insert("", tk.END, values=(
                v.plaka, v.marka, v.model,
                f"{v.ucret:,.0f}₺", v.durum.capitalize(),
                v.kiralayan or "—"
            ))

        self._update_statistics()
        self._update_button_states(None)

    def _update_statistics(self):
        s = self.rental_service.get_statistics()
        self.stat_labels['toplam'].config(text=str(s['toplam_arac']))
        self.stat_labels['musait'].config(text=str(s['musait_arac']))
        self.stat_labels['kirada'].config(text=str(s['kirada_arac']))
        self.stat_labels['gelir'].config(text=f"{s['toplam_gelir']:,.0f}₺")

    def _on_selection_change(self, event):
        sel = self.tree.selection()
        if sel:
            plaka = self.tree.item(sel[0])['values'][0]
            self._update_button_states(self.data_manager.get_vehicle_by_plaka(plaka))
        else:
            self._update_button_states(None)

    def _update_button_states(self, vehicle):
        for btn in self.action_buttons.values():
            btn.disable()

        if vehicle is None:
            return

        if vehicle.durum == "müsait":
            self.action_buttons['rent'].enable()
        elif vehicle.durum == "kirada":
            self.action_buttons['return'].enable()

        if self.is_admin:
            self.action_buttons['edit'].enable()

            if vehicle.durum == "müsait":
                self.action_buttons['delete'].enable()

    def _add_vehicle(self):
        ok, msg = self.rental_service.add_vehicle(
            self.plaka_entry.get(), self.marka_entry.get(),
            self.model_entry.get(), self.ucret_entry.get())

        if ok:
            messagebox.showinfo("✓ Başarılı", msg)
            for e in [self.plaka_entry, self.marka_entry, self.model_entry, self.ucret_entry]:
                e.delete(0, tk.END)
            self._refresh_vehicle_list()
            self._set_status("Araç eklendi")
        else:
            messagebox.showerror("✗ Hata", msg)

    def _start_rental(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Bir araç seçin!")
            return

        plaka = self.tree.item(sel[0])['values'][0]
        v = self.data_manager.get_vehicle_by_plaka(plaka)
        if not v:
            return

        dialog = RentalDialog(self.root, f"{v.marka} {v.model} ({v.plaka})", self.current_user.username)
        self.root.wait_window(dialog)

        if dialog.result:
            ok, msg, _ = self.rental_service.start_rental(
                plaka, dialog.result['kiralayan'],
                dialog.result['baslangic'], dialog.result['bitis'])

            if ok:
                messagebox.showinfo("✓ Başarılı", msg)
                self._refresh_vehicle_list()
            else:
                messagebox.showerror("✗ Hata", msg)

    def _end_rental(self):
        sel = self.tree.selection()
        if not sel:
            return

        plaka = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Onay", f"'{plaka}' iade alınsın mı?"):
            ok, msg = self.rental_service.end_rental(plaka)
            if ok:
                messagebox.showinfo("✓ Başarılı", msg)
                self._refresh_vehicle_list()
            else:
                messagebox.showerror("✗ Hata", msg)

    def _edit_vehicle(self):
        sel = self.tree.selection()
        if not sel:
            return

        plaka = self.tree.item(sel[0])['values'][0]
        v = self.data_manager.get_vehicle_by_plaka(plaka)
        if not v:
            return

        dialog = EditVehicleDialog(self.root, v)
        self.root.wait_window(dialog)

        if dialog.result:
            ok, msg = self.rental_service.update_vehicle(
                plaka, dialog.result['marka'], dialog.result['model'],
                dialog.result['ucret'], dialog.result['durum'])

            if ok:
                messagebox.showinfo("✓ Başarılı", msg)
                self._refresh_vehicle_list()
            else:
                messagebox.showerror("✗ Hata", msg)

    def _delete_vehicle(self):
        sel = self.tree.selection()
        if not sel:
            return

        plaka = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Silme Onayı", f"'{plaka}' silinsin mi?"):
            ok, msg = self.rental_service.delete_vehicle(plaka)
            if ok:
                messagebox.showinfo("✓ Başarılı", msg)
                self._refresh_vehicle_list()
            else:
                messagebox.showerror("✗ Hata", msg)

    def _logout(self):
        """Çıkış yap ve auth ekranına dön."""
        if messagebox.askyesno("Çıkış", "Oturumu kapatmak istiyor musunuz?"):
            # Timer'u durdur
            self._running = False

            # Tüm widget'ları temizle
            for widget in self.root.winfo_children():
                widget.destroy()

            # Ana pencereyi gizle
            self.root.withdraw()

            # Auth penceresini aç
            from src.ui.auth_gui import AuthWindow

            def on_login_success(user):
                self.root.deiconify()
                CarRentalApp(self.root, current_user=user)

            AuthWindow(self.root, self.data_manager, on_login_success)

    def _show_rental_history(self):
        """Kiralama geçmişi diyaloğunu aç."""
        RentalHistoryDialog(self.root, self.data_manager)

    def _set_status(self, msg):
        self.status_label.config(text=f"✓ {msg} ({datetime.now().strftime('%H:%M:%S')})")

    def _on_closing(self):
        if messagebox.askyesno("Çıkış", "Çıkmak istiyor musunuz?"):
            self.data_manager.cleanup_users_on_exit()
            self.root.destroy()
