#!/usr/bin/env python

import sys, os
from ui.MainWindow import MainWindow
from PyQt4.QtGui import QApplication
from util.Log import Log

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setStyle('plastique')
	
	debugging = True
	mainLog = Log(debugging)
	mainWindow = MainWindow(mainLog)
	mainWindow.show()
	app.exec_()
	