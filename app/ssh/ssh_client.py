import threading as th
import paramiko
import os
from scp import SCPClient
import concurrent.futures
import threading
from tkinter.filedialog import askdirectory
from ssh.tools_aux import cantidad_horas_activo

class ComunicationSSH:
    
        
    def create_ssh_client(self,ip, port, username, password):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(ip, port=port, username=username, password=password)
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
            raise

        return ssh
    
    
    def backup(self,ip:str,port:int,user:str,password:str,name_disp: str):
        ruta = askdirectory()
        
        if not ruta:
            print("No se seleccionó ninguna ruta.")
            return False

        try:
            
            ssh = self.create_ssh_client(ip,port,user,password)
            local_path = os.path.join(ruta, name_disp.replace(" ", "") + ".cfg")
                       
            with SCPClient(ssh.get_transport()) as scp:
                scp.get('/var/tmp/system.cfg', local_path)
        
            return True

        except paramiko.AuthenticationException as e:
            print(f"Error de autenticación: {e}")
            return False
        except paramiko.SSHException as e:
            print(f"Error SSH: {e}")
            return False
        except OSError as e:
            print(f"No se pudo realizar la transferencia \nError: {e}")
            return False
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False
        finally:
            ssh.close()

    
    def reboot(self, ip: str, port: int, username: str, get_pass: str) -> bool:
        
        try:
            client = self.create_ssh_client(ip, port, username, get_pass)
            
            if client:
                stdin, stdout, stderr = client.exec_command('reboot')
                client.close()
                return True
            else:
                print("Failed to create SSH client.")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
        
    def info_device(self,ip: str, port: int, username: str, get_pass: str, name_device: str):
        
        command = "(((wstalist -p | grep -c \"mac\" ; mca-status | grep uptime | cut -c8- ; mca-status | grep lanSpeed | cut -c10-) | xargs echo -n) | tr \" \" \",\")"
        
        client = None
        try:
            
            client =self.create_ssh_client(ip=ip, port=port, username=username, password=get_pass)
           
            if client:
                stdin, stdout, stderr = client.exec_command(command=command, timeout=3)
                
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()
                
                # Verificar estado de ejecución del comando
                code_status = stdout.channel.recv_exit_status()
                
                if code_status == 0:
                    results = output.split(",")
                    if len(results) == 3:
                        
                        return(f"{output},{ip},{name_device}")
                    else:
                        return (f"{output},0,{ip},{name_device}")
                else:
                    return (f"{error},0,{ip},{name_device}")
                    
        except TimeoutError as e:
            print(f"SSH connection timeout error: {e}")
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if client:
                client.close()


    def inicializacion_ssh(self,ips: dict, password: str, username: str) -> dict:
       
        def connection_wrapper(name,ip):
            return self.info_device(ip,23, username, password, name)
        
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(ips)) as executor:
            future_to_ip = {executor.submit(connection_wrapper, name,ip): (name,ip) for name,ip in ips.items()}
            
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    data = future.result()
                    split_text = data.split(",")
                   
                    client_count, uptime, speed, ip, name = split_text[0], int(split_text[1]), split_text[2], split_text[3], split_text[4]
                    
                    results[name] = {
                        "clientes": client_count,
                        "ip": ip,
                        "tiempo": cantidad_horas_activo(uptime),
                        "velocidad": speed
                    }
                except Exception as exc:
                    print(f'Error processing {ip}: {exc}')
        
        return results
                
            
            
 
    
    
