"""
Araç Kiralama Uygulaması - Grafiksel Kullanıcı Arayüzü
Modern, Responsive ve macOS uyumlu arayüz.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import os
import platform

from data_manager import DataManager
from rental_service import RentalService


# Renk paleti
COLORS = {
    'bg_primary': '#1e1e2e',
    'bg_secondary': '#2d2d3f',
    'bg_card': '#3d3d5c',
    'accent': '#7c3aed',
    'accent_hover': '#8b5cf6',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0c0',
    'text_dark': '#1e1e2e',
    'success': '#22c55e',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
}

FONT_FAMILY = "Helvetica"
IS_MACOS = platform.system() == 'Darwin'


class StyledButton(tk.Frame):
    """macOS uyumlu özel buton widget'ı."""
    
    def __init__(self, parent, text, command, bg_color, fg_color='#ffffff', 
                 font_size=11, bold=True, padx=20, pady=10, state='normal', **kwargs):
        super().__init__(parent, bg=parent.cget('bg') if hasattr(parent, 'cget') else COLORS['bg_primary'])
        
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.disabled_bg = '#555555'
        self.disabled_fg = '#888888'
        self._state = state
        
        font_weight = "bold" if bold else "normal"
        self.label = tk.Label(
            self, text=text,
            font=(FONT_FAMILY, font_size, font_weight),
            bg=bg_color, fg=fg_color,
            padx=padx, pady=pady, cursor='hand2'
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        self.label.bind('<Button-1>', self._on_click)
        self.label.bind('<Enter>', self._on_enter)
        self.label.bind('<Leave>', self._on_leave)
        
        if state == 'disabled':
            self.disable()
    
    def _on_click(self, event):
        if self._state == 'normal' and self.command:
            self.command()
    
    def _on_enter(self, event):
        if self._state == 'normal':
            # Rengi biraz açıklaştır
            self.label.config(bg=self._lighten_color(self.bg_color))
    
    def _on_leave(self, event):
        if self._state == 'normal':
            self.label.config(bg=self.bg_color)
        else:
            self.label.config(bg=self.disabled_bg)
    
    def _lighten_color(self, color):
        """Rengi biraz açıklaştır."""
        try:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return color
    
    def enable(self):
        self._state = 'normal'
        self.label.config(bg=self.bg_color, fg=self.fg_color, cursor='hand2')
    
    def disable(self):
        self._state = 'disabled'
        self.label.config(bg=self.disabled_bg, fg=self.disabled_fg, cursor='arrow')
    
    def config(self, **kwargs):
        if 'state' in kwargs:
            if kwargs['state'] == tk.NORMAL or kwargs['state'] == 'normal':
                self.enable()
            else:
                self.disable()


class RentalDialog(tk.Toplevel):
    """Kiralama bilgileri giriş diyalogu."""
    
    def __init__(self, parent, vehicle_info: str):
        super().__init__(parent)
        self.title("Kiralama Başlat")
        self.geometry("550x520")
        self.resizable(True, True)
        self.minsize(500, 480)
        self.transient(parent)
        self.grab_set()
        
        self.configure(bg=COLORS['bg_primary'])
        
        self.result = None
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
            ("Müşteri Adı:", "customer_entry", ""),
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
        self.result = {
            'kiralayan': self.customer_entry.get(),
            'baslangic': self.start_date_entry.get(),
            'bitis': self.end_date_entry.get()
        }
        self.destroy()
    
    def _on_cancel(self):
        self.result = None
        self.destroy()


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


class CarRentalApp:
    """Ana uygulama sınıfı."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Araç Kiralama Sistemi")
        self.root.geometry("1300x850")
        self.root.minsize(1100, 750)
        self.root.configure(bg=COLORS['bg_primary'])
        
        # Veri yöneticisi
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_manager = DataManager(os.path.join(script_dir, "vehicles.json"))
        self.rental_service = RentalService(self.data_manager)
        
        self._setup_styles()
        self._create_widgets()
        
        self.root.after(100, self._initial_load)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _initial_load(self):
        self.data_manager.load_vehicles()
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
        
        # Sol
        left = tk.Frame(header, bg=COLORS['bg_primary'])
        left.pack(side=tk.LEFT)
        
        tk.Label(left, text="Araç Kiralama Sistemi",
                font=(FONT_FAMILY, 24, "bold"),
                bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(anchor=tk.W)
        
        tk.Label(left, text="Filo Yönetim Platformu",
                font=(FONT_FAMILY, 11),
                bg=COLORS['bg_primary'], fg=COLORS['text_secondary']).pack(anchor=tk.W)
        
        # Sağ - İstatistikler
        stats = tk.Frame(header, bg=COLORS['bg_primary'])
        stats.pack(side=tk.RIGHT)
        
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
        # Form kartı - daha kompakt
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
        
        # Kaydet
        StyledButton(parent, "💾 KAYDET", self._manual_save,
                    COLORS['bg_card'], COLORS['text_primary'], 
                    font_size=10, bold=False, pady=8).pack(fill=tk.X, side=tk.BOTTOM)
    
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
        self.tree.bind("<Double-1>", lambda e: self._edit_vehicle())
        
        # Butonlar
        btn_frame = tk.Frame(card, bg=COLORS['bg_card'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.action_buttons = {}
        for text, cmd, color, key in [
            ("🔑 KİRALA", self._start_rental, COLORS['success'], "rent"),
            ("↩️ İADE", self._end_rental, COLORS['warning'], "return"),
            ("✏️ DÜZENLE", self._edit_vehicle, COLORS['info'], "edit"),
            ("🗑️ SİL", self._delete_vehicle, COLORS['danger'], "delete")
        ]:
            btn = StyledButton(btn_frame, text, cmd, color, '#ffffff',
                              font_size=11, padx=15, pady=10, state='disabled')
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
        self.time_label.config(text=datetime.now().strftime("📅 %d.%m.%Y  🕐 %H:%M:%S"))
        self.root.after(1000, self._update_time)
    
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
        if vehicle is None:
            for btn in self.action_buttons.values():
                btn.disable()
        else:
            self.action_buttons['edit'].enable()
            
            if vehicle.durum == "müsait":
                self.action_buttons['rent'].enable()
                self.action_buttons['return'].disable()
                self.action_buttons['delete'].enable()
            elif vehicle.durum == "kirada":
                self.action_buttons['rent'].disable()
                self.action_buttons['return'].enable()
                self.action_buttons['delete'].disable()
            else:
                self.action_buttons['rent'].disable()
                self.action_buttons['return'].disable()
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
        
        dialog = RentalDialog(self.root, f"{v.marka} {v.model} ({v.plaka})")
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
    
    def _manual_save(self):
        if self.data_manager.save_vehicles():
            messagebox.showinfo("✓ Başarılı", "Veriler kaydedildi!")
            self._set_status("Kaydedildi")
        else:
            messagebox.showerror("Hata", "Kaydetme hatası!")
    
    def _set_status(self, msg):
        self.status_label.config(text=f"✓ {msg} ({datetime.now().strftime('%H:%M:%S')})")
    
    def _on_closing(self):
        if messagebox.askyesno("Çıkış", "Çıkmak istiyor musunuz?"):
            self.data_manager.save_vehicles()
            self.root.destroy()
