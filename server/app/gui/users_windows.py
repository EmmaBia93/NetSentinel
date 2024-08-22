from PySide6.QtWidgets import QApplication,QHBoxLayout, QTableWidget, QTableWidgetItem, QVBoxLayout, QDialog, QPushButton, QHeaderView, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QBrush
from app.gui.dialog_success import DialogSuccess
from app.gui.dialog_error import DialogError
import os
from app.ssh.ssh_client import ComunicationSSH
import threading
import webbrowser
from tkinter.filedialog import askdirectory

class UserTable(QDialog):
    def __init__(self,name ,ip, tecnologia, parent=None):
        super(UserTable, self).__init__(parent)
        self.name=name
        self.setWindowTitle(name)
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

        button_layout = QHBoxLayout()

        backup_button = QPushButton("Respaldar Información")
        backup_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: '#27ae60';
                                        color: black;
                                        border: 4px solid #229954;
                                        font-size:17px;
                                        border-radius: 10px;
                                    }
                                    QPushButton:hover {
                                        background-color: '#229954';
                                        color: white;
                                    }
                                """)
        backup_button.clicked.connect(self.backup_user_data)  
        button_layout.addWidget(backup_button)
        
        
        

        
        restart_all_button = QPushButton("Reiniciar a todos")
        restart_all_button.setStyleSheet("""
                                QPushButton {
                                    background-color: '#e74c3c';
                                    color: black;
                                    border: 4px solid #c0392b;
                                    font-size:17px;
                                    border-radius: 10px;
                                }
                                QPushButton:hover {
                                    background-color: '#c0392b';
                                    color: white;
                                }
                            """)
        restart_all_button.clicked.connect(self.restart_all_users)
        button_layout.addWidget(restart_all_button)
        
        
        restart_button = QPushButton("Reiniciar")
        restart_button.setStyleSheet("""
                            QPushButton {
                                background-color: '#f39c12';
                                color: black;
                                border: 4px solid #d68910;
                                font-size:17px;
                                border-radius: 10px;
                            }
                            QPushButton:hover {
                                background-color: '#d68910';
                                color: white;
                            }
                        """)
        restart_button.clicked.connect(self.restart_selected_user)  # Conecta a una función para reiniciar el usuario seleccionado
        button_layout.addWidget(restart_button)
        
        
        backup_button = QPushButton("Backup")
        backup_button.setStyleSheet("""
                            QPushButton {
                                background-color: '#9b59b6';
                                color: black;
                                border: 4px solid #512e5f;
                                font-size:17px;
                                border-radius: 10px;
                            }
                            QPushButton:hover {
                                background-color: '#76448a';
                                color: white;
                            }
                        """)
        backup_button.clicked.connect(self.backup_user)  # Conecta a una función para reiniciar el usuario seleccionado
        button_layout.addWidget(backup_button)
        
        
        
        
        
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
        close_button.clicked.connect(self.accept)  
        button_layout.addWidget(close_button)
        
        
        
        layout.addLayout(button_layout)

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
        if column==1:
            data = self.table.item(row, 1).text()
            url = f"http://{data}:83"
            webbrowser.open(url)
        if column==2 and self.table.item(row, 2).text() == 'enabled':
            ssh = ComunicationSSH()
            ip = self.table.item(row, 1).text()
            response = ssh.desmarcar_frecuencia(ip=ip)
            if response:
                DialogSuccess(self,"Se ha desmarcado la frecuencia con exito!!!").exec()
            else:
                DialogError(self,"No se ha podido desmarcar la frecuencia").exec()
        elif column==2 and self.table.item(row, 2).text() == 'disabled':
            DialogError(self,"Ya esta desmarcada la frecuencia").exec()

    def restart_all_users(self):
        pass
    
    def backup_user_data(self):
        ruta = askdirectory()
               
        if not ruta:
            print("No se seleccionó ninguna ruta.")
        else:
            local_path = os.path.join(ruta, self.name.replace(" ", "") + ".txt")
            with open(local_path, 'w') as archivo:
                row = self.table.rowCount()
                for fila in range(row):
                    datos_fila = []
                    for columna in [0,1]:
                        item = self.table.item(fila, columna)
                        if item is not None:
                            datos_fila.append(item.text().strip())
                        else:
                            datos_fila.append('')  # Si el item está vacío
                    linea = ','.join(datos_fila)  # Separar datos por comas (puedes cambiar el separador)
                    archivo.write(linea + '\n')  # Escribir la línea en el archivo
                linea = f"Cantidad de usuarios {row}"
                archivo.write(linea + '\n')
        
        DialogSuccess(self,"Se ha Creado el Archivo con exito!!!").exec()
    
    def restart_selected_user(self):
        row = self.table.currentRow()
        if row > 0:
            nombre = self.table.item(row,0).text()
            ssh = ComunicationSSH()
            request = ssh.reboot(self.table.item(row,1).text(),"M5")
        if request:
            
            DialogSuccess(self,f"Se ha reiniciado al Usuario: {nombre.title()}, con exito!!!").exec()
        else:
            DialogError(self,f"No se ha podido reiniciar al Usuario: {nombre.title()}").exec()
    
    def backup_user(self):
        row = self.table.currentRow()
        nombre = self.table.item(row,0).text()
        if row >0:
            ssh = ComunicationSSH()
            request = ssh.backup(nombre,self.table.item(row,1).text(),"M5")
        if request:
            nombre = self.table.item(row,0).text()
            DialogSuccess(self,f"Backup de: {nombre.title()}, con exito!!!").exec()
        else:
            DialogError(self,f"No se ha podido realizar el Backup al Usuario: {nombre.title()}").exec()