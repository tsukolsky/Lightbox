from PyQt4.QtGui import QMainWindow, QWidget, QHBoxLayout, QPushButton, QTabBar, \
                        QTabWidget, QVBoxLayout, QMenuBar, QAction, QIcon, QLabel, QFont, \
                        QMessageBox, QPixmap
                        
from PyQt4.QtCore import Qt, SIGNAL
import sys, os, time
from PyQt4.QtGui import QApplication
from util.Log import Log
from util.Settings import *
from util.MyPushButton import TagPushButton, IDPushButton
from Pattern import Pattern
from ExecutionThread import ExecutionThread

BUTTONS_PER_ROW = 4
BUTTON_FONT_SIZE = 14
MIN_BUTTON_HEIGHT = 50
MIN_BUTTON_WIDTH = 100
STST_BUTTON_HEIGHT = 50
STST_BUTTON_WIDTH = 80
WATERMARK_DIM = 80
ADD_PATTERN_ENABLED = False
PATTERN_PREAMBLE = "Current Pattern: "
NO_PATTERN_SELECTED = "None"
PATTERN_EDIT_MODE = "EDIT"
PATTERN_SELECT_MODE = "SELECT"

STATUS_PREAMBLE = "Status: "
STOPPED = "Stopped"
RUNNING = "Running"

