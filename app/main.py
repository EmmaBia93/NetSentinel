import csv 
import csv
from sqlalchemy.orm import sessionmaker
from database.models import init_db, Devices

def load_devices_from_txt(file_path):
    # Inicializar la base de datos y crear una sesión
    Session = init_db()
    session = Session()

    with open(file_path, newline='') as csvfile:
        device_reader = csv.DictReader(csvfile)
        
        for row in device_reader:
            device = Devices(
                nombre=row['nombre'],
                ip=row['ip'],
                frecuencia=row['frecuencia'],
                tecnologia=row['tecnologia'],
                localidad=row['localidad'],
                tipo=row['tipo']
            )
            session.add(device)

    # Confirmar los cambios en la base de datos
    session.commit()
    session.close()

# Ejemplo de uso
if __name__ == '__main__':
    load_devices_from_txt('C:\\Users\\PC\\Documents\\repositorio\\PanelesPY\\dispositivos.txt')
    print("Datos cargados exitosamente")