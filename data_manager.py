import sqlite3
import os
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Vehicle:
    plaka: str
    marka: str
    model: str
    ucret: float
    durum: str = "müsait"
    kiralayan: Optional[str] = None
    baslangic_tarihi: Optional[str] = None
    bitis_tarihi: Optional[str] = None


@dataclass
class RentalHistory:
    plaka: str
    kiralayan: str
    baslangic_tarihi: str
    bitis_tarihi: str
    toplam_ucret: float
    iade_tarihi: Optional[str] = None


class DataManager:

    def __init__(self, db_path: str = "vehicles.db"):
        self.db_path = db_path
        self._connect()
        self._create_tables()
        self._ensure_initial_data()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            plaka TEXT PRIMARY KEY,
            marka TEXT,
            model TEXT,
            ucret REAL,
            durum TEXT,
            kiralayan TEXT,
            baslangic_tarihi TEXT,
            bitis_tarihi TEXT
        )
        """)

        self.cursor.execute("""
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

    def _ensure_initial_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM vehicles")
        if self.cursor.fetchone()[0] == 0:
            sample = [
                ("34ABC123", "Toyota", "Corolla", 800, "müsait", None, None, None),
                ("06XYZ789", "Honda", "Civic", 750, "müsait", None, None, None),
                ("35DEF456", "Volkswagen", "Golf", 900, "müsait", None, None, None)
            ]
            self.cursor.executemany("""
            INSERT INTO vehicles VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, sample)
            self.conn.commit()

    # ---------- VEHICLE CRUD ----------

    def add_vehicle(self, vehicle: Vehicle) -> bool:
        try:
            self.cursor.execute("""
            INSERT INTO vehicles VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                vehicle.plaka, vehicle.marka, vehicle.model, vehicle.ucret,
                vehicle.durum, vehicle.kiralayan,
                vehicle.baslangic_tarihi, vehicle.bitis_tarihi
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_vehicle(self, plaka: str) -> bool:
        self.cursor.execute("DELETE FROM vehicles WHERE plaka = ?", (plaka,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def update_vehicle(self, plaka: str, data: dict) -> bool:
        fields = ", ".join(f"{k}=?" for k in data.keys())
        values = list(data.values()) + [plaka]
        self.cursor.execute(f"""
        UPDATE vehicles SET {fields} WHERE plaka = ?
        """, values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_vehicle_by_plaka(self, plaka: str) -> Optional[Vehicle]:
        self.cursor.execute("SELECT * FROM vehicles WHERE plaka = ?", (plaka,))
        row = self.cursor.fetchone()
        return Vehicle(**row) if row else None

    def get_all_vehicles(self) -> List[Vehicle]:
        self.cursor.execute("SELECT * FROM vehicles")
        return [Vehicle(**row) for row in self.cursor.fetchall()]

    def get_vehicles_by_status(self, status: str) -> List[Vehicle]:
        self.cursor.execute("SELECT * FROM vehicles WHERE durum = ?", (status,))
        return [Vehicle(**row) for row in self.cursor.fetchall()]

    # ---------- RENTAL HISTORY ----------

    def add_rental_history(self, history: RentalHistory):
        self.cursor.execute("""
        INSERT INTO rental_history
        (plaka, kiralayan, baslangic_tarihi, bitis_tarihi, toplam_ucret, iade_tarihi)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            history.plaka, history.kiralayan,
            history.baslangic_tarihi, history.bitis_tarihi,
            history.toplam_ucret, history.iade_tarihi
        ))
        self.conn.commit()

    def get_rental_history(self) -> List[RentalHistory]:
        self.cursor.execute("SELECT * FROM rental_history")
        return [
            RentalHistory(
                plaka=row["plaka"],
                kiralayan=row["kiralayan"],
                baslangic_tarihi=row["baslangic_tarihi"],
                bitis_tarihi=row["bitis_tarihi"],
                toplam_ucret=row["toplam_ucret"],
                iade_tarihi=row["iade_tarihi"]
            )
            for row in self.cursor.fetchall()
        ]

    def save_vehicles(self) -> bool:
        # SQLite'ta her işlem commit olduğu için dummy
        return True
