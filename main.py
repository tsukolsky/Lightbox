#!/usr/bin/env python

import sys, os
from MainWindow import MainWindow
from PyQt4.QtGui import QApplication
from util.Log import Log

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setStyle('plastique')
	
	debugging = False
	mainLog = Log(debugging)
	mainWindow = MainWindow(mainLog)
	mainWindow.show()
	app.exec_()
	