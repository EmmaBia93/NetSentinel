from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QDialog, QPushButton,QHeaderView
from PySide6.QtCore import Qt
import sys
from app.ssh.ssh_client import ComunicationSSH
import threading
class UserTable(QDialog):
    def __init__(self,ip,tecnologia, parent=None):
        super(UserTable, self).__init__(parent)
        self.setWindowTitle("Editar Dispositivo")
        self.setGeometry(100, 100, 1920, 1080)
        self.showMaximized()
        
        layout = QVBoxLayout(self)
        ssh_data = [
            {"name": "Usuario 1", "ip": "192.168.1.1", "frequency": True},
            {"name": "Usuario 2", "ip": "192.168.1.2", "frequency": False},
            {"name": "Usuario 3", "ip": "192.168.1.3", "frequency": True},
        ]
        ssh = ComunicationSSH()
        ping_thread = threading.Thread(target=ssh.stations_users,args=(ip,tecnologia))
        ping_thread.daemon = True
        ping_thread.start()
        
        # Configurar la tabla
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setRowCount(len(ssh_data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "IP", "Frecuencia","Cable"])
        self.table.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
        self.table.setColumnWidth(0, 500)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 200)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Rellenar la tabla con datos de SSH
        for row, user in enumerate(ssh_data):
            self.set_table_item(row, 0, user['name'])
            self.set_table_item(row, 1, user['ip'])
            frequency_item = QTableWidgetItem("Enabled" if user['frequency'] else "Disabled")
            frequency_item.setTextAlignment(Qt.AlignCenter)
            self.set_table_item(row, 2, frequency_item)
            self.set_table_item(row, 3, QTableWidgetItem("0"))

        # Agregar botón para cerrar el diálogo (opcional)
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.accept)  # Cierra el diálogo al hacer clic
        layout.addWidget(close_button)


    def set_table_item(self, row, column, text):
       
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, column, item)