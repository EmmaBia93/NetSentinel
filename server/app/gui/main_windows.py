import sys
from PySide6.QtWidgets import QApplication,QDialog,QMainWindow, QWidget,QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QCheckBox
from PySide6.QtCore import QFile, QTextStream, Qt
from PySide6.QtGui import QColor,QIcon
import threading
from database.manage import get_paneles,update_panel,create_panel,delete_panel,get_enlaces
from icmp.icmp_client import is_device_online
from  ssh.ssh_client import ComunicationSSH
from toggle.toogle_switch import Toggle
from gui.edit_windows import EditWindow
from gui.delete_windows import DeletePanelDialog
from gui.new_panel import NewPanelWindows


class MainWindow(QMainWindow):
    def __init__(self, useCustomTheme=False, themeFile=""):
        super().__init__()

        self.setWindowTitle("Gestión de Paneles")
        self.setGeometry(100, 100, 1000, 700)
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
        
        localidades = ["Media Agua", "Los Berros", "Colonia", "Cochagual", "Carpinteria","Cañada", "Tres Esquinas","Enlaces"]
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
        btn_funcion = {"Editar":self.edit_selected_row,
                       "Borrar":self.borrar_device,
                       "Nuevo Enlace":self.new_enlace,
                       "Nuevo Panel":self.new_panel,
                       "Backup":self.create_backup,
                       "Reinicio":self.reboot
                       }
        

        button_labels = ["Editar", "Borrar", "Nuevo Enlace", "Nuevo Panel", "Backup", "Reinicio"]
        for label in button_labels:
            btn = QPushButton(label)
            buttons_layout.addWidget(btn)
            btn.clicked.connect(btn_funcion[label])
        
        right_layout.addWidget(buttons_frame)
        
        # Tabla de paneles
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Nombre", "IP", "Tiempo", "Clientes", "Velocidad", "Frecuencia","Tec","Live?"])
        self.table.horizontalHeader().setSectionResizeMode(7,QHeaderView.Stretch)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 200)
        self.table.setColumnWidth(5, 200)

      
        
       

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
        if localidad!="Enlaces":
            
            devices = get_paneles(localidad)
        else:
            devices = get_enlaces()
            
        devices_ssh = [[panel.nombre, panel.ip,panel.tecnologia] for panel in devices]
            
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
            tec = device.tecnologia
            data = ssh_data.get(name, {})
            online = online_status.get(ip, False)

            self.set_table_item(row, 0, name)
            self.set_table_item(row, 1, ip)
            self.set_table_item(row, 2, str(data.get("tiempo", "-")))
            self.set_table_item(row, 3, str(data.get("clientes", "-")))
            self.set_table_item(row, 4, data.get("velocidad", "-"))
            self.set_table_item(row, 5, frec)
            self.set_table_item(row, 6, tec)
            self.set_table_item(row, 7, "Online" if online else "Offline")
            

           

    def set_table_item(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, column, item)
        

    def edit_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        data = [
            self.table.item(selected_row, col).text() if self.table.item(selected_row, col) is not None else "" 
            for col in range(self.table.columnCount())
        ]

        edit_dialog = EditWindow(self)
        edit_dialog.set_data(data)
        
        if edit_dialog.exec_() == QDialog.Accepted:
            new_data = edit_dialog.get_data()
            request=update_panel(new_data[1],new_data[0],new_data[5],new_data[6])
            if request:
                QMessageBox.information(self, "Operación Exitosa", "El panel Actualizado.")
                for col in range(len(new_data)):
                    self.set_table_item(selected_row, col, new_data[col])

            else:
                QMessageBox.information(self, "Operación Cancelada", "Surgio un problema al intentar actualizar")

        
    
    def borrar_device(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        data = [
            self.table.item(selected_row, col).text() if self.table.item(selected_row, col) is not None else "" 
            for col in range(self.table.columnCount())
        ]

        dialog = DeletePanelDialog(self)
        dialog.set_data(data)
        
        if dialog.exec():
            request=delete_panel(data[0])
            if request:
                self.table.removeRow(selected_row)
                QMessageBox.information(self, "Operación Exitosa", "El panel fue eliminado.")
            else:
                QMessageBox.information(self, "Operación Cancelada", "El panel no pudo ser eliminado.")
        else:
            QMessageBox.information(self, "Operación Cancelada", "El panel no fue eliminado.")


    def new_enlace(self):
        print("soy nuevo enlace")
    
    
    def new_panel(self):
        window = NewPanelWindows(self)
    
        if window.exec() == QDialog.Accepted:
            data = window.get_data()
            
            if data:
                
                request=create_panel(data[0],data[1],data[2],data[3],data[4])

                if request:

                    print("Se Agrego correctamente el nuevo panel")
                else:
                    print("No se pudo agregar el panel")
                
                    






    def create_backup(self):
        print("soy backup")
    def reboot(self):
        print("soy reinicio")