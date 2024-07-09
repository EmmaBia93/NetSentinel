from ping3 import ping

def is_device_online(ip):
    """Verifica si una dirección IP responde a una solicitud ICMP (ping).
    
    Args:
        ip (str): La dirección IP del dispositivo a verificar.
        
    Returns:
        bool: True si el dispositivo responde al ping, False en caso contrario.
    """
    try:
        response = ping(ip, timeout=2)
        return response is not None
    
    except Exception as e:
        print(f"Error al intentar hacer ping a {ip}: {e}")
        return False
    


