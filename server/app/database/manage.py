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
    try:
        new_device = Panel(nombre=nombre, ip=ip, localidad=localidad, frecuencia=frecuencia, tecnologia=tecnologia)
        session.add(new_device)
        session.commit()
        return True
    except:
        return False

def create_enlace(nombre, ip, localidad, frecuencia, tecnologia):
    """Crea un nuevo dispositivo."""
    new_device = Enlace(nombre=nombre, ip=ip, localidad=localidad, frecuencia=frecuencia, tecnologia=tecnologia)
    session.add(new_device)
    session.commit()
    return new_device

def delete_panel(nombre):
    """Elimina un dispositivo por su nombre."""
    device = session.query(Panel).filter_by(nombre=nombre).first()
    if device:
        session.delete(device)
        session.commit()
        return True
    return False

def update_panel(ip,nuevo_nombre=None, nueva_frecuencia=None, nueva_tecnologia=None):
    try:
        # Buscar el registro por IP
        panel = session.query(Panel).filter_by(ip=ip).first()
            
         # Si el registro no existe, retornar un mensaje
        if not panel:
            return False
        
        #Actualizar los campos si se proporcionaron nuevos valores
        if nuevo_nombre:
            panel.nombre = nuevo_nombre
        if nueva_frecuencia:
            panel.frecuencia = nueva_frecuencia
        if nueva_tecnologia:
            panel.tecnologia = nueva_tecnologia
        
        # # Guardar los cambios en la base de datos
        session.commit()
        return True
    except Exception as e:
        # En caso de error, deshacer los cambios
        session.rollback()
        return False
    finally:
        session.close()