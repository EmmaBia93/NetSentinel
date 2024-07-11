from sqlalchemy.orm import sessionmaker
from database.models import Panel,Enlace, init_db

Session = init_db()
session = Session()

def get_paneles(localidad):
    """Obtiene todos los dispositivos de una localidad específica.
    Si se especifica el tipo, filtra por tipo ('panel' o 'enlace').
    """
    query = session.query(Panel).filter_by(localidad=localidad)
    return query.all()

def get_enlaces():
     return session.query(Enlace).all()

def create_panel(nombre, ip, localidad, frecuencia, tecnologia):
    """Crea un nuevo dispositivo."""
    new_device = Panel(nombre=nombre, ip=ip, localidad=localidad, frecuencia=frecuencia, tecnologia=tecnologia)
    session.add(new_device)
    session.commit()
    return new_device

def create_enlace(nombre, ip, localidad, frecuencia, tecnologia):
    """Crea un nuevo dispositivo."""
    new_device = Enlace(nombre=nombre, ip=ip, localidad=localidad, frecuencia=frecuencia, tecnologia=tecnologia)
    session.add(new_device)
    session.commit()
    return new_device

def delete_device(nombre):
    """Elimina un dispositivo por su nombre."""
    device = session.query(Panel).filter_by(nombre=nombre).first()
    if device:
        session.delete(device)
        session.commit()
        return True
    return False