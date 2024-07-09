from sqlalchemy.orm import sessionmaker
from app.database.models import Device, init_db

Session = init_db()
session = Session()

def get_devices(localidad, tipo=None):
    """Obtiene todos los dispositivos de una localidad específica.
    Si se especifica el tipo, filtra por tipo ('panel' o 'enlace').
    """
    query = session.query(Device).filter_by(localidad=localidad)
    if tipo:
        query = query.filter_by(tipo=tipo)
    return query.all()

def create_device(nombre, ip, localidad, frecuencia, tecnologia, tipo):
    """Crea un nuevo dispositivo."""
    new_device = Device(nombre=nombre, ip=ip, localidad=localidad, frecuencia=frecuencia, tecnologia=tecnologia, tipo=tipo)
    session.add(new_device)
    session.commit()
    return new_device

def delete_device(nombre):
    """Elimina un dispositivo por su nombre."""
    device = session.query(Device).filter_by(nombre=nombre).first()
    if device:
        session.delete(device)
        session.commit()
        return True
    return False