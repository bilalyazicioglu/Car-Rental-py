import json
import os
from dataclasses import dataclass, asdict, field
from typing import Optional, List
from datetime import datetime


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
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Vehicle':
        return cls(
            plaka=data.get('plaka', ''),
            marka=data.get('marka', ''),
            model=data.get('model', ''),
            ucret=float(data.get('ucret', 0)),
            durum=data.get('durum', 'müsait'),
            kiralayan=data.get('kiralayan'),
            baslangic_tarihi=data.get('baslangic_tarihi'),
            bitis_tarihi=data.get('bitis_tarihi')
        )


@dataclass
class RentalHistory:
    plaka: str
    kiralayan: str
    baslangic_tarihi: str
    bitis_tarihi: str
    toplam_ucret: float
    iade_tarihi: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RentalHistory':
        return cls(
            plaka=data.get('plaka', ''),
            kiralayan=data.get('kiralayan', ''),
            baslangic_tarihi=data.get('baslangic_tarihi', ''),
            bitis_tarihi=data.get('bitis_tarihi', ''),
            toplam_ucret=float(data.get('toplam_ucret', 0)),
            iade_tarihi=data.get('iade_tarihi')
        )


class DataManager:
    
    def __init__(self, data_file: str = "vehicles.json"):
        self.data_file = data_file
        self.vehicles: List[Vehicle] = []
        self.rental_history: List[RentalHistory] = []
        self._ensure_data_file()
        self.load_vehicles()
    
    def _ensure_data_file(self):
        if not os.path.exists(self.data_file):
            self._create_initial_data()
    
    def _create_initial_data(self):
        initial_data = {
            "vehicles": [
                {
                    "plaka": "34ABC123",
                    "marka": "Fiat",
                    "model": "Doblo",
                    "ucret": 800,
                    "durum": "müsait",
                    "kiralayan": None,
                    "baslangic_tarihi": None,
                    "bitis_tarihi": None
                },
                {
                    "plaka": "06XYZ789",
                    "marka": "Honda",
                    "model": "Civic",
                    "ucret": 750,
                    "durum": "müsait",
                    "kiralayan": None,
                    "baslangic_tarihi": None,
                    "bitis_tarihi": None
                },
                {
                    "plaka": "35DEF456",
                    "marka": "Volkswagen",
                    "model": "Passat",
                    "ucret": 900,
                    "durum": "müsait",
                    "kiralayan": None,
                    "baslangic_tarihi": None,
                    "bitis_tarihi": None
                }
            ],
            "rental_history": []
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
    
    def load_vehicles(self) -> List[Vehicle]:
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.vehicles = [Vehicle.from_dict(v) for v in data.get('vehicles', [])]
                self.rental_history = [RentalHistory.from_dict(h) for h in data.get('rental_history', [])]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Veri yüklenirken hata: {e}")
            self.vehicles = []
            self.rental_history = []
        return self.vehicles
    
    def save_vehicles(self) -> bool:
        try:
            data = {
                "vehicles": [v.to_dict() for v in self.vehicles],
                "rental_history": [h.to_dict() for h in self.rental_history]
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"Veri kaydedilirken hata: {e}")
            return False
    
    def add_vehicle(self, vehicle: Vehicle) -> bool:
        if self.get_vehicle_by_plaka(vehicle.plaka):
            return False
        self.vehicles.append(vehicle)
        return True
    
    def remove_vehicle(self, plaka: str) -> bool:
        vehicle = self.get_vehicle_by_plaka(plaka)
        if vehicle:
            self.vehicles.remove(vehicle)
            return True
        return False
    
    def update_vehicle(self, plaka: str, updated_data: dict) -> bool:
        vehicle = self.get_vehicle_by_plaka(plaka)
        if vehicle:
            for key, value in updated_data.items():
                if hasattr(vehicle, key):
                    setattr(vehicle, key, value)
            return True
        return False
    
    def get_vehicle_by_plaka(self, plaka: str) -> Optional[Vehicle]:
        for vehicle in self.vehicles:
            if vehicle.plaka == plaka:
                return vehicle
        return None
    
    def get_all_vehicles(self) -> List[Vehicle]:
        return self.vehicles
    
    def get_vehicles_by_status(self, status: str) -> List[Vehicle]:
        return [v for v in self.vehicles if v.durum == status]
    
    def add_rental_history(self, history: RentalHistory):
        self.rental_history.append(history)
    
    def get_rental_history(self) -> List[RentalHistory]:
        return self.rental_history
