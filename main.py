# main.py

import sys
from PyQt5.QtWidgets import QApplication
from src.database.db_manager import DatabaseManager
from src.ui.main_window import MainWindow

def main():
    # Inicializa o QApplication
    app = QApplication(sys.argv)
    
    # Inicializa o banco de dados
    db_manager = DatabaseManager()
    db_manager.create_tables()
    
    # Inicia a interface gráfica
    window = MainWindow()
    window.show()
    
    # Executa o loop de eventos
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()