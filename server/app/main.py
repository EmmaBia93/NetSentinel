from database.manage import get_paneles
from ssh.ssh_client import ComunicationSSH
from icmp.icmp_client import is_device_online
from gui.main_windows import QApplication,MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Aplicar tema personalizado
    useCustomTheme = True
    themeFile = "dark_theme.qss"
    
    window = MainWindow(useCustomTheme, themeFile)
    
    window.show()
    
    sys.exit(app.exec())
