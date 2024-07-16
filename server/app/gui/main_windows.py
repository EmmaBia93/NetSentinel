import sys
from PySide6.QtWidgets import QApplication,QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QCheckBox
from PySide6.QtCore import QFile, QTextStream, Qt
from PySide6.QtGui import QColor,QIcon
import threading
from database.manage import get_paneles
from icmp.icmp_client import is_device_online
from ssh.ssh_client import ComunicationSSH
from toggle.toogle_switch import Toggle


class MainWindow(QMainWindow):
    def __init__(self, useCustomTheme=False, themeFile=""):
        super().__init__()

        self.setWindowTitle("Gestión de Paneles")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()  # Iniciar en pantalla completa

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Menú de localidades
        menu_frame = QFrame()
        menu_frame.setFrameShape(QFrame.StyledPanel)
        menu_layout = QVBoxLayout(menu_frame)
        
        self.ssh_switch = Toggle()
        
        menu_layout.addWidget(self.ssh_switch,Qt.AlignCenter,Qt.AlignHCenter)
        
        localidades = ["Media Agua", "Los Berros", "Colonia", "Cochagual", "Carpinteria","Cañada", "Tres Esquinas"]
        for localidad in localidades:
            btn = QPushButton(localidad)
            btn.setFixedHeight(60)  # Hacer los botones más grandes
            btn.setFixedWidth(200)
            btn.clicked.connect(lambda checked, loc=localidad: self.load_data(loc))
            menu_layout.addWidget(btn)
        
        # Expandir botones verticalmente
        menu_layout.addStretch(1)
        
        main_layout.addWidget(menu_frame)
        
        # Panel derecho
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Botones superiores
        buttons_frame = QFrame()
        buttons_frame.setFrameShape(QFrame.StyledPanel)
        buttons_layout = QHBoxLayout(buttons_frame)

        button_labels = ["Editar", "Borrar", "Nuevo Enlace", "Nuevo Panel", "Backup", "Reinicio"]
        for label in button_labels:
            btn = QPushButton(label)
            buttons_layout.addWidget(btn)
        
        right_layout.addWidget(buttons_frame)
        
        # Tabla de paneles
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Nombre", "IP", "Horas Activo", "Total Clientes", "Velocidad", "Frecuencia", "Online"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

       

        # Hacer las filas seleccionables pero no editables
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

       


        right_layout.addWidget(self.table)
        
        main_layout.addWidget(right_panel)

        # Aplicar el tema personalizado si está habilitado
        if useCustomTheme:
            self.apply_theme(themeFile)
            

    def apply_theme(self, qss_file):
        file = QFile(qss_file)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())



    def load_data(self, localidad):
        # Aquí se debe implementar la lógica para cargar los datos desde la base de datos
        devices = get_paneles(localidad)
        devices_ssh = [[panel.nombre, panel.ip,panel.tecnologia] for panel in devices]
        # Obtener información del SSH y el estado online
        threading.Thread(target=self.update_table_data, args=(devices,devices_ssh)).start()

    

    def update_table_data(self, devices,devices_ssh):

       
        ssh_enabled = self.ssh_switch.StateButton()
        
        if ssh_enabled:
            conn = ComunicationSSH()
            ssh_data = conn.inicializacion_ssh(devices_ssh)
        else:
            ssh_data = {device.nombre: {"clientes": "-", "tiempo": "-", "velocidad": "-"} for device in devices}
        
        ips = [device.ip for device in devices]
        online_status = is_device_online(ips)

        # Actualizar la tabla en el hilo principal
        self.table.setRowCount(len(devices))
        for row, device in enumerate(devices):
            name = device.nombre
            ip = device.ip
            frec = device.frecuencia
            data = ssh_data.get(name, {})
            online = online_status.get(ip, False)

            self.set_table_item(row, 0, name)
            self.set_table_item(row, 1, ip)
            self.set_table_item(row, 2, str(data.get("tiempo", "-")))
            self.set_table_item(row, 3, str(data.get("clientes", "-")))
            self.set_table_item(row, 4, data.get("velocidad", "-"))
            self.set_table_item(row, 5, frec)
            self.set_table_item(row, 6, "Online" if online else "Offline")

           

    def set_table_item(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, column, item)
        
        
    
