import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from database.manage import get_paneles, create_panel, create_enlace
from icmp.icmp_client import is_device_online
from dotenv import load_dotenv
from ssh.ssh_client import ComunicationSSH

load_dotenv()

LOCALIDADES = ["Media Agua", "Los Berros", "Cochagual", "Colonia", "Carpinteria", "Cañada", "Tres Esquinas"]

class Application(tb.Window):
    conn =  ComunicationSSH()
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Gestión de Paneles y Enlaces")
        self.geometry("800x600")
        
        # Marco del menú lateral
        self.menu_frame = ttk.Frame(self)
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Botones de localidades
        for localidad in LOCALIDADES:
            btn = ttk.Button(self.menu_frame, text=localidad, command=lambda loc=localidad: self.show_panels(loc))
            btn.pack(fill="x", pady=2)
        
        # Botones para crear panel y enlace
        self.btn_create_panel = ttk.Button(self.menu_frame, text="Crear Panel", command=self.create_panel)
        self.btn_create_panel.pack(fill="x", pady=10)
        self.btn_create_enlace = ttk.Button(self.menu_frame, text="Crear Enlace", command=self.create_enlace)
        self.btn_create_enlace.pack(fill="x", pady=2)
        
        # Botones para backup y reinicio
        self.btn_backup = ttk.Button(self.menu_frame, text="Realizar Backup", command=self.backup)
        self.btn_backup.pack(fill="x", pady=10)
        self.btn_restart = ttk.Button(self.menu_frame, text="Reiniciar Panel", command=self.restart_panel)
        self.btn_restart.pack(fill="x", pady=2)
        
        # Marco de la tabla principal
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Crear el Treeview para mostrar los paneles
        columns = ("Nombre", "IP", "Estado", "Clientes", "Horas Activo","Cable", "Frecuencia")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
       
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)
    
     # Definir los colores de las etiquetas
        self.tree.tag_configure('online_even', background='#b3ffb3', foreground='black')  # Verde claro con texto negro
        self.tree.tag_configure('online_odd', background='#66ff66', foreground='black')  # Verde oscuro con texto negro
        self.tree.tag_configure('offline_even', background='#ffb3b3', foreground='black')  # Rojo claro con texto negro
        self.tree.tag_configure('offline_odd', background='#ff6666', foreground='black')  # Rojo oscuro con texto negro
    
    def show_panels(self, localidad):
        # Limpiar los elementos existentes en el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener los paneles por localidad
        panels = get_paneles(localidad)
        
        # Verificar el estado en línea de cada IP
        panel_ips = [panel.ip for panel in panels]
        ips=[[panel.nombre,panel.ip,panel.tecnologia] for panel in panels]
        
        #online_status = is_device_online(panel_ips)
        panell={}
        
        resquest= self.conn.inicializacion_ssh(ips)
        # Insertar los datos en el Treeview
        
        
        for index, panel in enumerate(panels):
            #panell["estado"] = "Online" if online_status[panel.ip] else "Offline"
            tag = self.get_tag('Online', index)
           
            self.tree.insert("", "end", values=(
                panel.nombre, resquest[panel.nombre]['ip'], 'Online', resquest[panel.nombre]['clientes'],resquest[panel.nombre]['tiempo'], resquest[panel.nombre]['velocidad'], panel.frecuencia
            ), tags=(tag,))
    
    def get_tag(self, estado, index):
        if estado == "Online":
            return 'online_even' if index % 2 == 0 else 'online_odd'
        else:
            return 'offline_even' if index % 2 == 0 else 'offline_odd'
    
    
    def create_panel(self):
        # Lógica para crear un panel
        pass
    
    def create_enlace(self):
        # Lógica para crear un enlace
        pass
    
    def backup(self):
        # Lógica para realizar backup
        pass
    
    def restart_panel(self):
        # Lógica para reiniciar el panel seleccionado
        pass

if __name__ == "__main__":
    app = Application()
    app.mainloop()
