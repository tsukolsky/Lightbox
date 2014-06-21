from PyQt4.QtGui import QMainWindow, QWidget, QHBoxLayout, QPushButton, QTabBar, \
                        QTabWidget, QVBoxLayout, QMenuBar, QAction, QIcon, QLabel, QFont, \
                        QMessageBox, QPixmap
                        
from PyQt4.QtCore import Qt, SIGNAL
import sys
from PyQt4.QtGui import QApplication
from util.Log import Log
from util.Settings import *
from util.MyPushButton import MyPushButton
from Pattern import Pattern

BUTTONS_PER_ROW = 3
MIN_BUTTON_HEIGHT = 100
MIN_BUTTON_WIDTH = 250
STST_BUTTON_HEIGHT = 80
STST_BUTTON_WIDTH = 140
ADD_PATTERN_ENABLED = False
PATTERN_PREAMBLE = "Selected Pattern: "
NO_PATTERN_SELECTED = "None Selected"

class MainWindow(QMainWindow):
    FILE_MENU = "&File"
    EXIT_MENU = "E&xit"
    ADD_MENU = "Add &Pattern"
    DELETE_MENU = "&Delete"
    VERSION_MENU = "&Version"
    ABOUT_MENU = "&About"
    
    ## __init__ ---------------------------------------------------------
    def __init__(self, Log = None):
        # Make Main window
        QMainWindow.__init__(self, None)
        self.setWindowTitle("Lightbox")
        self.resize(800, 480)       # Screen Size
        self.__log = Log
        self.__logTitle = "MainWindow"
        if self.__log == None:
            print "No Log File"
            self.close()
            
        # Create main layout for window
        mainWidget = QWidget(self)
        self.__mainLayout = QVBoxLayout(mainWidget)
        mainWidget.setLayout(self.__mainLayout)
      
        # Add Menu Bard
        self.__menu = self.__createMenu()

        ## Toolbar that is always there->Selected Pattern, Start, Stop, Current State Label
        self.__statusLayout = self.__createStatusLayout()

        
        self.__mainLayout.addLayout(self.__statusLayout)
       # mainLayout.addWidget(self.__tabs)
        
        self.__patterns = list()
        self.__buttons = list()
        
        self.__defaultButtonLayout = QVBoxLayout()
        self.__makeDefaultButtons()
        
        # Connect MyPushButton signals
        self.connect(self, SIGNAL("buttonXClicked(PyQt_PyObject)"), self.__buttonXClicked)

        # Make the window knwo what is the main widget
        self.setCentralWidget(mainWidget)


    def __createStatusLayout(self):
        self.__currentPatternLabel = QLabel(PATTERN_PREAMBLE + NO_PATTERN_SELECTED)
        font = self.__currentPatternLabel.font()
        font.setPointSize(18)
        self.__currentPatternLabel.setFont(font)
        self.StartButton = QPushButton("Start")
        font = self.StartButton.font()
        font.setPointSize(18)
        self.StartButton.setFont(font)
        self.StartButton.setMinimumSize(STST_BUTTON_WIDTH,STST_BUTTON_HEIGHT)
        startIcon = QIcon("icons/Start.png")
        stopIcon = QIcon("icons/Stop.png")
        self.StartButton.setIcon(startIcon)
        self.StopButton = QPushButton("Stop")
        font = self.StopButton.font()
        font.setPointSize(18)
        self.StopButton.setFont(font)
        self.StopButton.setIcon(stopIcon)
        self.StopButton.setMinimumSize(STST_BUTTON_WIDTH, STST_BUTTON_HEIGHT)
        self.StartButton.clicked.connect(self.__handleStart)
        self.StopButton.clicked.connect(self.__handleStop)
        
        currentSelectionLayout = QVBoxLayout()
        infoLayout = QHBoxLayout()
        infoLayout.addStretch(1)
        infoLayout.addWidget(self.__currentPatternLabel)
        startStopLayout = QHBoxLayout()
        startStopLayout.addStretch(1)
        startStopLayout.addWidget(self.StartButton)
        startStopLayout.addWidget(self.StopButton)

        infoBarLayout = QHBoxLayout()
        logoLayout = QVBoxLayout()
        origMark = QPixmap("icons/USCG.jpg")
        newMark = origMark.scaled(150,150)
        logoLabel = QLabel()
        logoLabel.setPixmap(newMark)
        logoLayout.addWidget(logoLabel)
        
        currentSelectionLayout.addLayout(infoLayout)
        currentSelectionLayout.addLayout(startStopLayout)
        
        infoBarLayout.addLayout(logoLayout)
        infoBarLayout.addLayout(currentSelectionLayout)
        
        return infoBarLayout
        
    def __Log(self,message):
        self.__log.LOG(self.__logTitle,message)
           
    def __createMenu(self):
        menu = self.menuBar()
        
        ## File Menu -----------------------------------------
        fileMenu = menu.addMenu(MainWindow.FILE_MENU)
        
        if ADD_PATTERN_ENABLED:
            newPatternAction = QAction(menu)
            newPatternAction.setText(MainWindow.ADD_MENU)
            newPatternAction.triggered.connect(self.__addPattern)
        
            deletePatternAction = QAction(menu)
            deletePatternAction.setText(MainWindow.DELETE_MENU)
            deletePatternAction.triggered.connect(self.__deletePattern)
            
            fileMenu.addAction(newPatternAction)
            fileMenu.addAction(deletePatternAction)
            
        exitAction = QAction(menu)
        exitAction.setText(MainWindow.EXIT_MENU)
        exitAction.triggered.connect(self.__exit)
        
        fileMenu.addAction(exitAction)
        
        ## About Menu ----------------------------------------
        aboutMenu = menu.addMenu(MainWindow.ABOUT_MENU)
        
        versionAction = QAction(menu)
        versionAction.setText(MainWindow.VERSION_MENU)
        versionAction.triggered.connect(self.__showAbout)
        
        aboutMenu.addAction(versionAction)
        
    def __showAbout(self):
        ret = QMessageBox.information(self,"Version Info", "Release: July 10, 2014")
    
    def __makeDefaultButtons(self):
       for iter in range(0,NUM_DEFAULT_PATTERNS):
           self.__Log("Making preset %d"%iter)
           pattern_params = DEFAULT_PATTERNS[iter]
           name = pattern_params[pIndex.Name]
           des = pattern_params[pIndex.Description] 
           default = pattern_params[pIndex.Default]
           clist = pattern_params[pIndex.ColorList]
           reqColors = pattern_params[pIndex.RequiredColors]
           pwm = pattern_params[pIndex.PWM]
           newPattern = Pattern(name, des, default,clist, reqColors, pwm)
           self.__patterns += [newPattern]
       
       self.__redrawButtons()
    
    def __clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.hide()
                else:
                    self.__clearLayout(item.layout())
            
    def __redrawButtons(self):
        self.__clearLayout(self.__defaultButtonLayout)
        self.__defaultButtonLayout = QVBoxLayout()
        self.__buttons = list()
        
        self.__Log("Redrawing Buttons")
        numOfButtons = len(self.__patterns)
        numOfRows = numOfButtons/BUTTONS_PER_ROW
        if numOfButtons%BUTTONS_PER_ROW != 0:
            numOfRows += 1
        self.__Log("Buttons: %d, Rows: %d"%(numOfButtons, numOfRows))
        for i in range(0,numOfRows):
            self.__Log("Row %d"%i)
            newRow = QHBoxLayout()
            buttonsLeft = numOfButtons - i*BUTTONS_PER_ROW
            buttonsInRow = BUTTONS_PER_ROW
            if buttonsLeft < BUTTONS_PER_ROW:
                buttonsInRow = buttonsLeft
            for j in range(0,buttonsInRow):
                patternId = i*BUTTONS_PER_ROW + j
                #print "Pattern ID %d"%patternId
                pattern = self.__patterns[patternId]
                name = pattern.GetName()
                desc = pattern.GetDescription()
                #print "Name %s"%name
                newLabel = QLabel(desc)
                newButton = MyPushButton(self,name)
                newButton.setMinimumSize(MIN_BUTTON_WIDTH,MIN_BUTTON_HEIGHT)
                font = QFont(newButton.font())
                font.setPointSize(24)
                newButton.setFont(font)
                self.__buttons.append(newButton)
                newButtonLayout = QVBoxLayout()
                newButtonLayout.addWidget(newButton)
                labelLayout = QHBoxLayout()
                labelLayout.addStretch()
                labelLayout.addWidget(newLabel)
                labelLayout.addStretch()
                newButtonLayout.addLayout(labelLayout)
                newRow.addLayout(newButtonLayout)
                
                
            self.__defaultButtonLayout.addLayout(newRow)

        self.__mainLayout.addLayout(self.__defaultButtonLayout)  
            
        
    def __buttonXClicked(self,buttonTag):
        self.__Log("Pattern \'%s\' pressed"%buttonTag)
        self.__selectedPattern = buttonTag
        self.__currentPatternLabel.setText(PATTERN_PREAMBLE+buttonTag)
        
    def __addPattern(self):
        self.__Log("Add Pattern")
        newPattern = Pattern()
        newDescription = "Pattern %d"%(len(self.__patterns))
        self.__Log("New description %s"%newDescription)
        copyPattern = self.__patterns[0]
        newPattern = copyPattern.CopyPattern(newDescription)
        self.__patterns += [newPattern]
        self.__redrawButtons()
        
    def __deletePattern(self):
        self.__Log("Delete Pattern")
        
    def __handleStart(self):
        self.__Log("START")
        
    def __handleStop(self):
        self.__Log("STOP")
        
    def __exit(self):
        self.close()
        