import threading as th
import paramiko
import os
from scp import SCPClient
import concurrent.futures
from dotenv import load_dotenv
from tkinter.filedialog import askdirectory
from app.ssh.tools_aux import cantidad_horas_activo
import re
import random
import time
class ComunicationSSH:
    
        
    def __create_ssh_client(self,ip, port, username, password):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(ip, port=port, username=username, password=password)
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
            raise

        return ssh
    
    
    def backup(self,name:str,ip:str,tecno:str):
        ruta = askdirectory()
        load_dotenv()
        
        if not ruta:
            print("No se seleccionó ninguna ruta.")
            return False

        try:
            if tecno != 'AC':
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AIRMAX'))
            else:
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AC'))
           
            local_path = os.path.join(ruta, name.replace(" ", "") + ".cfg")
                       
            with SCPClient(client.get_transport()) as scp:
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
            client.close()

    
    def reboot(self, ip: str,tecno:str) -> bool:
        
        load_dotenv()
        try:
            if tecno != 'AC':
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AIRMAX'))
            else:
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AC'))
            
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
        
        
    def __info_device(self,ip: str, port: int, username: str, get_pass: str, name_device: str,tecno:str):
        
        if tecno !='AIRFIBER':
            command = "(((wstalist -p | grep -c \"mac\" ; mca-status | grep uptime | cut -c8- ;mca-status | grep lanSpeed | awk -F'[=M]' '{print $2}')| xargs echo -n)| tr \" \" \", \" )"

        else:
           command = "(((wstalist -p | grep -c \"mac\" ; mca-status | grep uptime | cut -c8- ; mca-status | ifconfig ath0 | grep txqueuelen | sed 's/.*txqueuelen:\([0-9]*\).*/\\1/') | xargs echo -n) | tr \" \" \",\")"

        client = None
        try:
            
            client =self.__create_ssh_client(ip=ip, port=port, username=username, password=get_pass)
           
            if client:
                stdin, stdout, stderr = client.exec_command(command=command, timeout=3)
                
                output = stdout.read().decode("utf-8").strip()
                error = stderr.read().decode("utf-8").strip()
               
                # Verificar estado de ejecución del comando
                code_status = stdout.channel.recv_exit_status()
                
                if code_status == 0:
                    
                    results = output.split(",")
                    
                    if len(results) == 3:
                        
                        return(f"{output},{ip},{name_device}")
                    else:
                        return (f"{output},0,{ip},{name_device}")
                else:
                    return (f"0,0,0,{ip},{name_device}")
                    
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


    def inicializacion_ssh(self,ips: list) -> dict:
        """
        La funcion recibe como parametro una lista de lista, la cual esta compuesta por:
        Nombre: El nombre del dispositivo.
        IP: Direccion del dispositivo.
        Tecnologia: Ya sea AC, M2 o M5.
        Se debe respetar ese orden al momento de armar la lista.

        Retorna: Un diccionario con la siguiente estructura:

        Nombre:{ "clientes": client_count,"ip": ip,"tiempo": cantidad_horas_activo,"velocidad": speed }
        
        """
        load_dotenv()
        def connection_wrapper(name,ip,tecno):
            
            if tecno == 'M5' or tecno =='M2':
                
                return self.__info_device(ip,os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AIRMAX'), name,tecno)
            
            else:
                
                return self.__info_device(ip,os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AC'), name,tecno)
            
        
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(ips)) as executor:
            future_to_ip = {executor.submit(connection_wrapper,name,ip,tecno): (name,ip,tecno) for name,ip,tecno in ips}
            
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
                
            
    def stations_users(self,ip,tecno):
        load_dotenv()
        
        command = "wstalist | grep 'lastip' | awk '{print $2}' | sed 's/\"/ /g' | sed 's/,//g' | xargs echo -n | tr ' ' ','"


        client = None
        try:
            if tecno != 'AC':
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AIRMAX'))
            else:
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AC'))

            
           
            if client:
                
                stdin, stdout, stderr = client.exec_command(command=command, timeout=3)
                
                output = stdout.read().decode("utf-8").strip()
                error = stderr.read().decode("utf-8").strip()
               
                # Verificar estado de ejecución del comando
                code_status = stdout.channel.recv_exit_status()
                
                if code_status == 0:
                    result = output.split(",")
                    
                    return result
            else:
                print("Failed to create SSH client.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            client.close()
 
    def connect_with_fallback(self,ip, username, passwords):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        for password in passwords:
            try:
                ssh.connect(ip, username=username, password=password,port=os.getenv('PORT'))
                return ssh  # Devuelve la conexión SSH exitosa
            except paramiko.AuthenticationException:
                print(f"Autenticación fallida para {ip} con la contraseña {password}")
            except Exception as e:
                print(f"Error al conectar con {ip}: {e}")
                break  # Sal del bucle si ocurre un error diferente
        return None  # Devuelve None si todas las conexiones fallan
    
    
    def request_info_with_fallback(self,ip):
        load_dotenv()
        username=os.getenv('UBNT')
        passwords=[os.getenv('PASS_AIRMAX'),os.getenv('PASS_AC')]
        ssh = self.connect_with_fallback(ip, username, passwords)
      
        
        if ssh is None:
            return ip, "No se pudo autenticar con ninguna contraseña"
        
        try:
            comando = """
                        mca-status | grep 'deviceName=' | awk -F ',' '{print $1}' | sed 's/M5//g; s/M2//g; s/ AC//g' | cut -c 12-;
                        cat /tmp/system.cfg | grep 'wireless.1.scan_list.status' | cut -c 29-;
                        mca-status | grep 'lanSpeed=' | sed 's/[^0-9]//g';
                        mca-status | grep signal | cut -c 9-;
                        mca-status | grep ccq= | cut -c 5- | awk '{print $1/10}'
                        mca-status | grep distance | awk -F '=' '{print $2}'
                        """
            stdin, stdout, stderr = ssh.exec_command(comando)

            
            output = stdout.read().decode('utf-8').strip().split('\n')

            
            userName = output[0]
            scanStatus = output[1]
            lanSpeed = output[2]
            signal = output[3]
            ccq = f"{float(output[4]):.0f}"
            distance = f"{int(output[5])/1000:.1f} km"
            



            
            output = f"{userName},{scanStatus},{lanSpeed},{ip},{signal},{ccq},{distance}"
            return output
        
        except TimeoutError as e:
            print(f"SSH connection timeout error: {e}")
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        finally:
            ssh.close()
    
    
    
    def request_users(self,ip,tecnologia):
        ips=self.stations_users(ip,tecnologia)
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(ips)) as executor:
            futures = {executor.submit(self.request_info_with_fallback, ip): ip for ip in ips}

            for future in concurrent.futures.as_completed(futures):
                ip = futures[future]
                try:
                    data = future.result()
                    split_text = data.split(",")
                    username,check_frec,lan,ip_user,signal,ccq,distance = split_text[0],split_text[1],split_text[2],split_text[3],split_text[4],split_text[5],split_text[6]
                    
                    results.append({'name':username,'ip':ip_user,'frequency':check_frec,'speed':lan,'signal':signal,'ccq':ccq,'distance':distance})
                except Exception as exc:
                    print(f'IP {ip} generated an exception: {exc}')
        
        return results
    
    def desmarcar_frecuencia(self,ip):
        load_dotenv()
        ssh = self.__create_ssh_client(ip=ip,port=os.getenv('PORT'),username=os.getenv('UBNT'),password=os.getenv('PASS_AIRMAX'))
        if ssh:
            
            command = "sed -i 's/^wireless.1.scan_list.status=enabled$/wireless.1.scan_list.status=disabled/' /tmp/system.cfg && cfgmtd -wp /etc"
            command1 = "reboot"
            try:
                ssh.exec_command(command=command)
                time.sleep(2)
                ssh.exec_command(command=command1)
                
                return True
            except TimeoutError as e:
                print(f"SSH connection timeout error: {e}")
                return False
            except paramiko.SSHException as e:
                print(f"SSH connection error: {e}")
                return False
            
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return False
            finally:
                ssh.close()

    def test(self,ip):
        time.sleep(1)
        return random.choice([True,False])