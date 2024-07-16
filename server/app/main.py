from database.manage import get_paneles
from ssh.ssh_client import ComunicationSSH
from icmp.icmp_client import is_device_online


if __name__ == '__main__':
    devices = get_paneles('Colonia')

    ips = [panel.ip for panel in devices]

    request = is_device_online(ips)

    print(request) 


