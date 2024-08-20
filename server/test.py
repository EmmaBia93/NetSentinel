
import threading as th
import paramiko

commad = "mca-status | grep 'deviceName=' |awk -F ',' '{print $1}'|sed 's/M5//g; s/M2//g; s/AC//g' | cut -c 12-;cat /tmp/system.cfg| grep 'wireless.1.scan_list.status' | cut -c 29-;mca-status | grep 'lanSpeed='  | sed 's/[^0-9]//g'"
command2="wstalist |grep \"lastip\" | awk '{print $2}' | sed s/\"/\ /g | sed s/,//g"

from PySide6.QtCore import Qt, QThread, Signal,QSize

from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QDialog

class DataLoader(QThread):
    data_loaded = Signal(list)

    def run(self):
        ssh_data = [
            {"name": "Usuario 1", "ip": "192.168.1.1", "frequency": True},
            {"name": "Usuario 2", "ip": "192.168.1.2", "frequency": False},
            {"name": "Usuario 3", "ip": "192.168.1.3", "frequency": True},
        ]
        self.msleep(2000)  # Simular un retraso
        self.data_loaded.emit(ssh_data)

class UserTable(QDialog):
    def __init__(self, parent=None):
        super(UserTable, self).__init__(parent)
        self.setWindowTitle("Editar Dispositivo")
        self.setFixedSize(400, 600)
        
        layout = QVBoxLayout(self)
        
        self.loading_label = QLabel(self)
        self.loading_movie = QMovie("app/gui/img/rainbow_loader.gif")
        self.loading_movie.setScaledSize(QSize(500,500))
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setFixedSize(QSize(500,500))
        self.loading_movie.start()
        layout.addWidget(self.loading_label,Qt.AlignCenter,Qt.AlignCenter)
        
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nombre", "IP", "Frecuencia"])
        layout.addWidget(self.table)
        self.table.hide()
        
        self.data_loader = DataLoader()
        self.data_loader.data_loaded.connect(self.populate_table)
        self.data_loader.start()

    def populate_table(self, ssh_data):
        self.loading_movie.stop()
        self.loading_label.hide()
        self.table.show()

        self.table.setRowCount(len(ssh_data))
        for row, user in enumerate(ssh_data):
            self.table.setItem(row, 0, QTableWidgetItem(user['name']))
            self.table.setItem(row, 1, QTableWidgetItem(user['ip']))
            frequency_item = QTableWidgetItem("Enabled" if user['frequency'] else "Disabled")
            frequency_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, frequency_item)

# Ejemplo de ejecución
if __name__ == "__main__":
    app = QApplication([])
    window = UserTable()
    window.show()
    app.exec_()
