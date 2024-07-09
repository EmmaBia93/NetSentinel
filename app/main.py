from database.models import init_db, Devices


def main():
    
    Session = init_db()
    session = Session()



    if not session.query(Devices).first():  # Verifica si la tabla 'devices' está vacía
        session.add_all([
            Devices(nombre='Panel1', ip='192.168.1.1', localidad='Media Agua', frecuencia='5GHz', tecnologia='AC', tipo='panel'),
            Devices(nombre='Enlace1', ip='192.168.1.2', localidad='Media Agua', frecuencia='5GHz', tecnologia='AirMax', tipo='enlace')
        ])
        session.commit()









if __name__ == '__main__':
    main()