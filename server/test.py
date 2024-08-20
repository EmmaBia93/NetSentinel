
import threading as th
import paramiko

commad = "mca-status | grep 'deviceName=' |awk -F ',' '{print $1}'|sed 's/M5//g; s/M2//g; s/AC//g' | cut -c 12-;cat /tmp/system.cfg| grep 'wireless.1.scan_list.status' | cut -c 29-;mca-status | grep 'lanSpeed='  | sed 's/[^0-9]//g'"
command2="wstalist |grep \"lastip\" | awk '{print $2}' | sed s/\"/\ /g | sed s/,//g"

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

