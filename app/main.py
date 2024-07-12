
import csv
from sqlalchemy.orm import sessionmaker
from database.models import init_db, Panel,Enlace
from database.manage import get_paneles, get_enlaces
from ssh.ssh_client import ComunicationSSH

if __name__ == '__main__':
    request=get_paneles("Los Berros")
   
    request = {panel.nombre : panel.ip for panel in request}
    
    conn = ComunicationSSH()



   
    


    