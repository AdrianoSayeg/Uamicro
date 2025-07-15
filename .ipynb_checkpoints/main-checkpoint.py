import sys
from PyQt5 import QtWidgets
from interfaz import uamicro1

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = uamicro1()
    window.show()
    sys.exit(app.exec_())
