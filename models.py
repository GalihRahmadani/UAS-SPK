from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Helm(Base):
    __tablename__ = "tblhelm"
    no = Column(Integer, primary_key=True)
    nama_helm = Column(String)
    harga = Column(Integer)
    berat = Column(String)
    double_visor = Column(String)
    sertifikasi = Column(String) 
    garansi = Column(String) 

    def __repr__(self):
        return f"Helm(type={self.type!r}, nama_helm={self.nama_helm!r}, harga={self.harga!r}, berat={self.berat!r}, double_visor={self.double_visor!r}, sertifikasi={self.sertifikasi!r}, garansi={self.garansi!r}, benefit={self.benefit!r})"