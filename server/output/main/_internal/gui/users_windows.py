from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QDialog, QPushButton, QHeaderView, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QBrush
import sys
from app.ssh.ssh_client import ComunicationSSH
import threading
import webbrowser

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
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Nombre", "IP", "Frecuencia", "Cable", "Señal","CCQ",'Distancia'])
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 320)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 200)
        self.table.setColumnWidth(5, 200)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.event_double)
        layout.addWidget(self.table)

        # Agregar barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(30)  # Altura fija para la barra de progreso
        self.progress_bar.setStyleSheet("""
                                QProgressBar {
                                    border: 3px solid #2c3e50;     /* Borde */
                                    border-radius: 0px;          /* Esquinas redondeadas */
                                    background-color: #181920;     /* Color de fondo de la barra */
                                    text-align: center;            /* Texto centrado */
                                    font: bold 14px;               /* Estilo del texto */
                                    color: #2c3e50;                /* Color del texto */
                                }

                                QProgressBar::chunk {
                                    border-radius: 10px;           /* Esquinas redondeadas de la parte de progreso */
                                               
                                    
                                    background-color: qlineargradient(
                                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #1abc9c, stop:1 #16a085);   /* Degradado */
                                }
                            """)
        self.progress_bar.setRange(0, 0)  # Rango normal
        layout.addWidget(self.progress_bar)

        # Agregar botón para cerrar el diálogo (opcional)
        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet("""
                                QPushButton {
                                    background-color: '#2980b9';
                                    color: black;
                                    border: 4px solid #154360;
                                    font-size:17px;
                                    border-radius: 10px;
                                }
                                QPushButton:hover {
                                    background-color: '#1f618d';
                                    color: white;
                                }
                              
                                
                            """)
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
            self.set_table_item(row, 2, user['frequency'])
            self.set_table_item(row, 3, user['speed'] if user['speed'] else 'Desconectado')
            self.set_table_item(row, 4, user['signal'])
            self.set_table_item(row, 5, user['ccq'])
            self.set_table_item(row, 6, user['distance'])
            


        # Ocultar la barra de progreso cuando se complete la carga
        self.progress_bar.setVisible(False)

    def set_table_item(self, row, column, text):
        dic_colors = {'enabled':'#d35400','disabled':'#2ecc71','Desconectado':'#e74c3c','10':'#e74c3c','100':'#2ecc71'}
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        icon = QIcon()
        if column == 2 or column == 3:
            item.setForeground(QBrush(QColor(dic_colors[text])))
            
        if column == 4:
            if int(text) < 68:
                item.setForeground(QBrush(QColor("#2ecc71")))
            elif 68 <= int(text) <= 77:
                item.setForeground(QBrush(QColor("#f1c40f")))
            else: 
               item.setForeground(QBrush(QColor("#e74c3c"))) 
        
        
        if column == 5:
            if int(text) >= 75:
                item.setForeground(QBrush(QColor("#2ecc71")))
            elif 60 <= int(text) <= 74:
                item.setForeground(QBrush(QColor("#f1c40f")))
            else: 
               item.setForeground(QBrush(QColor("#e74c3c"))) 
        
        if column == 6:
            distancia = float(text.replace("km", "").strip())
            if distancia <= 2.0:
                item.setForeground(QBrush(QColor("#2ecc71")))
            elif distancia > 2.0 and distancia<=3.0:
                item.setForeground(QBrush(QColor("#f1c40f")))
            else:
                item.setForeground(QBrush(QColor("#e74c3c")))
        if column in [0,1]:
            item.setForeground(QBrush(QColor("#dedede")))
            
        self.table.setItem(row, column, item)
    
    def event_double(self,row,column):
        selected_row = self.table.currentRow()
        data = self.table.item(row, 1).text()
        url = f"http://{data}:83"
        webbrowser.open(url)