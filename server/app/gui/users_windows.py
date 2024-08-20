from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QDialog, QPushButton, QHeaderView, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QBrush
import sys
from app.ssh.ssh_client import ComunicationSSH
import threading

class UserTable(QDialog):
    def __init__(self, ip, tecnologia, parent=None):
        super(UserTable, self).__init__(parent)
        self.setWindowTitle("USUARIOS")
        self.setGeometry(100, 100, 1920, 1080)
        self.showMaximized()

        layout = QVBoxLayout(self)

        # Configurar la tabla
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "IP", "Frecuencia", "Cable"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 500)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 200)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Agregar barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Indica un proceso indeterminado
        layout.addWidget(self.progress_bar)

        # Agregar botón para cerrar el diálogo (opcional)
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.accept)  # Cierra el diálogo al hacer clic
        layout.addWidget(close_button)

        # Ejecutar la carga de datos en un hilo separado
        threading.Thread(target=self.load_datatable, args=(ip, tecnologia)).start()

    

    def load_datatable(self, ip, tecnologia):
        ssh = ComunicationSSH()
        response = ssh.request_users(ip, tecnologia)
        self.table.setRowCount(len(response))
        
        # Rellenar la tabla con datos de SSH
        for row, user in enumerate(response):
            self.set_table_item(row, 0, user['name'])
            self.set_table_item(row, 1, user['ip'])
            self.set_table_item(row, 2, user['frequency'], user['frequency'] == 'enabled')
            self.set_table_item(row, 3, user['speed'] if user['speed'] else 'Desconectado', user['speed'] != '100')

        # Ocultar la barra de progreso cuando se complete la carga
        self.progress_bar.setVisible(False)

    def set_table_item(self, row, column, text, highlight=False):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        icon = QIcon()
        if highlight:
            if column == 2 and text == 'enabled':
                item.setForeground(QBrush(QColor("#d35400")))
            elif column == 3 and text == '10':
                item.setForeground(QBrush(QColor("#e74c3c")))
            elif column == 3 and text == 'Desconectado':
                item.setForeground(QBrush(QColor("#e74c3c")))
        self.table.setItem(row, column, item)
