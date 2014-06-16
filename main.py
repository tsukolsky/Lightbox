#!/usr/bin/env python

import sys, os
from MainWindow import MainWindow
from PyQt4.QtGui import QApplication

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setStyle('plastique')
	
	mainWindow = MainWindow()
	mainWindow.show()
	app.exec_()
	