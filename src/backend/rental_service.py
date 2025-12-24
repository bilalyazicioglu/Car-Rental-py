from datetime import datetime, date
from typing import Tuple, List
from src.backend.data_manager import DataManager
from src.models.vehicle import Vehicle
from src.models.rental_history import RentalHistory


class ValidationError(Exception):
    pass


class RentalService:
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def validate_vehicle_data(self, plaka: str, marka: str, model: str, ucret: str) -> Tuple[bool, str]:
        if not plaka or not plaka.strip():
            return False, "Plaka boş olamaz!"

        if not marka or not marka.strip():
            return False, "Marka boş olamaz!"

        if not model or not model.strip():
            return False, "Model boş olamaz!"

        if not ucret or not ucret.strip():
            return False, "Günlük ücret boş olamaz!"

        try:
            ucret_float = float(ucret)
            if ucret_float <= 0:
                return False, "Günlük ücret pozitif bir sayı olmalıdır!"
        except ValueError:
            return False, "Günlük ücret geçerli bir sayı olmalıdır!"

        if self.data_manager.get_vehicle_by_plaka(plaka.strip().upper()):
            return False, f"'{plaka}' plakalı araç zaten mevcut!"

        return True, ""

    def validate_dates(self, baslangic: str, bitis: str) -> Tuple[bool, str]:
        if not baslangic or not baslangic.strip():
            return False, "Başlangıç tarihi boş olamaz!"

        if not bitis or not bitis.strip():
            return False, "Bitiş tarihi boş olamaz!"

        try:
            baslangic_date = datetime.strptime(baslangic.strip(), self.DATE_FORMAT).date()
        except ValueError:
            return False, "Başlangıç tarihi geçersiz! (Formatı: YYYY-AA-GG)"

        try:
            bitis_date = datetime.strptime(bitis.strip(), self.DATE_FORMAT).date()
        except ValueError:
            return False, "Bitiş tarihi geçersiz! (Formatı: YYYY-AA-GG)"

        if bitis_date < baslangic_date:
            return False, "Bitiş tarihi başlangıç tarihinden önce olamaz!"

        if baslangic_date < date.today():
            return False, "Başlangıç tarihi bugünden önce olamaz!"

        return True, ""

    def calculate_rental_days(self, baslangic: str, bitis: str) -> int:
        try:
            baslangic_date = datetime.strptime(baslangic, self.DATE_FORMAT).date()
            bitis_date = datetime.strptime(bitis, self.DATE_FORMAT).date()
            days = (bitis_date - baslangic_date).days + 1
            return max(1, days)
        except ValueError:
            return 1

    def calculate_total_cost(self, ucret: float, baslangic: str, bitis: str) -> float:
        days = self.calculate_rental_days(baslangic, bitis)
        return ucret * days

    def add_vehicle(self, plaka: str, marka: str, model: str, ucret: str) -> Tuple[bool, str]:
        is_valid, error_msg = self.validate_vehicle_data(plaka, marka, model, ucret)
        if not is_valid:
            return False, error_msg

        #3 ay sonrasi sigorta ve kasko bitis tarihi
        from datetime import datetime, timedelta
        today = datetime.now().date()
        three_months_later = today + timedelta(days=90)
        insurance_date = three_months_later.strftime("%Y-%m-%d")

        vehicle = Vehicle(
            plaka=plaka.strip().upper(),
            marka=marka.strip(),
            model=model.strip(),
            ucret=float(ucret),
            sigorta_bitis=insurance_date,
            kasko_bitis=insurance_date
        )

        if self.data_manager.add_vehicle(vehicle):
            return True, f"'{vehicle.plaka}' plakalı araç başarıyla eklendi! (Sigorta/Kasko: {insurance_date})"
        else:
            return False, "Araç eklenirken bir hata oluştu!"

    def start_rental(self, plaka: str, kiralayan: str, baslangic: str, bitis: str) -> Tuple[bool, str, float]:
        vehicle = self.data_manager.get_vehicle_by_plaka(plaka)
        if not vehicle:
            return False, "Araç bulunamadı!", 0

        if vehicle.durum != "müsait":
            return False, f"Bu araç şu anda '{vehicle.durum}' durumunda. Kiralama yapılamaz!", 0

        if not kiralayan or not kiralayan.strip():
            return False, "Müşteri adı boş olamaz!", 0

        is_valid, error_msg = self.validate_dates(baslangic, bitis)
        if not is_valid:
            return False, error_msg, 0

        total_cost = self.calculate_total_cost(vehicle.ucret, baslangic, bitis)
        days = self.calculate_rental_days(baslangic, bitis)

        self.data_manager.update_vehicle(plaka, {
            'durum': 'kirada',
            'kiralayan': kiralayan.strip(),
            'baslangic_tarihi': baslangic,
            'bitis_tarihi': bitis
        })
        self.data_manager.save_vehicles()

        message = (
            f"Kiralama başarıyla tamamlandı!\n\n"
            f"Araç: {vehicle.marka} {vehicle.model} ({vehicle.plaka})\n"
            f"Müşteri: {kiralayan}\n"
            f"Süre: {days} gün\n"
            f"Günlük Ücret: {vehicle.ucret:.2f} TL\n"
            f"Toplam Ücret: {total_cost:.2f} TL"
        )

        return True, message, total_cost

    def end_rental(self, plaka: str) -> Tuple[bool, str]:
        vehicle = self.data_manager.get_vehicle_by_plaka(plaka)
        if not vehicle:
            return False, "Araç bulunamadı!"

        if vehicle.durum != "kirada":
            return False, "Bu araç zaten kirada değil!"

        # Kiralayan bilgisini değişkene kaydet
        old_kiralayan = vehicle.kiralayan or "Bilinmiyor"

        if vehicle.baslangic_tarihi and vehicle.bitis_tarihi:
            total_cost = self.calculate_total_cost(
                vehicle.ucret,
                vehicle.baslangic_tarihi,
                vehicle.bitis_tarihi
            )
            history = RentalHistory(
                plaka=vehicle.plaka,
                kiralayan=vehicle.kiralayan or "",
                baslangic_tarihi=vehicle.baslangic_tarihi,
                bitis_tarihi=vehicle.bitis_tarihi,
                toplam_ucret=total_cost,
                iade_tarihi=datetime.now().strftime(self.DATE_FORMAT)
            )
            self.data_manager.add_rental_history(history)

        self.data_manager.update_vehicle(plaka, {
            'durum': 'müsait',
            'kiralayan': None,
            'baslangic_tarihi': None,
            'bitis_tarihi': None
        })
        self.data_manager.save_vehicles()

        return True, f"'{plaka}' plakalı araç başarıyla iade alındı!\nMüşteri: {old_kiralayan}"

    def delete_vehicle(self, plaka: str) -> Tuple[bool, str]:
        vehicle = self.data_manager.get_vehicle_by_plaka(plaka)
        if not vehicle:
            return False, "Araç bulunamadı!"

        if vehicle.durum == "kirada":
            return False, "Kirada olan araç silinemez! Önce iade alınmalıdır."

        if self.data_manager.remove_vehicle(plaka):
            self.data_manager.save_vehicles()
            return True, f"'{plaka}' plakalı araç başarıyla silindi!"

        return False, "Araç silinirken bir hata oluştu!"

    def update_vehicle(self, plaka: str, marka: str, model: str, ucret: str, durum: str) -> Tuple[bool, str]:
        vehicle = self.data_manager.get_vehicle_by_plaka(plaka)
        if not vehicle:
            return False, "Araç bulunamadı!"

        if not marka or not marka.strip():
            return False, "Marka boş olamaz!"

        if not model or not model.strip():
            return False, "Model boş olamaz!"

        try:
            ucret_float = float(ucret)
            if ucret_float <= 0:
                return False, "Günlük ücret pozitif bir sayı olmalıdır!"
        except ValueError:
            return False, "Günlük ücret geçerli bir sayı olmalıdır!"

        valid_statuses = ["müsait", "kirada", "bakımda"]
        if durum not in valid_statuses:
            return False, f"Geçersiz durum! ({', '.join(valid_statuses)})"

        self.data_manager.update_vehicle(plaka, {
            'marka': marka.strip(),
            'model': model.strip(),
            'ucret': ucret_float,
            'durum': durum
        })
        self.data_manager.save_vehicles()

        return True, f"'{plaka}' plakalı araç başarıyla güncellendi!"

    def get_available_vehicles(self) -> List[Vehicle]:
        return self.data_manager.get_vehicles_by_status("müsait")

    def get_rented_vehicles(self) -> List[Vehicle]:
        return self.data_manager.get_vehicles_by_status("kirada")

    def get_all_vehicles(self) -> List[Vehicle]:
        return self.data_manager.get_all_vehicles()

    def get_statistics(self) -> dict:
        all_vehicles = self.get_all_vehicles()
        rental_history = self.data_manager.get_rental_history()

        total_income = sum(h.toplam_ucret for h in rental_history)

        return {
            'toplam_arac': len(all_vehicles),
            'musait_arac': len(self.get_available_vehicles()),
            'kirada_arac': len(self.get_rented_vehicles()),
            'bakim_arac': len(self.data_manager.get_vehicles_by_status("bakımda")),
            'toplam_kiralama': len(rental_history),
            'toplam_gelir': total_income
        }
