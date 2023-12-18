from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Helm(Base):
    __tablename__ = "tblhelm"
    no = Column(Integer, primary_key=True)
    nama_helm = Column(String(255))
    harga = Column(String(255))
    berat = Column(String(255))
    double_visor = Column(String(255))
    sertifikasi = Column(String(255))
    garansi = Column(String(255))

    def __init__(self, no, nama_helm, harga, berat, double_visor, sertifikasi, garansi):
        self.no = no
        self.nama_helm = nama_helm
        self.harga = harga
        self.berat = berat
        self.double_visor = double_visor
        self.sertifikasi = sertifikasi
        self.garansi = garansi

    def calculate_score(self, dev_scale):
        score = 0
        score -= self.harga * dev_scale['harga']
        score += self.berat * dev_scale['berat']
        score += self.double_visor * dev_scale['double_visor']
        score += self.sertifikasi * dev_scale['sertifikasi']
        score += self.garansi * dev_scale['garansi']
        return score

    def __repr__(self):
        return f"Helm(no={self.no!r}, nama_helm={self.nama_helm!r}, harga={self.harga!r}, berat={self.berat!r}, double_visor={self.double_visor!r}, sertifikasi={self.sertifikasi!r}, garansi={self.garansi!r})"
