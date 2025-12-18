import tkinter as tk
from tkinter import messagebox
from data_manager import DataManager


class AuthWindow(tk.Toplevel):
    def __init__(self, root, data_manager: DataManager, on_success):
        super().__init__(root)
        self.root = root
        self.dm = data_manager
        self.on_success = on_success

        self.title("Giriş")
        self.geometry("400x300")
        self.resizable(False, False)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.role = tk.StringVar(value="user")

        self._build()

    def _build(self):
        frame = tk.Frame(self, padx=30, pady=30)
        frame.pack(expand=True)

        tk.Label(frame, text="Kullanıcı Adı").pack(anchor="w")
        tk.Entry(frame, textvariable=self.username).pack(fill="x")

        tk.Label(frame, text="Şifre").pack(anchor="w", pady=(10, 0))
        tk.Entry(frame, textvariable=self.password, show="*").pack(fill="x")

        tk.Button(frame, text="Giriş Yap", command=self.login).pack(fill="x", pady=10)
        tk.Button(frame, text="Kayıt Ol", command=self.register).pack(fill="x")

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
