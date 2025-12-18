import sqlite3
from dataclasses import dataclass
from datetime import datetime


# ===================== MODELLER =====================

@dataclass
class User:
    username: str
    role: str


@dataclass
class Vehicle:
    plaka: str
    marka: str
    model: str
    ucret: float
    durum: str
    kiralayan: str | None


@dataclass
class RentalHistory:
    plaka: str
    kiralayan: str
    baslangic_tarihi: str
    bitis_tarihi: str
    toplam_ucret: float
    iade_tarihi: str


# ===================== DATA MANAGER =====================

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
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            plaka TEXT PRIMARY KEY,
            marka TEXT,
            model TEXT,
            ucret REAL,
            durum TEXT,
            kiralayan TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS rental_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plaka TEXT,
            kiralayan TEXT,
            baslangic_tarihi TEXT,
            bitis_tarihi TEXT,
            toplam_ucret REAL,
            iade_tarihi TEXT
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
        self.conn.execute("""
        INSERT INTO vehicles VALUES (?, ?, ?, ?, ?, ?)
        """, (v.plaka, v.marka, v.model, v.ucret, v.durum, v.kiralayan))
        self.conn.commit()

    def get_all_vehicles(self):
        c = self.conn.execute("SELECT * FROM vehicles")
        return [Vehicle(**row) for row in map(dict, c.fetchall())]

    def get_vehicle_by_plaka(self, plaka):
        c = self.conn.execute("SELECT * FROM vehicles WHERE plaka=?", (plaka,))
        row = c.fetchone()
        return Vehicle(**row) if row else None

    def update_vehicle(self, v: Vehicle):
        self.conn.execute("""
        UPDATE vehicles SET marka=?, model=?, ucret=?, durum=?, kiralayan=?
        WHERE plaka=?
        """, (v.marka, v.model, v.ucret, v.durum, v.kiralayan, v.plaka))
        self.conn.commit()

    def delete_vehicle(self, plaka):
        self.conn.execute("DELETE FROM vehicles WHERE plaka=?", (plaka,))
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
            
    def cleanup_users_on_exit(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE role != 'admin'")
        self.conn.commit()

