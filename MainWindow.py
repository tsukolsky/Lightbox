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

BUTTONS_PER_ROW = 4
BUTTON_FONT_SIZE = 14
MIN_BUTTON_HEIGHT = 50
MIN_BUTTON_WIDTH = 100
STST_BUTTON_HEIGHT = 50
STST_BUTTON_WIDTH = 80
WATERMARK_DIM = 80
ADD_PATTERN_ENABLED = False
PATTERN_PREAMBLE = "Selected Pattern: "
NO_PATTERN_SELECTED = "None Selected"
PATTERN_EDIT_MODE = "EDIT"
PATTERN_SELECT_MODE = "SELECT"

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
        self.resize(800, 440)       # Screen Size
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
        self.__selectedPatternLayout = QVBoxLayout()
        self.__makeDefaultButtons()
        
        # Connect MyPushButton signals
        self.connect(self, SIGNAL("buttonXClicked(PyQt_PyObject)"), self.__buttonXClicked)

        # Make the window knwo what is the main widget
        self.setCentralWidget(mainWidget)
        
        self.__mode = PATTERN_SELECT_MODE

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
       
       self.__drawPatternButtons()
    
    def __clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.hide()
                else:
                    self.__clearLayout(item.layout())
            
    def __drawPatternButtons(self):
        self.__mode = PATTERN_SELECT_MODE
        self.__clearLayout(self.__selectedPatternLayout)
        self.__clearLayout(self.__defaultButtonLayout)
        self.__defaultButtonLayout = QVBoxLayout()
        self.__selectedPatternLayout = QVBoxLayout()
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
                font.setPointSize(BUTTON_FONT_SIZE)
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
        self.__Log("Button Tag: %s"%buttonTag)
        if self.__mode == PATTERN_SELECT_MODE:
            self.__patternSelected(buttonTag)
        elif self.__mode == PATTERN_EDIT_MODE:
            self.__editPattern(buttonTag)
        else:
            self.__Log("Unknown button tag")
        
    def __editPattern(self,buttonTag):
        print buttonTag.find("Color")
        if buttonTag.find("Color") == 0:
            self.__Log("Color button pressed.")
        elif buttonTag == "Back":
            self.__drawPatternButtons()
        elif buttonTag == "OK":
            self.__handleStart()
            self.__drawPatternButtons()
        else:
            self.__Log("Unknown tag: %s"%buttonTag)
            
    def __patternSelected(self,buttonTag):
        self.__Log("Pattern \'%s\' pressed"%buttonTag)
        self.__selectedPattern = buttonTag
        self.__currentPatternLabel.setText(PATTERN_PREAMBLE+buttonTag)
        
        # Get the actual pattern from the list of patterns
        for it in range(0,len(self.__patterns)):
            tmpPattern = self.__patterns[it]
            if tmpPattern.GetName() == buttonTag:
                self.__Log("FOUND PATTERN")
                self.__drawPatternSettings(tmpPattern)
                return
        
        self.__Log("Didn't find a pattern that matched tag!")
        
    def __addPattern(self):
        self.__Log("Add Pattern")
        newPattern = Pattern()
        newDescription = "Pattern %d"%(len(self.__patterns))
        self.__Log("New description %s"%newDescription)
        copyPattern = self.__patterns[0]
        newPattern = copyPattern.CopyPattern(newDescription)
        self.__patterns += [newPattern]
        self.__drawPatternButtons()
        
    def __deletePattern(self):
        self.__Log("Delete Pattern")
        
    def __drawPatternSettings(self, pattern):
        self.__mode = PATTERN_EDIT_MODE
        self.__Log("Draw pattern settings")
        self.__Log("Pattern \'%s\' pressed"%pattern.GetName())
        self.__Log("Clearing pattern layout.")
        self.__clearLayout(self.__defaultButtonLayout)
        self.__clearLayout(self.__selectedPatternLayout)
        
        # Draw the layout based on the pattern
        self.__defaultButtonLayout = QVBoxLayout()
        self.__selectedPatternLayout = QVBoxLayout()
        
        # Pattern picture 
        patternLayout = QHBoxLayout()
        patLabel = QLabel(pattern.GetName())
        image = QLabel("ICON HERE")
        patternLayout.addStretch(1)
        patternLayout.addWidget(patLabel)
        patternLayout.addStretch(1)
        self.__selectedPatternLayout.addLayout(patternLayout)
        
        # Color choosing buttons
        numOfColors = pattern.GetRequiredColors()
        self.__Log("Number of required colors is %d"%numOfColors)
        colorButtonLayout = QHBoxLayout()
        colorButtonLayout.addStretch(1)
        for x in range(1,numOfColors+1,1):
            newButton = MyPushButton(self,"Color %d..."%x)
            newButton.setMaximumSize(100,100)
            colorButtonLayout.addWidget(newButton)
        colorButtonLayout.addStretch(1)
        self.__selectedPatternLayout.addLayout(colorButtonLayout)
        self.__selectedPatternLayout.addStretch(1)
        
        # Control buttons
        controlButtonLayout = QHBoxLayout()
        controlButtonLayout.addStretch(1)
        backButton = MyPushButton(self,"Back")
        okButton = MyPushButton(self,"OK")
        controlButtonLayout.addWidget(okButton)
        controlButtonLayout.addWidget(backButton)
        self.__selectedPatternLayout.addLayout(controlButtonLayout)
        
        self.__mainLayout.addLayout(self.__selectedPatternLayout)
            
    def __handleStart(self):
        self.__Log("START")
        
    def __handleStop(self):
        self.__Log("STOP")
        
    def __exit(self):
        self.close()
        
