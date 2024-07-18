import sys
from PySide6 import QtCore
from PySide6.QtWidgets import QDialog,QLineEdit,QLabel, QVBoxLayout, QHBoxLayout, QPushButton


class EditWindow(QDialog):
    def __init__(self, parent=None):
        super(EditWindow, self).__init__(parent)
        self.setWindowTitle("Editar Dispositivo")
        self.setFixedSize(400, 600)
        self.data=[]
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Establecer márgenes
        layout.setSpacing(20) 
        
        # Campos de edición
        self.name_edit = QLineEdit()
        self.name_edit.setFixedHeight(50)
        self.name_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ip_edit = QLineEdit()
        self.ip_edit.setFixedHeight(50)
        self.ip_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.freq_edit = QLineEdit()
        self.freq_edit.setFixedHeight(50)
        self.freq_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tecno_edit = QLineEdit()
        self.tecno_edit.setFixedHeight(50)
        self.tecno_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        layout.addWidget(QLabel("Nombre:",alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("IP:",alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.ip_edit)
        layout.addWidget(QLabel("Frecuencia:",alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.freq_edit)

        layout.addWidget(QLabel("Tecnologia:",alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.tecno_edit)
        

        # Botones
        self.save_button = QPushButton("Aceptar")
        self.cancel_button = QPushButton("Cancelar")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def set_data(self, data):
        self.data=data
        self.name_edit.setText(data[0])
        self.ip_edit.setText(data[1])
        self.freq_edit.setText(data[5])
        self.tecno_edit.setText(data[6])
      

    def get_data(self):
        return [
            self.name_edit.text(),
            self.ip_edit.text(),
            self.data[2],
            self.data[3],
            self.data[4],
            self.freq_edit.text(),
            self.tecno_edit.text(),
       
        ]
