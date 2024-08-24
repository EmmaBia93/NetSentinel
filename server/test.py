import paramiko
from dotenv import load_dotenv
import json
import re

def __create_ssh_client(ip, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
            ssh.connect(ip, port=port, username=username, password=password)
    except paramiko.SSHException as e:
        print(f"SSH connection error: {e}")
        raise

    return ssh


load_dotenv()
ssh = __create_ssh_client("10.107.0.4",23,"ubnt","628819872cia")
command = "wstalist |grep \"lastip\""
stdin, stdout, stderr = ssh.exec_command(command=command, timeout=3)
output = stdout.read().decode("utf-8").strip()
output = json.loads(output)

for current in output:
    ip_address = current['remote']['ipaddr'][0] if "remote" in current and "ipaddr" in current["remote"] else "Desconocido"
    name = re.sub(r'\b(M5|AC)\b', '', current['remote']['hostname']).strip()
    time = current['remote']['uptime']
    distance = current['remote']['distance']
    signal = current['remote']['signal']
    lan = current['remote']['ethlist'][0]["speed"]
    
    print(f"{name},{ip_address},{time},{distance},{signal},{lan}")