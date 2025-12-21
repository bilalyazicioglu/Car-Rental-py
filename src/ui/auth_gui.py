import tkinter as tk
from tkinter import messagebox
from src.backend.data_manager import DataManager
from constants import COLORS

class AuthWindow(tk.Toplevel):
    def __init__(self, root, data_manager: DataManager, on_success):
        super().__init__(root)
        self.root = root
        self.dm = data_manager
        self.on_success = on_success

        self.title("Giriş")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg=COLORS['bg_primary'])

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.role = tk.StringVar(value="user")

        self._build()

    def _build(self):
        frame = tk.Frame(self, padx=30, pady=30, bg=COLORS['bg_primary'])
        frame.pack(expand=True)

        tk.Label(frame, text="Kullanıcı Adı", bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(anchor="w")
        tk.Entry(frame, textvariable=self.username, bg='#2d2d3f', fg=COLORS['text_primary'], insertbackground=COLORS['text_primary']).pack(fill="x")

        tk.Label(frame, text="Şifre", bg=COLORS['bg_primary'], fg=COLORS['text_primary']).pack(anchor="w", pady=(10, 0))
        tk.Entry(frame, textvariable=self.password, show="*", bg='#2d2d3f', fg=COLORS['text_primary'], insertbackground=COLORS['text_primary']).pack(fill="x")

        # Giriş butonu (Label tabanlı - macOS uyumlu)
        login_btn = tk.Label(frame, text="Giriş Yap", bg=COLORS['accent'], fg=COLORS['text_primary'],
                            font=("Helvetica", 11, "bold"), pady=8, cursor="hand2")
        login_btn.pack(fill="x", pady=(15, 5))
        login_btn.bind("<Button-1>", lambda e: self.login())

        # Kayıt butonu
        register_btn = tk.Label(frame, text="Kayıt Ol", bg='#2d2d3f', fg=COLORS['text_primary'],
                               font=("Helvetica", 11), pady=8, cursor="hand2")
        register_btn.pack(fill="x", pady=5)
        register_btn.bind("<Button-1>", lambda e: self.register())

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz")
            return

        user = self.dm.authenticate_user(username, password)

        if not user:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış")
            return

        self.destroy()
        self.on_success(user)

    def register(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if self.dm.user_exists(self.username.get()):
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten var")
            return

        ok = self.dm.create_user(username, password, "user")

        if ok:
            messagebox.showinfo("Başarılı", "Kayıt tamamlandı, giriş yapabilirsiniz")
        else:
            messagebox.showerror("Hata", "Kayıt başarısız")
