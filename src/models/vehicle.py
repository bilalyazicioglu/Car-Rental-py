from dataclasses import dataclass

@dataclass
class Vehicle:
    plaka: str
    marka: str
    model: str
    ucret: float
    durum: str
    kiralayan: str | None
    baslangic_tarihi: str | None
    bitis_tarihi: str | None

    def __init__(self, plaka: str, marka: str, model: str, ucret: float, durum: str = "müsait", kiralayan: str | None = None, baslangic_tarihi: str | None = None, bitis_tarihi: str | None = None):
        self.plaka = plaka
        self.marka = marka
        self.model = model
        self.ucret = ucret
        self.durum = durum
        self.kiralayan = kiralayan
        self.baslangic_tarihi = baslangic_tarihi
        self.bitis_tarihi = bitis_tarihi