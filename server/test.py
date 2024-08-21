import paramiko
import os
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        
ssh.connect("10.104.0.52", port=os.getenv('PORT'), username=os.getenv('UBNT'), password=os.getenv('PASS_AIRMAX'))

# Comando combinado
comando = """
mca-status | grep 'deviceName=' | awk -F ',' '{print $1}' | sed 's/M5//g; s/M2//g; s/ AC//g' | cut -c 12-;
cat /tmp/system.cfg | grep 'wireless.1.scan_list.status' | cut -c 29-;
mca-status | grep 'lanSpeed=' | sed 's/[^0-9]//g';
mca-status | grep signal | cut -c 9-;
mca-status | grep ccq= | cut -c 5- | awk '{print $1/10}'
"""


stdin, stdout, stderr = ssh.exec_command(comando)

# Leer la salida completa
output = stdout.read().decode('utf-8').strip().split('\n')

# Asignar cada salida a una variable correspondiente
userName = output[0]
scanStatus = output[1]
lanSpeed = output[2]
signal = output[3]
ccq = f"{float(output[4]):.0f}"

print(f"{ccq}")