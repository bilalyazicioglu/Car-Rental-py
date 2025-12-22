import os
import tkinter as tk
from src.backend.data_manager import DataManager
from src.ui.auth_gui import AuthWindow
from src.ui.main_gui import CarRentalApp


def main():
    root = tk.Tk()
    root.withdraw()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "car_rental.db")

    data_manager = DataManager(db_path)

    def on_login_success(user):
        root.deiconify()
        CarRentalApp(root, current_user=user)

    def on_close():
        data_manager.cleanup_users_on_exit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    AuthWindow(root, data_manager, on_login_success)
    root.mainloop()


if __name__ == "__main__":
    main()
