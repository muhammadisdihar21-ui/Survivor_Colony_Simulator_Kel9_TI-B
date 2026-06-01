# CLASS SURVIVOR
# Menyimpan data survivor colony
class Survivor:
    def __init__(self, nama, energi=100, level=1, exp=0, lokasi="Camp"):
        self.nama = nama
        self.energi = energi
        self.level = level
        self.exp = exp 
        self.lokasi = lokasi

    # Mengubah object menjadi dictionary agar bisa disimpan ke file JSON
    def to_dict(self):
        return {
            "nama": self.nama,
            "energi": self.energi,
            "level": self.level,
            "exp" : self.exp,
            "lokasi": self.lokasi
        }

# CLASS AREA
# Menyimpan data area eksplorasi
class Area:
    def __init__(self, nama, sumber_daya, koordinat):
        self.nama = nama
        self.sumber_daya = sumber_daya
        self.koordinat = koordinat
