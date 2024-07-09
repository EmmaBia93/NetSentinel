from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Devices(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    ip = Column(String, nullable=False, unique=True)
    localidad = Column(String,nullable=False)
    frecuencia = Column(String,nullable=True)
    tecnologia = Column(String, nullable=False)
    tipo = Column(String, nullable=False)


def init_db():
    engine = create_engine('sqlite:///app/database/database.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)