import threading as th
import paramiko
import os
from scp import SCPClient
from tkinter.filedialog import askdirectory


class ComunicationSSH:

    def create_ssh_client(self,ip, port, username, password):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=port, username=username, password=password)
        return ssh
    
    
    def backup(self,disp: str):
        ruta = askdirectory()
        if not ruta:
            print("No se seleccionó ninguna ruta.")
            return

        try:
            
            ssh = self.create_ssh_client("10.104.0.4", 23, 'ubnt', "628819872")

            local_path = os.path.join(ruta, disp.replace(" ", "") + ".cfg")
            
            # Usar SCP para copiar el archivo desde el servidor remoto
            with SCPClient(ssh.get_transport()) as scp:
                scp.get('/var/tmp/system.cfg', local_path)
            
            print(f"Backup realizado correctamente en: {local_path}")

        except paramiko.AuthenticationException as e:
            print(f"Error de autenticación: {e}")
        except paramiko.SSHException as e:
            print(f"Error SSH: {e}")
        
        except OSError as e:
            print(f"No se pudo realizar la transferencia \nError: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            ssh.close()
