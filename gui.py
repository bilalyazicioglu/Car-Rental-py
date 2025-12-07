"""
Araç Kiralama Uygulaması - Grafiksel Kullanıcı Arayüzü
Tkinter tabanlı modern ve kullanıcı dostu arayüz.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date, timedelta
from typing import Optional
import os

from data_manager import DataManager
from rental_service import RentalService


class RentalDialog(tk.Toplevel):
    """Kiralama bilgileri giriş diyalogu."""
    
    def __init__(self, parent, vehicle_info: str):
        super().__init__(parent)
        self.title("Kiralama Başlat")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        self._create_widgets(vehicle_info)
        self._center_window()
    
    def _center_window(self):
        """Pencereyi ekranın ortasına konumla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self, vehicle_info: str):
        """Widget'ları oluştur."""
        # Ana frame
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(
            main_frame, 
            text="🚗 Kiralama Bilgileri",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Araç bilgisi
        vehicle_label = ttk.Label(
            main_frame,
            text=f"Araç: {vehicle_info}",
            font=("Helvetica", 10)
        )
        vehicle_label.pack(pady=(0, 20))
        
        # Form alanları
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Müşteri adı
        ttk.Label(form_frame, text="Müşteri Adı:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.customer_entry = ttk.Entry(form_frame, width=30)
        self.customer_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Başlangıç tarihi
        ttk.Label(form_frame, text="Başlangıç Tarihi:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.start_date_entry = ttk.Entry(form_frame, width=30)
        self.start_date_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.start_date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        
        # Bitiş tarihi
        ttk.Label(form_frame, text="Bitiş Tarihi:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.end_date_entry = ttk.Entry(form_frame, width=30)
        self.end_date_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        # Varsayılan olarak 3 gün sonrası
        default_end = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")
        self.end_date_entry.insert(0, default_end)
        
        # Tarih formatı ipucu
        hint_label = ttk.Label(
            main_frame,
            text="📅 Tarih formatı: YYYY-AA-GG (örn: 2025-12-15)",
            font=("Helvetica", 9),
            foreground="gray"
        )
        hint_label.pack(pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="✓ Kiralama Başlat",
            command=self._on_confirm
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="✗ İptal",
            command=self._on_cancel
        ).pack(side=tk.LEFT, padx=5)
        
        # Enter tuşu bağla
        self.bind("<Return>", lambda e: self._on_confirm())
        self.bind("<Escape>", lambda e: self._on_cancel())
        
        # Focus
        self.customer_entry.focus_set()
    
    def _on_confirm(self):
        """Onay butonuna basıldığında."""
        self.result = {
            'kiralayan': self.customer_entry.get(),
            'baslangic': self.start_date_entry.get(),
            'bitis': self.end_date_entry.get()
        }
        self.destroy()
    
    def _on_cancel(self):
        """İptal butonuna basıldığında."""
        self.result = None
        self.destroy()


class EditVehicleDialog(tk.Toplevel):
    """Araç düzenleme diyalogu."""
    
    def __init__(self, parent, vehicle):
        super().__init__(parent)
        self.title("Araç Düzenle")
        self.geometry("400x280")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.vehicle = vehicle
        self.result = None
        self._create_widgets()
        self._center_window()
    
    def _center_window(self):
        """Pencereyi ekranın ortasına konumla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Widget'ları oluştur."""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(
            main_frame,
            text=f"🔧 Araç Düzenle: {self.vehicle.plaka}",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X)
        
        # Marka
        ttk.Label(form_frame, text="Marka:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.marka_entry = ttk.Entry(form_frame, width=30)
        self.marka_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        self.marka_entry.insert(0, self.vehicle.marka)
        
        # Model
        ttk.Label(form_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_entry = ttk.Entry(form_frame, width=30)
        self.model_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.model_entry.insert(0, self.vehicle.model)
        
        # Ücret
        ttk.Label(form_frame, text="Günlük Ücret (TL):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ucret_entry = ttk.Entry(form_frame, width=30)
        self.ucret_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.ucret_entry.insert(0, str(self.vehicle.ucret))
        
        # Durum
        ttk.Label(form_frame, text="Durum:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.durum_combo = ttk.Combobox(
            form_frame,
            values=["müsait", "kirada", "bakımda"],
            state="readonly",
            width=27
        )
        self.durum_combo.grid(row=3, column=1, pady=5, padx=(10, 0))
        self.durum_combo.set(self.vehicle.durum)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="✓ Kaydet",
            command=self._on_save
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="✗ İptal",
            command=self._on_cancel
        ).pack(side=tk.LEFT, padx=5)
        
        self.bind("<Return>", lambda e: self._on_save())
        self.bind("<Escape>", lambda e: self._on_cancel())
    
    def _on_save(self):
        """Kaydet butonuna basıldığında."""
        self.result = {
            'marka': self.marka_entry.get(),
            'model': self.model_entry.get(),
            'ucret': self.ucret_entry.get(),
            'durum': self.durum_combo.get()
        }
        self.destroy()
    
    def _on_cancel(self):
        """İptal butonuna basıldığında."""
        self.result = None
        self.destroy()


class CarRentalApp:
    """Ana uygulama sınıfı."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🚗 Araç Kiralama Sistemi")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        # İkonları destekleyen sistemlerde pencere ikonu ayarla
        try:
            self.root.iconname("Araç Kiralama")
        except:
            pass
        
        # Veri yöneticisi ve servis
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, "vehicles.json")
        self.data_manager = DataManager(data_file)
        self.rental_service = RentalService(self.data_manager)
        
        # Stil ayarları
        self._setup_styles()
        
        # Arayüz oluştur
        self._create_widgets()
        
        # Araç listesini yükle
        self._refresh_vehicle_list()
        
        # Pencere kapatma olayı
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_styles(self):
        """Tkinter stil ayarları."""
        style = ttk.Style()
        
        # Tema seç
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'aqua' in available_themes:  # macOS
            style.theme_use('aqua')
        
        # Treeview stilleri
        style.configure("Treeview", rowheight=30, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        
        # Buton stilleri
        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"))
    
    def _create_widgets(self):
        """Ana widget'ları oluştur."""
        # Ana container
        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Üst bölüm - Başlık ve istatistikler
        self._create_header(main_container)
        
        # Orta bölüm - Sol: Form, Sağ: Liste
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Sol panel - Form
        left_panel = ttk.Frame(content_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self._create_form_panel(left_panel)
        
        # Sağ panel - Liste ve butonlar
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self._create_list_panel(right_panel)
        
        # Alt bölüm - Durum çubuğu
        self._create_status_bar(main_container)
    
    def _create_header(self, parent):
        """Başlık bölümü."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Başlık
        title_label = ttk.Label(
            header_frame,
            text="🚗 Araç Kiralama Sistemi",
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # İstatistikler frame
        stats_frame = ttk.Frame(header_frame)
        stats_frame.pack(side=tk.RIGHT)
        
        self.stats_label = ttk.Label(
            stats_frame,
            text="",
            font=("Helvetica", 10)
        )
        self.stats_label.pack()
    
    def _create_form_panel(self, parent):
        """Sol panel - Araç ekleme formu."""
        # Form başlığı
        form_title = ttk.Label(
            parent,
            text="📝 Yeni Araç Ekle",
            font=("Helvetica", 14, "bold")
        )
        form_title.pack(pady=(10, 15))
        
        # Form alanları
        form_frame = ttk.LabelFrame(parent, text="Araç Bilgileri", padding=15)
        form_frame.pack(fill=tk.X, padx=5)
        
        # Plaka
        ttk.Label(form_frame, text="Plaka:").pack(anchor=tk.W)
        self.plaka_entry = ttk.Entry(form_frame)
        self.plaka_entry.pack(fill=tk.X, pady=(2, 10))
        
        # Marka
        ttk.Label(form_frame, text="Marka:").pack(anchor=tk.W)
        self.marka_entry = ttk.Entry(form_frame)
        self.marka_entry.pack(fill=tk.X, pady=(2, 10))
        
        # Model
        ttk.Label(form_frame, text="Model:").pack(anchor=tk.W)
        self.model_entry = ttk.Entry(form_frame)
        self.model_entry.pack(fill=tk.X, pady=(2, 10))
        
        # Günlük Ücret
        ttk.Label(form_frame, text="Günlük Ücret (TL):").pack(anchor=tk.W)
        self.ucret_entry = ttk.Entry(form_frame)
        self.ucret_entry.pack(fill=tk.X, pady=(2, 10))
        
        # Ekleme butonu
        add_button = ttk.Button(
            form_frame,
            text="➕ Araç Ekle",
            command=self._add_vehicle,
            style="Accent.TButton"
        )
        add_button.pack(fill=tk.X, pady=(10, 0))
        
        # Filtre bölümü
        filter_frame = ttk.LabelFrame(parent, text="🔍 Filtre", padding=10)
        filter_frame.pack(fill=tk.X, padx=5, pady=20)
        
        ttk.Label(filter_frame, text="Durum:").pack(anchor=tk.W)
        self.filter_combo = ttk.Combobox(
            filter_frame,
            values=["Tümü", "Müsait", "Kirada", "Bakımda"],
            state="readonly"
        )
        self.filter_combo.pack(fill=tk.X, pady=(2, 10))
        self.filter_combo.set("Tümü")
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_vehicle_list())
        
        # Kaydet butonu
        save_button = ttk.Button(
            parent,
            text="💾 Verileri Kaydet",
            command=self._manual_save
        )
        save_button.pack(fill=tk.X, padx=5, pady=10, side=tk.BOTTOM)
    
    def _create_list_panel(self, parent):
        """Sağ panel - Araç listesi ve işlem butonları."""
        # Liste başlığı
        list_header = ttk.Frame(parent)
        list_header.pack(fill=tk.X, pady=(10, 5))
        
        list_title = ttk.Label(
            list_header,
            text="📋 Araç Listesi",
            font=("Helvetica", 14, "bold")
        )
        list_title.pack(side=tk.LEFT)
        
        # Yenile butonu
        refresh_btn = ttk.Button(
            list_header,
            text="🔄 Yenile",
            command=self._refresh_vehicle_list
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Treeview için frame
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview oluştur
        columns = ("plaka", "marka", "model", "ucret", "durum", "kiralayan")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )
        
        # Sütun başlıkları
        self.tree.heading("plaka", text="Plaka")
        self.tree.heading("marka", text="Marka")
        self.tree.heading("model", text="Model")
        self.tree.heading("ucret", text="Günlük Ücret")
        self.tree.heading("durum", text="Durum")
        self.tree.heading("kiralayan", text="Kiralayan")
        
        # Sütun genişlikleri
        self.tree.column("plaka", width=100, anchor=tk.CENTER)
        self.tree.column("marka", width=100, anchor=tk.CENTER)
        self.tree.column("model", width=100, anchor=tk.CENTER)
        self.tree.column("ucret", width=100, anchor=tk.CENTER)
        self.tree.column("durum", width=80, anchor=tk.CENTER)
        self.tree.column("kiralayan", width=150, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Seçim değişikliği olayı
        self.tree.bind("<<TreeviewSelect>>", self._on_selection_change)
        # Çift tıklama ile düzenleme
        self.tree.bind("<Double-1>", lambda e: self._edit_vehicle())
        
        # İşlem butonları
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.rent_button = ttk.Button(
            button_frame,
            text="🔑 Kiralama Başlat",
            command=self._start_rental,
            state=tk.DISABLED
        )
        self.rent_button.pack(side=tk.LEFT, padx=5)
        
        self.return_button = ttk.Button(
            button_frame,
            text="↩️ Aracı İade Et",
            command=self._end_rental,
            state=tk.DISABLED
        )
        self.return_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(
            button_frame,
            text="✏️ Düzenle",
            command=self._edit_vehicle,
            state=tk.DISABLED
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(
            button_frame,
            text="🗑️ Sil",
            command=self._delete_vehicle,
            state=tk.DISABLED
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)
    
    def _create_status_bar(self, parent):
        """Durum çubuğu."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(
            status_frame,
            text="Hazır",
            font=("Helvetica", 9),
            foreground="gray"
        )
        self.status_label.pack(side=tk.LEFT)
    
    def _refresh_vehicle_list(self):
        """Araç listesini yenile."""
        # Mevcut öğeleri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filtre değerini al
        filter_value = self.filter_combo.get()
        
        # Araçları al
        if filter_value == "Tümü":
            vehicles = self.rental_service.get_all_vehicles()
        elif filter_value == "Müsait":
            vehicles = self.rental_service.get_available_vehicles()
        elif filter_value == "Kirada":
            vehicles = self.rental_service.get_rented_vehicles()
        else:  # Bakımda
            vehicles = self.data_manager.get_vehicles_by_status("bakımda")
        
        # Listeye ekle
        for vehicle in vehicles:
            kiralayan_display = vehicle.kiralayan if vehicle.kiralayan else "-"
            ucret_display = f"{vehicle.ucret:.2f} TL"
            
            # Durum rengi için tag
            durum_tag = vehicle.durum.replace("ı", "i")  # Tag adları için
            
            self.tree.insert("", tk.END, values=(
                vehicle.plaka,
                vehicle.marka,
                vehicle.model,
                ucret_display,
                vehicle.durum,
                kiralayan_display
            ), tags=(durum_tag,))
        
        # Tag renkleri
        self.tree.tag_configure("müsait", background="#d4edda")
        self.tree.tag_configure("kirada", background="#fff3cd")
        self.tree.tag_configure("bakımda", background="#f8d7da")
        
        # İstatistikleri güncelle
        self._update_statistics()
        
        # Butonları devre dışı bırak
        self._update_button_states(None)
    
    def _update_statistics(self):
        """İstatistikleri güncelle."""
        stats = self.rental_service.get_statistics()
        stats_text = (
            f"📊 Toplam: {stats['toplam_arac']} | "
            f"✅ Müsait: {stats['musait_arac']} | "
            f"🚗 Kirada: {stats['kirada_arac']} | "
            f"🔧 Bakım: {stats['bakim_arac']} | "
            f"💰 Toplam Gelir: {stats['toplam_gelir']:.2f} TL"
        )
        self.stats_label.config(text=stats_text)
    
    def _on_selection_change(self, event):
        """Liste seçimi değiştiğinde."""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            plaka = item['values'][0]
            vehicle = self.data_manager.get_vehicle_by_plaka(plaka)
            self._update_button_states(vehicle)
        else:
            self._update_button_states(None)
    
    def _update_button_states(self, vehicle):
        """Seçili araca göre buton durumlarını güncelle."""
        if vehicle is None:
            self.rent_button.config(state=tk.DISABLED)
            self.return_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
        else:
            self.edit_button.config(state=tk.NORMAL)
            
            if vehicle.durum == "müsait":
                self.rent_button.config(state=tk.NORMAL)
                self.return_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.NORMAL)
            elif vehicle.durum == "kirada":
                self.rent_button.config(state=tk.DISABLED)
                self.return_button.config(state=tk.NORMAL)
                self.delete_button.config(state=tk.DISABLED)
            else:  # bakımda
                self.rent_button.config(state=tk.DISABLED)
                self.return_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.NORMAL)
    
    def _add_vehicle(self):
        """Yeni araç ekle."""
        plaka = self.plaka_entry.get()
        marka = self.marka_entry.get()
        model = self.model_entry.get()
        ucret = self.ucret_entry.get()
        
        success, message = self.rental_service.add_vehicle(plaka, marka, model, ucret)
        
        if success:
            messagebox.showinfo("Başarılı", message)
            self._clear_form()
            self._refresh_vehicle_list()
            self._set_status("Araç başarıyla eklendi")
        else:
            messagebox.showerror("Hata", message)
    
    def _clear_form(self):
        """Form alanlarını temizle."""
        self.plaka_entry.delete(0, tk.END)
        self.marka_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.ucret_entry.delete(0, tk.END)
    
    def _start_rental(self):
        """Kiralama işlemi başlat."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir araç seçin!")
            return
        
        item = self.tree.item(selected[0])
        plaka = item['values'][0]
        vehicle = self.data_manager.get_vehicle_by_plaka(plaka)
        
        if not vehicle:
            messagebox.showerror("Hata", "Araç bulunamadı!")
            return
        
        # Kiralama diyaloğunu aç
        vehicle_info = f"{vehicle.marka} {vehicle.model} ({vehicle.plaka})"
        dialog = RentalDialog(self.root, vehicle_info)
        self.root.wait_window(dialog)
        
        if dialog.result:
            success, message, total_cost = self.rental_service.start_rental(
                plaka,
                dialog.result['kiralayan'],
                dialog.result['baslangic'],
                dialog.result['bitis']
            )
            
            if success:
                messagebox.showinfo("Kiralama Başarılı", message)
                self._refresh_vehicle_list()
                self._set_status("Kiralama işlemi tamamlandı")
            else:
                messagebox.showerror("Hata", message)
    
    def _end_rental(self):
        """Kiralama işlemini bitir."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir araç seçin!")
            return
        
        item = self.tree.item(selected[0])
        plaka = item['values'][0]
        
        if messagebox.askyesno("Onay", f"'{plaka}' plakalı aracı iade almak istiyor musunuz?"):
            success, message = self.rental_service.end_rental(plaka)
            
            if success:
                messagebox.showinfo("Başarılı", message)
                self._refresh_vehicle_list()
                self._set_status("Araç başarıyla iade alındı")
            else:
                messagebox.showerror("Hata", message)
    
    def _edit_vehicle(self):
        """Araç bilgilerini düzenle."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir araç seçin!")
            return
        
        item = self.tree.item(selected[0])
        plaka = item['values'][0]
        vehicle = self.data_manager.get_vehicle_by_plaka(plaka)
        
        if not vehicle:
            messagebox.showerror("Hata", "Araç bulunamadı!")
            return
        
        # Düzenleme diyaloğunu aç
        dialog = EditVehicleDialog(self.root, vehicle)
        self.root.wait_window(dialog)
        
        if dialog.result:
            success, message = self.rental_service.update_vehicle(
                plaka,
                dialog.result['marka'],
                dialog.result['model'],
                dialog.result['ucret'],
                dialog.result['durum']
            )
            
            if success:
                messagebox.showinfo("Başarılı", message)
                self._refresh_vehicle_list()
                self._set_status("Araç bilgileri güncellendi")
            else:
                messagebox.showerror("Hata", message)
    
    def _delete_vehicle(self):
        """Aracı sil."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir araç seçin!")
            return
        
        item = self.tree.item(selected[0])
        plaka = item['values'][0]
        
        if messagebox.askyesno(
            "Silme Onayı",
            f"'{plaka}' plakalı aracı silmek istediğinizden emin misiniz?\n\nBu işlem geri alınamaz!"
        ):
            success, message = self.rental_service.delete_vehicle(plaka)
            
            if success:
                messagebox.showinfo("Başarılı", message)
                self._refresh_vehicle_list()
                self._set_status("Araç başarıyla silindi")
            else:
                messagebox.showerror("Hata", message)
    
    def _manual_save(self):
        """Manuel olarak verileri kaydet."""
        if self.data_manager.save_vehicles():
            messagebox.showinfo("Başarılı", "Veriler başarıyla kaydedildi!")
            self._set_status("Veriler kaydedildi")
        else:
            messagebox.showerror("Hata", "Veriler kaydedilirken bir hata oluştu!")
    
    def _set_status(self, message: str):
        """Durum çubuğu mesajını ayarla."""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"{message} ({current_time})")
    
    def _on_closing(self):
        """Uygulama kapatılırken."""
        if messagebox.askyesno("Çıkış", "Uygulamadan çıkmak istiyor musunuz?\n\nVeriler otomatik olarak kaydedilecek."):
            self.data_manager.save_vehicles()
            self.root.destroy()
