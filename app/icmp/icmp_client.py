from ping3 import ping

def is_device_online(ips):
   
#    return True if ping(ip,timeout=1) else False

    results = {}
    for ip in ips:
        try:
            response = ping(ip, timeout=1)
            if response:
                results[ip] = True
        except Exception as e:
            print(f"Error al intentar hacer ping a {ip}: {e}")
            results[ip] = False
    return results