INTENSITY_PREAMBLE = "Intensity: "

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
      
        # Selected pattern
        self.__selectedPattern = None
        self.__currentIntensity = 4000  
        self.__loadedPattern = None
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
        
        # Connect TagPushButton signals
        self.connect(self, SIGNAL("tagPushButtonClicked(PyQt_PyObject)"), self._tagButtonClicked)
        self.connect(self,SIGNAL("idPushButtonClicked(PyQt_PyObject)"), self._idButtonClicked)
        
        # Make the window knwo what is the main widget
        self.setCentralWidget(mainWidget)
        
        self.__mode = PATTERN_SELECT_MODE

        self.__running = False

    def __createStatusLayout(self):
        ## Make the currently running, start and stop button, running status
        self.__currentPatternLabel = QLabel(PATTERN_PREAMBLE + NO_PATTERN_SELECTED)
        font = self.__currentPatternLabel.font()
        font.setPointSize(18)
        self.__currentPatternLabel.setFont(font)
        self.__currentStatusLabel = QLabel(STATUS_PREAMBLE + STOPPED)
        font = self.__currentStatusLabel.font()
        font.setPointSize(18)
        self.__currentStatusLabel.setFont(font)
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
        
        currentSelectionLayout = QHBoxLayout()
        currentSelectionLayout.addWidget(self.__currentPatternLabel)
        currentSelectionLayout.addStretch(1)
        currentSelectionLayout.addWidget(self.__currentStatusLabel)
        currentSelectionLayout.addStretch(1)
        currentSelectionLayout.addWidget(self.StartButton)
        currentSelectionLayout.addWidget(self.StopButton)
        
        ## Make Intensity Layout
        self.__intensityLabel = QLabel(INTENSITY_PREAMBLE + str(self.__currentIntensity))
        font = self.__intensityLabel.font()
        font.setPointSize(18)
        self.__intensityLabel.setFont(font)
        self.__intensityButton = QPushButton("Set Intensity...")
        font = self.__intensityButton.font()
        font.setPointSize(18)
        self.__intensityButton.setFont(font)
        self.__intensityButton.setMinimumSize(STST_BUTTON_WIDTH*2, STST_BUTTON_HEIGHT)
        self.__intensityButton.clicked.connect(self.__intensityButtonClicked)
        intensityLayout = QHBoxLayout()
        intensityLayout.addWidget(self.__intensityLabel)
        intensityLayout.addStretch(1)
        intensityLayout.addWidget(self.__intensityButton)

        infoBarLayout = QVBoxLayout()
        infoBarLayout.addLayout(currentSelectionLayout)
        infoBarLayout.addLayout(intensityLayout)
        
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
    
    ## Make the Default pattern Buttons ----------------------------------------------
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
    
    ## Clear Layouts ------------------------------------------------------------------
    def __clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.hide()
                else:
                    self.__clearLayout(item.layout())
            
    ## Draw the Premade pattern buttons ------------------------------------------------
    def __drawPatternButtons(self):
        self.__mode = PATTERN_SELECT_MODE
        #if self.__selectedPattern != None:
        #    self.__selectedPattern.ClearColors()
            
        self.__clearLayout(self.__selectedPatternLayout)
        self.__clearLayout(self.__defaultButtonLayout)
        self.__defaultButtonLayout = QVBoxLayout()
        self.__selectedPatternLayout = QVBoxLayout()
        self.__buttons = list()
        
        self.__Log("Redrawing Buttons")
        numOfButtons = len(self.__patterns)
        numOfRows = numOfButtons/BUTTONS_PER_ROW
        lastRowStretch = False
        if numOfButtons%BUTTONS_PER_ROW != 0:
            numOfRows += 1
            lastRowStretch = True
        self.__Log("Buttons: %d, Rows: %d"%(numOfButtons, numOfRows))
        for i in range(0,numOfRows):
            self.__Log("Row %d"%i)
            newRow = QHBoxLayout()
            buttonsLeft = numOfButtons - i*BUTTONS_PER_ROW
            buttonsInRow = BUTTONS_PER_ROW
            if buttonsLeft < BUTTONS_PER_ROW:
                buttonsInRow = buttonsLeft
                newRow.addStretch(1)
            for j in range(0,buttonsInRow):
                patternId = i*BUTTONS_PER_ROW + j
                #print "Pattern ID %d"%patternId
                pattern = self.__patterns[patternId]
                name = pattern.GetName()
                desc = pattern.GetDescription()
                #print "Name %s"%name
                newLabel = QLabel(desc)
                newButton = TagPushButton(self,name)
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
                
            # Iflast row and < full, add stretch to left and right side (left done above)
            if lastRowStretch and i == numOfRows-1:
                newRow.addStretch(1)
            self.__defaultButtonLayout.addLayout(newRow)

        self.__mainLayout.addLayout(self.__defaultButtonLayout)  
            
    ## Color Button has been clicked -------------------------------------------------------
    def _idButtonClicked(self,ID):
        ## Currently only Color buttons are using the ID Button
        self.__Log("ColorID: %d"%ID)
        if self.__mode == PATTERN_EDIT_MODE:
            ## Show color select.
            self.__currentColorSelection = ID - 1
            self.__drawColorButtons()
        else:
            self.__Log("Bad Mode")
    
    def __drawColorButtons(self):
        self.__colorButtonChooserLayout = QHBoxLayout()
        numOfColors = len(Colors)
        
        for i in range(0,numOfColors-1):        ## -1 excludes the Empty
            button = TagPushButton(self,Colors[i])
            font = button.font()
            font.setPointSize(14)
            button.setFont(font)
            self.__colorButtonChooserLayout.addWidget(button)
        
        self.__drawPatternSettings(self.__selectedPattern, True)
        
    def __colorSelected(self, colorTag):
        self.__Log("Got Color Selected: %s, setting index %d"%(colorTag,self.__currentColorSelection))
        self.__selectedPattern.SetColor(self.__currentColorSelection,colorTag)
        self.__drawPatternSettings(self.__selectedPattern) 
    
    def __intensityButtonClicked(self):
        self.__Log("Intensity Button Clicked")
    
    def _tagButtonClicked(self,buttonTag):
        self.__Log("Button Tag: %s"%buttonTag)
        if self.__mode == PATTERN_SELECT_MODE:
            self.__patternSelected(buttonTag)
        elif self.__mode == PATTERN_EDIT_MODE:
            # Must be the back or OK buttons
            if buttonTag == "Back":
                self.__patternEditControlPressed(buttonTag)
            else:
                self.__colorSelected(buttonTag)
        else:
            self.__Log("Bad Mode")
        
    def __patternEditControlPressed(self,buttonTag):
        if buttonTag == "Back":
            self.__drawPatternButtons()
        else:
            self.__Log("Unknown tag: %s"%buttonTag)
            
    def __patternSelected(self,buttonTag):
        self.__Log("Pattern \'%s\' pressed"%buttonTag)
        #self.__currentPatternLabel.setText(PATTERN_PREAMBLE+buttonTag)
        
        # Get the actual pattern from the list of patterns
        for it in range(0,len(self.__patterns)):
            self.__selectedPattern = self.__patterns[it]
            if self.__selectedPattern.GetName() == buttonTag:
                self.__Log("FOUND PATTERN")
                self.__selectedPattern.ClearColors()
                self.__drawPatternSettings(self.__selectedPattern)
                return
        
        self.__Log("Didn't find a pattern that matched tag!")
        
   
    ## Draw Settings Window -------------------------------------------------------  
    def __drawPatternSettings(self, pattern, withColors=False):
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
        font = patLabel.font()
        font.setPointSize(20)
        patLabel.setFont(font)
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
            buttonLayout = QVBoxLayout()
            
            # Make Button
            newButton = IDPushButton(self,"Color %d..."%x, x)
            font = newButton.font()
            font.setPointSize(14)
            newButton.setFont(font)
            newButton.setMaximumSize(100,100)
            
            # Make Label
            newLabel = QLabel(self.__selectedPattern.GetColorByIndex(x-1))
            font = newLabel.font()
            font.setPointSize(14)
            newLabel.setFont(font)
            buttonLayout.addWidget(newButton)
            labelLayout = QHBoxLayout()
            labelLayout.addStretch(1)
            labelLayout.addWidget(newLabel)
            labelLayout.addStretch(1)
            
            # Add label to button layout, button layout to color button layout
            buttonLayout.addLayout(labelLayout)
            colorButtonLayout.addLayout(buttonLayout)
            
        colorButtonLayout.addStretch(1)
        self.__selectedPatternLayout.addLayout(colorButtonLayout)
        if withColors:
            self.__selectedPatternLayout.addLayout(self.__colorButtonChooserLayout)
        self.__selectedPatternLayout.addStretch(1)
        
        # Control buttons
        controlButtonLayout = QHBoxLayout()
        controlButtonLayout.addStretch(1)
        backButton = TagPushButton(self,"Back")
        controlButtonLayout.addWidget(backButton)
        self.__selectedPatternLayout.addLayout(controlButtonLayout)
        
        self.__mainLayout.addLayout(self.__selectedPatternLayout)
            
    def __handleStart(self):
        self.__Log("START")
        if (self.__selectedPattern != None):
            if self.__running:
                if (self.EXECUTION_THREAD != None):
                    self.EXECUTION_THREAD.join()
                    time.sleep(.5)
                    
            if self.__selectedPattern.CanStart():
                self.__Log("STARTING STARTING STARTING")
                self.__running = True
                self.__loadedPattern = self.__selectedPattern
                self.__currentPatternLabel.setText(PATTERN_PREAMBLE + self.__loadedPattern.GetName())
                self.__currentStatusLabel.setText(STATUS_PREAMBLE + RUNNING)
                # Start Threading
                self.EXECUTION_THREAD = ExecutionThread(self.__loadedPattern,4000)
                self.EXECUTION_THREAD.start()
                time.sleep(.5)   # Sleep to make sure that the other thread gets what it needs
                self.__drawPatternButtons()
            elif self.__loadedPattern != None and self.__mode == PATTERN_SELECT_MODE and self.EXECUTION_THREAD != None:
                self.__currentPatternLabel.setText(PATTERN_PREAMBLE + self.__loadedPattern.GetName())
                self.__currentStatusLabel.setText(STATUS_PREAMBLE + RUNNING)
                self.EXECUTION_THREAD = ExecutionThread(self.__loadedPattern,4000)
                self.EXECUTION_THREAD.start()
            
    def __handleStop(self):
        self.__Log("STOP")
        if self.__running:
            self.__running = False
            #self.__selectedPattern.ClearColors()
            #self.__currentPatternLabel.setText(PATTERN_PREAMBLE + NO_PATTERN_SELECTED)
            self.__currentStatusLabel.setText(STATUS_PREAMBLE + STOPPED)
            
            # Stop Threading
            if (self.EXECUTION_THREAD != None):
                self.EXECUTION_THREAD.join()
                
            self.__redrawMode()
            
    def __redrawMode(self):
        if self.__mode == PATTERN_EDIT_MODE:
            self.__drawPatternSettings(self.__selectedPattern)
        elif self.__mode == PATTERN_SELECT_MODE:
            self.__drawPatternButtons()
        else:
            self.__Log("No mode to redraw")
            
    def __exit(self):
        self.close()
        
    ### DISABLED-----------------------------------------------------
    def __addPattern(self):
        self.__Log("Add Pattern")
        newPattern = Pattern()
        newDescription = "Pattern %d"%(len(self.__patterns))
        self.__Log("New description %s"%newDescription)
        copyPattern = self.__patterns[0]
        newPattern = copyPattern.CopyPattern(newDescription)
        self.__patterns += [newPattern]
        self.__drawPatternButtons()
        
    ## Disabled-------------------------------------------------------- 
    def __deletePattern(self):
        self.__Log("Delete Pattern")
        
