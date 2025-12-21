from dataclasses import dataclass

@dataclass
class RentalHistory:
    plaka: str
    kiralayan: str
    baslangic_tarihi: str
    bitis_tarihi: str
    toplam_ucret: float
    iade_tarihi: str
