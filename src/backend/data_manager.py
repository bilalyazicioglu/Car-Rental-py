import sqlite3
from src.models.vehicle import Vehicle
from src.models.user import User
from src.models.rental_history import RentalHistory

class DataManager:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._create_default_admin()

    # ---------- TABLES ----------
    def _create_tables(self):
        c = self.conn.cursor()

        c.execute("""
                  CREATE TABLE IF NOT EXISTS users
                  (
                      username
                      TEXT
                      PRIMARY
                      KEY,
                      password
                      TEXT
                      NOT
                      NULL,
                      role
                      TEXT
                      NOT
                      NULL
                  )
                  """)

        c.execute("""
                  CREATE TABLE IF NOT EXISTS vehicles
                  (
                      plaka
                      TEXT
                      PRIMARY
                      KEY,
                      marka
                      TEXT,
                      model
                      TEXT,
                      ucret
                      REAL,
                      durum
                      TEXT,
                      kiralayan
                      TEXT,
                      baslangic_tarihi
                      TEXT,
                      bitis_tarihi
                      TEXT
                  )
                  """)

        c.execute("""
                  CREATE TABLE IF NOT EXISTS rental_history
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      plaka
                      TEXT,
                      kiralayan
                      TEXT,
                      baslangic_tarihi
                      TEXT,
                      bitis_tarihi
                      TEXT,
                      toplam_ucret
                      REAL,
                      iade_tarihi
                      TEXT
                  )
                  """)

        self.conn.commit()

    # ---------- USERS ----------
    def user_exists(self, username):
        c = self.conn.execute("SELECT 1 FROM users WHERE username=?", (username,))
        return c.fetchone() is not None

    def create_user(self, username, password, role="user"):
        try:
            self.conn.execute(
                "INSERT INTO users VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.conn.commit()
            return True
        except:
            return False

    def authenticate_user(self, username, password):
        c = self.conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        row = c.fetchone()
        if not row:
            return None
        return User(row["username"], row["role"])

    # ---------- VEHICLES ----------
    def add_vehicle(self, v: Vehicle):
        """
        Vehicle objesi alır ve veritabanına ekler.
        """
        # Aynı plakaya sahip araç varsa ekleme
        if self.get_vehicle_by_plaka(v.plaka):
            return False

        self.conn.execute("""
                          INSERT INTO vehicles (plaka, marka, model, ucret, durum, kiralayan, baslangic_tarihi,
                                                bitis_tarihi)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                          """, (v.plaka, v.marka, v.model, v.ucret, v.durum, v.kiralayan, v.baslangic_tarihi,
                                v.bitis_tarihi))
        self.conn.commit()
        return True

    def get_all_vehicles(self):
        c = self.conn.execute("SELECT * FROM vehicles")
        return [Vehicle(**row) for row in map(dict, c.fetchall())]

    def get_vehicle_by_plaka(self, plaka):
        c = self.conn.execute("SELECT * FROM vehicles WHERE plaka=?", (plaka,))
        row = c.fetchone()
        return Vehicle(**row) if row else None

    def update_vehicle(self, plaka: str, data: dict):
        """Araç bilgilerini günceller. data dict içinde güncellenecek alanlar olmalı."""
        allowed_fields = ['marka', 'model', 'ucret', 'durum', 'kiralayan', 'baslangic_tarihi', 'bitis_tarihi']
        updates = []
        values = []
        for key, value in data.items():
            if key in allowed_fields:
                updates.append(f"{key}=?")
                values.append(value)
        if updates:
            values.append(plaka)
            self.conn.execute(f"UPDATE vehicles SET {', '.join(updates)} WHERE plaka=?", values)
            self.conn.commit()

    def delete_vehicle(self, plaka):
        self.conn.execute("DELETE FROM vehicles WHERE plaka=?", (plaka,))
        self.conn.commit()

    def remove_vehicle(self, plaka):
        """delete_vehicle için alias - rental_service uyumluluğu."""
        self.delete_vehicle(plaka)
        return True

    def save_vehicles(self):
        """SQLite otomatik kaydettiği için bu metod sadece uyumluluk için var."""
        self.conn.commit()

    # ---------- RENTAL HISTORY ----------
    def add_rental_history(self, h: RentalHistory):
        self.conn.execute("""
                          INSERT INTO rental_history
                          (plaka, kiralayan, baslangic_tarihi, bitis_tarihi, toplam_ucret, iade_tarihi)
                          VALUES (?, ?, ?, ?, ?, ?)
                          """, (
                              h.plaka, h.kiralayan,
                              h.baslangic_tarihi, h.bitis_tarihi,
                              h.toplam_ucret, h.iade_tarihi
                          ))
        self.conn.commit()

    def get_rental_history(self):
        c = self.conn.execute("SELECT * FROM rental_history")
        return [
            RentalHistory(
                row["plaka"],
                row["kiralayan"],
                row["baslangic_tarihi"],
                row["bitis_tarihi"],
                row["toplam_ucret"],
                row["iade_tarihi"]
            )
            for row in c.fetchall()
        ]

    def _create_default_admin(self):
        c = self.conn.execute(
            "SELECT 1 FROM users WHERE username='admin'"
        )
        if c.fetchone() is None:
            self.conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin", "admin", "admin")
            )
            self.conn.commit()

    def get_vehicles_by_status(self, durum: str):
        c = self.conn.execute("SELECT * FROM vehicles WHERE durum=?", (durum,))
        return [Vehicle(**row) for row in map(dict, c.fetchall())]
