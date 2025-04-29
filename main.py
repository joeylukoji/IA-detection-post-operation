import sys
import os # Besoin de os pour vérifier l'existence de la feuille de style
from PyQt5.QtWidgets import QApplication
from ui_main import MainWindow
import qdarkstyle # Importer QDarkStyle
from dotenv import load_dotenv # Importer load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def main():
    app = QApplication(sys.argv)

    # Appliquer le thème QDarkStyle
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
