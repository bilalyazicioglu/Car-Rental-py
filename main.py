import tkinter as tk
from data_manager import DataManager
from auth_gui import AuthWindow
from gui import CarRentalApp


def start_app(user):
    app = CarRentalApp(root)
    app.current_user = user


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    dm = DataManager("car_rental.db")

    def on_login(user):
        root.deiconify()
        start_app(user)

    AuthWindow(root, dm, on_login)
    root.mainloop()
