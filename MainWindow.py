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
from PresetManager import PresetManager

BUTTONS_PER_ROW             = 4
PATTERN_BUTTON_FONT_SIZE    = 12
PATTERN_LABEL_FONT_SIZE     = 8
PAGE_INFO_LABEL_SIZE     = 24
CONTROL_LABEL_FONT_SIZE     = 12
CONTROL_BUTTON_FONT_SIZE    = 12
INTENSITY_BUTTON_FONT_SIZE  = 20
MIN_BUTTON_HEIGHT           = 40
MIN_BUTTON_WIDTH            = 150
CONTROL_BUTTON_HEIGHT       = 30
CONTROL_BUTTON_WIDTH           = 70
INTENSITY_BUTTON_MIN_HEIGHT = 50
INTENSITY_BUTTON_MIN_WIDTH  = 100
ADD_PATTERN_ENABLED         = False
PATTERN_PREAMBLE            = "Current Pattern: "
NO_PATTERN_SELECTED         = "None"
EMPTY_PATTERN_SELECTED      = "Empty"
PATTERN_EDIT_MODE           = "EDIT"
PATTERN_SELECT_MODE         = "SELECT"
PATTERN_PRESET_SELECT_MODE  = "PRESET_SELECT"
PATTERN_PRESET_DELETE_MODE  = "PRESET_DELETE"
INTENSITY_SELECT_MODE       = "INTENSITY"
INTENSITY_PREAMBLE          = "Intensity: "
STATUS_PREAMBLE             = "Status: "
STOPPED                     = "Stopped"
RUNNING                     = "Running"
PRESET_TAG                  = "Preset Patterns"

class MainWindow(QMainWindow):
    SHUTDOWN_MENU = "&Shutdown"
    HELP_MENU = "&Help"
    SOFT_EXIT = "&Soft Exit"
    PHONE_HOME = "Pho&ne Home"
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
        self.CALLING_CLASS = "MainWindow"
        if self.__log == None:
            print "No Log File"
            self.close()
            
        # Create main layout for window
        mainWidget = QWidget(self)
        self.__mainLayout = QVBoxLayout(mainWidget)
        mainWidget.setLayout(self.__mainLayout)
      
        # Selected pattern
        self.__selectedPattern = None
        self.__presetPatternForDeleting = None
        self.__currentIntensity = 4000  
        self.__loadedPattern = None                 ## Loaded (Running Pattern)
        self.__loadedPatternBeforePreset = None
        self.__CACHED_PRESET = None
        self.EXECUTION_THREAD = None
        
        # Add Menu Bard
        self.__menu = self.__createMenu()

        ## Toolbar that is always there->Selected Pattern, Start, Stop, Current State Label
        self.__statusLayout = self.__createStatusLayout()
        self.__mainLayout.addLayout(self.__statusLayout)
        
        self.__patterns = list()
        self.__buttons = list()
        self.__savedPresets = list()
        
        self.__presetManager = PresetManager(self.__log)
        
        self.__defaultButtonLayout = QVBoxLayout()
        self.__selectedPatternLayout = QVBoxLayout()
        self.__intensitySelectLayout = QVBoxLayout()
        self.__presetButtonLayout = QVBoxLayout()
        self.__makeDefaultButtons()
        
        self.__importPresetsFromFile()
        
        # Connect TagPushButton signals
        self.connect(self, SIGNAL("tagPushButtonClicked(PyQt_PyObject)"), self._tagButtonClicked)
        self.connect(self,SIGNAL("idPushButtonClicked(PyQt_PyObject)"), self._idButtonClicked)
        
        # Make the window knwo what is the main widget
        self.setCentralWidget(mainWidget)
        
        self.__mode = PATTERN_SELECT_MODE
        self.__lastMode = self.__mode

        self.__running = False

    def __createStatusLayout(self):
        ## Make the currently running, start and stop button, running status
        self.__currentPatternLabel = QLabel(PATTERN_PREAMBLE + EMPTY_PATTERN_SELECTED)
        font = self.__currentPatternLabel.font()
        self.__setFont(self.__currentPatternLabel,CONTROL_LABEL_FONT_SIZE)
        self.__currentStatusLabel = QLabel(STATUS_PREAMBLE + STOPPED)
        self.__setFont(self.__currentStatusLabel,CONTROL_LABEL_FONT_SIZE)
        self.StartButton = QPushButton("Start")
        self.__setFont(self.StartButton, CONTROL_BUTTON_FONT_SIZE)
        self.StartButton.setMinimumSize(CONTROL_BUTTON_WIDTH,CONTROL_BUTTON_HEIGHT)
        startIcon = QIcon("/home/pi/Desktop/Lightbox/icons/Start.png")
        stopIcon = QIcon("/home/pi/Desktop/Lightbox/icons/Stop.png")
        self.StartButton.setIcon(startIcon)
        self.StopButton = QPushButton("Stop")
        self.__setFont(self.StopButton, CONTROL_BUTTON_FONT_SIZE)
        self.StopButton.setIcon(stopIcon)
        self.StopButton.setMinimumSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT)
        self.StartButton.clicked.connect(self.__handleStart)
        self.StopButton.clicked.connect(self.__handleStop)
        
        currentSelectionLayout = QHBoxLayout()
        currentSelectionLayout.addWidget(self.__currentPatternLabel)
        currentSelectionLayout.addStretch(1)
        currentSelectionLayout.addWidget(self.__currentStatusLabel)
        currentSelectionLayout.addWidget(self.StartButton)
        currentSelectionLayout.addWidget(self.StopButton)
        
        ## Make Intensity Layout
        self.__intensityLabel = QLabel(INTENSITY_PREAMBLE + str(self.__currentIntensity))
        self.__setFont(self.__intensityLabel,CONTROL_LABEL_FONT_SIZE)
        self.__intensityButton = QPushButton("Set Intensity...")
        self.__setFont(self.__intensityButton, CONTROL_BUTTON_FONT_SIZE)
        self.__intensityButton.setMinimumSize(CONTROL_BUTTON_WIDTH*2, CONTROL_BUTTON_HEIGHT)
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
        self.__log.LOG(self.CALLING_CLASS,message)
           
    def __createMenu(self):
        menu = self.menuBar()
        
        ## About Menu ----------------------------------------
        aboutMenu = menu.addMenu(MainWindow.ABOUT_MENU)
        
        versionAction = QAction(menu)
        versionAction.setText(MainWindow.VERSION_MENU)
        versionAction.triggered.connect(self.__showAbout)
        
        aboutMenu.addAction(versionAction)
        
        ## Shutdown Menu -----------------------------------------
        shutdownMenu = menu.addMenu(MainWindow.SHUTDOWN_MENU)
        
        if ADD_PATTERN_ENABLED:
            newPatternAction = QAction(menu)
            newPatternAction.setText(MainWindow.ADD_MENU)
            newPatternAction.triggered.connect(self.__addPattern)
        
            deletePatternAction = QAction(menu)
            deletePatternAction.setText(MainWindow.DELETE_MENU)
            deletePatternAction.triggered.connect(self.__deletePattern)
            
            shutdownMenu.addAction(newPatternAction)
            shutdownMenu.addAction(deletePatternAction)
            
        shutdownAction = QAction(menu)
        shutdownAction.setText(MainWindow.SHUTDOWN_MENU)
        shutdownAction.triggered.connect(self.__shutdown)
        
        shutdownMenu.addAction(shutdownAction)
        
        ## Soft Exit Menu ------------------------------------
        helpMenu = menu.addMenu(MainWindow.HELP_MENU)
        
        softExitAction = QAction(menu)
        softExitAction.setText(MainWindow.SOFT_EXIT)
        softExitAction.triggered.connect(self.__exit)
        
        helpMenu.addAction(softExitAction)
        
        if PHONE_HOME_ENABLED:
            phoneHomeAction = QAction(menu)
            phoneHomeAction.setText(MainWindow.PHONE_HOME)
            softExitAction.triggered.connect(self.__phoneHome)
            helpMenu.addAction(phoneHomeAction)
        
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
           newPattern = Pattern(name, des, default,clist, reqColors, pwm, self.__log)
           self.__patterns += [newPattern]
       
       self.__drawPatternButtons()
    
    def __importPresetsFromFile(self):
        self.__savedPresets = self.__presetManager.GetPresetPatterns()
    
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
    
    def __intensityButtonClicked(self):
        self.__Log("Intensity Button Clicked")
        self.__lastMode = self.__mode
        self.__drawIntensityButtons()     

    ## Color Button has been clicked -------------------------------------------------------
    def _idButtonClicked(self,ID):
        ## Currently only Color buttons are using the ID Button
        self.__Log("ColorID: %d"%ID)
        if self.__mode == PATTERN_EDIT_MODE:
            ## Show color select.
            self.__currentColorSelection = ID - 1
            self.__drawColorButtons()
        elif self.__mode == INTENSITY_SELECT_MODE:
            # Get the intensity selected
            self.__intensitySelected(ID)
        elif self.__mode == PATTERN_PRESET_SELECT_MODE:
            self.__presetPatternSelectedForStart(ID)
            #self.__drawPatternButtons()
        else:
            self.__Log("Bad Mode")
              
    def _tagButtonClicked(self,buttonTag):
        self.__Log("Button Tag: %s, mode: %s"%(buttonTag, self.__mode))
        if self.__mode == PATTERN_SELECT_MODE:
            self.__patternSelected(buttonTag)
        elif self.__mode == PATTERN_EDIT_MODE:
            # Must be the back or OK buttons
            if buttonTag == "Back":
                self.__patternEditControlPressed(buttonTag)
            elif buttonTag == "Save as Preset":
                self.__savePatternAsPreset()
            else:
                self.__colorSelected(buttonTag)
        elif self.__mode == PATTERN_PRESET_SELECT_MODE:
            if buttonTag == "Back":
                if self.__loadedPatternBeforePreset != None and self.__presetPatternForDeleting != None:
                    self.__Log("Both are not none")
                    if self.__loadedPatternBeforePreset.GetName() != self.__presetPatternForDeleting.GetName() and self.__loadedPatternBeforePreset.GetColorString() != self.__presetPatternForDeleting.GetColorString():
                        self.__Log("Setting preset back to the one it was before")
                        self.__loadedPattern = self.__loadedPatternBeforePreset
                        self.__loadedPatternBeforePreset = None
                self.__presetPatternForDeleting = None
                self.__loadedPatternBeforePreset = None
                self.__drawPatternButtons()
                if self.__loadedPattern != None:
                    self.__currentPatternLabel.setText(PATTERN_PREAMBLE + self.__loadedPattern.GetName() + ' ' + self.__loadedPattern.GetColorString())
            elif buttonTag == "Delete":
                self.__presetPatternForDeleting = self.__loadedPattern
                if self.__loadedPatternBeforePreset != None and self.__presetPatternForDeleting != None:
                    self.__Log("Both are not none")
                    if self.__loadedPatternBeforePreset.GetName() == self.__presetPatternForDeleting.GetName() and self.__loadedPatternBeforePreset.GetColorString() == self.__presetPatternForDeleting.GetColorString():
                        self.__Log("Deleting the currently loaded pattern")
                        self.__loadedPatternBeforePreset = None
                        self.__loadedPattern = None
                        self.__currentPatternLabel.setText(PATTERN_PREAMBLE + EMPTY_PATTERN_SELECTED)
                    else:
                        self.__Log("Setting the loaded pattern back to what it should be before delete occured")
                        self.__loadedPattern = self.__loadedPatternBeforePreset
                        self.__currentPatternLabel.setText(PATTERN_PREAMBLE + self.__loadedPattern.GetName()+ ' ' + self.__loadedPattern.GetColorString())
                elif self.__loadedPatternBeforePreset == None:
                    self.__currentPatternLabel.setText(PATTERN_PREAMBLE + EMPTY_PATTERN_SELECTED)
                    self.__loadedPattern = None
                else:
                    self.__loadedPattern = self.__loadedPatternBeforePreset
                    self.__currentPatternLabel.setText(PATTERN_PREAMBLE + self.__loadedPattern.GetName()+ ' ' + self.__loadedPattern.GetColorString())
                    
                self.__deletePresetPattern()
                if len(self.__savedPresets) > 0:
                    self.__drawPresetPatternsForSelection()
                else:
                    self.__drawPatternButtons()
            else:
                self.__Log("Unknown button")
        else:
            self.__Log("Bad Mode")
        
    def __presetPatternSelectedForStart(self,ID):
        self.__Log("Preset pattern selected with ID %d"%ID)
        if ID >= 0 and ID < len(self.__savedPresets):
            self.__selectedPattern = self.__savedPresets[ID]
            self.__currentPatternLabel.setText(PATTERN_PREAMBLE + self.__selectedPattern.GetName()  + ' ' + self.__selectedPattern.GetColorString())
            self.__loadedPattern = self.__selectedPattern
            self.__presetDeleteButton.setEnabled(True)
            self.StartButton.setEnabled(True)
            return      
        
    def __intensitySelected(self, ID):
        ## NOTE: INtensity does not change until the STOP->START  is pressed.
        self.__Log("Got Intensity: %d"%ID)
        self.__currentIntensity = ID
        self.__intensityLabel.setText(INTENSITY_PREAMBLE + str(ID))
        self.__mode = self.__lastMode
        self.__redrawMode()
        
    def __colorSelected(self, colorTag):
        self.__Log("Got Color Selected: %s, setting index %d"%(colorTag,self.__currentColorSelection))
        presetColorList = list()
        if (self.__savedPresets != None):
            for aPreset in self.__savedPresets:
                self.__Log("Preset Colors:%s"%(",".join(aPreset.GetColorList())))
                newList = list()
                for color in aPreset.GetColorList():
                    for presetColor in ColorsByIndex:
                        if presetColor == color:
                            newList += [presetColor]
                            break
                presetColorList += [newList]
                self.__Log("Preset Colors:%s"%(",".join(newList)))                    
                
                #presetColorList += [aPreset.GetColorList()]    
        self.__selectedPattern.SetColor(self.__currentColorSelection,colorTag)
        if self.__savedPresets != None:
            for ind,aPreset in enumerate(self.__savedPresets):
                self.__Log("Colors:  %s"%(",".join(presetColorList[ind])))
                aPreset.SetColorList(presetColorList[ind])
                self.__Log("Preset Colors:%s"%(",".join(aPreset.GetColorList())))
        
        ## Check to see if this is now valid
        if self.__selectedPattern.CanStart():
            self.__loadedPattern = self.__selectedPattern
            self.StartButton.setEnabled(True)
                    
        self.__drawPatternSettings(self.__selectedPattern) 
        
    def __savePatternAsPreset(self):
        self.__Log("Save Pattern As Preset")
        if self.__selectedPattern.CanStart():
            self.__Log("%d Presets already made"%len(self.__savedPresets))
            for aPreset in self.__savedPresets:
                self.__Log("Preset Colors:%s"%(",".join(aPreset.GetColorList())))
                
            if len(self.__savedPresets) < MAX_NUM_PRESETS:
                # Check to see if there is a duplicate of this already
                newPattern = Pattern()
                newPattern.SetName(self.__selectedPattern.GetName())
                newPattern.SetDescription(self.__selectedPattern.GetDescription())
                newPattern.SetLog(self.__log)
                newPattern.SetPwmSequenceDict(self.__selectedPattern.GetPwmSequenceDict())
                newPattern.SetColorList(self.__selectedPattern.GetColorList())
                newPattern.SetRequiredColors(self.__selectedPattern.GetRequiredColors())
                self.__Log("Colors %s"%(",".join(newPattern.GetColorList())))
                for pattern in self.__savedPresets:
                    if pattern.GetName() == newPattern.GetName():
                        if pattern.GetColorList() == newPattern.GetColorList():
                            return
                
                self.__savedPresets += [newPattern]
                self.__CACHED_PRESET = None
                self.__Log("Saved  Pattern.")
                self.__presetManager.SavePresetPattern(newPattern)
                self.__drawPatternSettings(self.__selectedPattern, False, True)  
        
    def __patternEditControlPressed(self,buttonTag):
        if buttonTag == "Back":
            self.__drawPatternButtons()
            if self.__loadedPattern != None:
                self.__currentPatternLabel.setText(PATTERN_PREAMBLE + self.__loadedPattern.GetName()  + ' ' + self.__loadedPattern.GetColorString())
        else:
            self.__Log("Unknown tag: %s"%buttonTag)
            
    def __patternSelected(self,buttonTag):
        self.__Log("Pattern \'%s\' pressed"%buttonTag)
        
        if buttonTag == PRESET_TAG:
            self.__Log("Preset Button Pressed.")
            self.__loadedPatternBeforePreset = self.__loadedPattern
            self.__drawPresetPatternsForSelection()
            return
        
        # Get the actual pattern from the list of patterns
        for it in range(0,len(self.__patterns)):
            self.__selectedPattern = self.__patterns[it]
            if self.__selectedPattern.GetName() == buttonTag:
                self.__Log("FOUND PATTERN")
                self.__selectedPattern.ClearColors()
                self.__drawPatternSettings(self.__selectedPattern)
                return
        
        self.__Log("Didn't find a pattern that matched tag!")
        
    
    def __handleStart(self):
        self.__Log("START")
        if self.__loadedPattern != None:
            if self.__running:
                if (self.EXECUTION_THREAD != None):
                    self.EXECUTION_THREAD.join()
                    time.sleep(.5)
            
            self.__running = True
            self.__currentStatusLabel.setText(STATUS_PREAMBLE + RUNNING)
            self.EXECUTION_THREAD = ExecutionThread(self.__loadedPattern,self.__currentIntensity, self.__log)
            self.EXECUTION_THREAD.start()
            time.sleep(.5)            
            
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
                time.sleep(.5)
                
            self.__redrawMode()
            
    def __exit(self):
        self.__handleStop()
        self.close()
        
    def __shutdown(self):
        self.__handleStop()
        if RASPI:
            os.system("sudo shutdown -h 0")
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
        
    ## Delete a preset pattern --------------------------------------
    def __deletePresetPattern(self):
        self.__Log("Delete Preset Pattern")
        self.__savedPresets.remove(self.__presetPatternForDeleting)
        self.__presetManager.DeletePresetPattern(self.__presetPatternForDeleting)
        
    def __setFont(self, object, size):
        font = QFont(object.font())
        font.setPointSize(size)
        object.setFont(font)  
        
    def __startValid(self):
        self.__Log("In start Valid")
        if self.__mode == PATTERN_EDIT_MODE or self.__mode == PATTERN_PRESET_SELECT_MODE:
            if self.__selectedPattern != None:
                self.StartButton.setEnabled(self.__selectedPattern.CanStart())
            else:
                self.StartButton.setEnabled(False)
            self.__Log("In edit mode/preset selection (same state as edit, selectedPattern has to be valid.")
        elif self.__loadedPattern != None:
            self.__Log("Looking at loaded pattern")
            if self.__loadedPattern.CanStart():
                self.StartButton.setEnabled(self.__loadedPattern.CanStart())
        else:
            self.StartButton.setEnabled(False)
            
    def __redrawMode(self):
        if self.__mode == PATTERN_EDIT_MODE:
            self.__drawPatternSettings(self.__selectedPattern)
        elif self.__mode == PATTERN_SELECT_MODE:
            self.__drawPatternButtons()
        elif self.__mode == INTENSITY_SELECT_MODE:
            self.__drawIntensityButtons()
        else:
            self.__Log("No mode to redraw")
                    
    ## Draw the Premade pattern buttons ------------------------------------------------
    def __drawPatternButtons(self):
        self.__mode = PATTERN_SELECT_MODE
        self.__startValid() 
        
        self.__clearLayout(self.__selectedPatternLayout)
        self.__clearLayout(self.__defaultButtonLayout)
        self.__clearLayout(self.__intensitySelectLayout)
        self.__clearLayout(self.__presetButtonLayout)
        
        self.__defaultButtonLayout = QVBoxLayout()
        self.__selectedPatternLayout = QVBoxLayout()
        self.__intensityLayout = QVBoxLayout()
        self.__presetButtonLayout = QVBoxLayout()
        self.__buttons = list()
        
        # add label for this screen
        patternLabelLayout = QHBoxLayout()
        patternLabelLayout.addStretch(1)
        patternLabel = QLabel("Temporal Patterns")
        self.__setFont(patternLabel,PAGE_INFO_LABEL_SIZE)
        patternLabelLayout.addWidget(patternLabel)
        patternLabelLayout.addStretch(1)
        self.__defaultButtonLayout.addLayout(patternLabelLayout)
        
        self.__Log("Redrawing Buttons")
        numOfButtons = len(self.__patterns)# + 1         # One for preset
        numOfRows = numOfButtons/BUTTONS_PER_ROW
        lastRowStretch = False
        if numOfButtons%BUTTONS_PER_ROW != 0:
            numOfRows += 1
            lastRowStretch = True
        self.__Log("Buttons: %d, Rows: %d"%(numOfButtons, numOfRows))
        for i in range(0,numOfRows):
            #self.__Log("Row %d"%i)
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
                self.__setFont(newLabel,PATTERN_LABEL_FONT_SIZE)
                newButton = TagPushButton(self,name)
                newButton.setMinimumSize(MIN_BUTTON_WIDTH,MIN_BUTTON_HEIGHT)
                self.__setFont(newButton, PATTERN_BUTTON_FONT_SIZE)
                self.__buttons.append(newButton)
                newButtonLayout = QVBoxLayout()
                newButtonLayout.addWidget(newButton)
                labelLayout = QHBoxLayout()
                labelLayout.addStretch()
                labelLayout.addWidget(newLabel)
                labelLayout.addStretch()
                newButtonLayout.addLayout(labelLayout)
                newButtonLayout.addStretch(1)
                newRow.addLayout(newButtonLayout)
                
            # Iflast row and < full, add stretch to left and right side (left done above)
            if lastRowStretch and i == numOfRows-1:
                ## Add the preset button here, we know it's there
                button = TagPushButton(self,PRESET_TAG)
                self.__setFont(button, PATTERN_BUTTON_FONT_SIZE)
                button.setMinimumSize(MIN_BUTTON_WIDTH,MIN_BUTTON_HEIGHT)
                presetLayout = QVBoxLayout()
                presetLayout.addWidget(button)
                presetLayout.addStretch(1)
                newRow.addLayout(presetLayout)
                newRow.addStretch(1)
            self.__defaultButtonLayout.addLayout(newRow)

        self.__mainLayout.addLayout(self.__defaultButtonLayout)  
   

    ## Draw Settings Window -------------------------------------------------------  
    def __drawPatternSettings(self, pattern, withColors=False, withSavedPresetTag=False):
        self.__mode = PATTERN_EDIT_MODE
        if pattern.CanStart():
            self.__currentPatternLabel.setText(PATTERN_PREAMBLE + pattern.GetName()  + ' ' + pattern.GetColorString())
        else:
            self.__currentPatternLabel.setText(PATTERN_PREAMBLE + EMPTY_PATTERN_SELECTED)
        
        self.__startValid() 
        self.__Log("Draw pattern settings")
        self.__Log("Pattern \'%s\' pressed"%pattern.GetName())
        self.__Log("Clearing pattern layout.")
        self.__clearLayout(self.__selectedPatternLayout)
        self.__clearLayout(self.__defaultButtonLayout)
        self.__clearLayout(self.__intensitySelectLayout)
        self.__clearLayout(self.__presetButtonLayout)
        
        self.__defaultButtonLayout = QVBoxLayout()
        self.__selectedPatternLayout = QVBoxLayout()
        self.__intensityLayout = QVBoxLayout()
        self.__presetButtonLayout = QVBoxLayout()
        
        # Pattern picture 
        patternLayout = QHBoxLayout()
        patLabel = QLabel(pattern.GetName())
        self.__setFont(patLabel,PAGE_INFO_LABEL_SIZE)
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
            self.__setFont(newButton,PATTERN_BUTTON_FONT_SIZE)
            newButton.setMaximumSize(100,100)
            
            # Make Label
            newLabel = QLabel(self.__selectedPattern.GetColorByIndex(x-1))
            self.__setFont(newLabel,PATTERN_LABEL_FONT_SIZE)
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
        saveButton = TagPushButton(self,"Save as Preset")
        backButton = TagPushButton(self,"Back")
        saveButton.setMinimumSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT)
        backButton.setMinimumSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT)
        self.__setFont(saveButton,CONTROL_BUTTON_FONT_SIZE)
        self.__setFont(backButton,CONTROL_BUTTON_FONT_SIZE)
        
	## If we just saved a preset, show the QLabel that we did.
        if (withSavedPresetTag):
            presetSavedLabel = QLabel("Successfully saved as Preset!")
            self.__setFont(presetSavedLabel, CONTROL_LABEL_FONT_SIZE)        
            controlButtonLayout.addWidget(presetSavedLabel)

        ## Check to see if adding a preset is okay?
        if len(self.__savedPresets) >= MAX_NUM_PRESETS:
            saveButton.setEnabled(False)
            presetsFullLabel = QLabel("Presets Full!")
            self.__setFont(presetsFullLabel,CONTROL_LABEL_FONT_SIZE)
            controlButtonLayout.addWidget(presetsFullLabel)
        else:
            saveButton.setEnabled(self.__selectedPattern.CanStart())
            
        controlButtonLayout.addWidget(saveButton)
        controlButtonLayout.addWidget(backButton)
        self.__selectedPatternLayout.addLayout(controlButtonLayout)
        
        self.__mainLayout.addLayout(self.__selectedPatternLayout)
    
    def __drawColorButtons(self):
        self.__colorButtonChooserLayout = QHBoxLayout()
        numOfColors = len(Colors)
        
        for i in range(0,numOfColors-1):        ## -1 excludes the Empty
            button = TagPushButton(self,Colors[i])
            self.__setFont(button, PATTERN_BUTTON_FONT_SIZE)
            self.__colorButtonChooserLayout.addWidget(button)
        
        self.__drawPatternSettings(self.__selectedPattern, True)            
            
    def __drawIntensityButtons(self):
        self.__mode = INTENSITY_SELECT_MODE
        self.__Log("Draw intensity buttons")
        self.__clearLayout(self.__selectedPatternLayout)
        self.__clearLayout(self.__defaultButtonLayout)
        self.__clearLayout(self.__intensitySelectLayout)
        self.__clearLayout(self.__presetButtonLayout)
        
        self.__defaultButtonLayout = QVBoxLayout()
        self.__selectedPatternLayout = QVBoxLayout()
        self.__intensitySelectLayout = QVBoxLayout()
        self.__presetButtonLayout = QVBoxLayout()
        
        self.__intensitySelectLayout.addStretch(1)
        
        labelLayout = QHBoxLayout()
        labelLayout.addStretch(1)
        intensityLabel = QLabel("Intensity Select (candela)")
        self.__setFont(intensityLabel,PAGE_INFO_LABEL_SIZE)
        labelLayout.addWidget(intensityLabel)
        labelLayout.addStretch(1)
        self.__intensitySelectLayout.addLayout(labelLayout)
        
        numOfButtons = len(Intensities)
        maxButtonsPerRow = 3
        numOfRows = numOfButtons/maxButtonsPerRow
        if numOfButtons%maxButtonsPerRow != 0:
            numOfRows += 1
            
        for i in range(0, numOfRows):
            rowLayout = QHBoxLayout()
            rowLayout.addStretch(1)
            buttonsLeft = numOfButtons - i*maxButtonsPerRow
            buttonsInRow = maxButtonsPerRow
            if buttonsLeft < maxButtonsPerRow:
                buttonsInRow = buttonsLeft
            for j in range(0,buttonsInRow):
                button = IDPushButton(self, str(Intensities[j+(i*maxButtonsPerRow)]), Intensities[j+(i*maxButtonsPerRow)])
                self.__setFont(button, INTENSITY_BUTTON_FONT_SIZE)
                button.setMinimumSize(INTENSITY_BUTTON_MIN_WIDTH, INTENSITY_BUTTON_MIN_HEIGHT)
                rowLayout.addWidget(button)
                
            rowLayout.addStretch(1)
            self.__intensitySelectLayout.addLayout(rowLayout)
            
        self.__mainLayout.addLayout(self.__intensitySelectLayout)
                
    def __drawPresetPatternsForSelection(self):
        if len(self.__savedPresets) > 0:
            self.__mode = PATTERN_PRESET_SELECT_MODE
            self.__createPresetPatternLayout()
            controlLayout = QHBoxLayout()
            controlLayout.addStretch(1)
            self.__presetDeleteButton = TagPushButton(self,"Delete")
            self.__setFont(self.__presetDeleteButton, CONTROL_BUTTON_FONT_SIZE)
            self.__presetDeleteButton.setMinimumSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT)
            self.__presetDeleteButton.setEnabled(False)
            backButton = TagPushButton(self,"Back")
            self.__setFont(backButton,CONTROL_BUTTON_FONT_SIZE)
            backButton.setMinimumSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT)
            controlLayout.addWidget(self.__presetDeleteButton)
            controlLayout.addWidget(backButton)
            self.__presetButtonLayout.addStretch(1)
            self.__presetButtonLayout.addLayout(controlLayout)
            self.__mainLayout.addLayout(self.__presetButtonLayout)

        self.__selectedPattern = None
        self.__startValid()
         
    def __createPresetPatternLayout(self):
        self.__clearLayout(self.__selectedPatternLayout)
        self.__clearLayout(self.__defaultButtonLayout)
        self.__clearLayout(self.__intensitySelectLayout)
        self.__clearLayout(self.__presetButtonLayout)
        
        self.__currentPatternLabel.setText(PATTERN_PREAMBLE + EMPTY_PATTERN_SELECTED)
        
        self.__defaultButtonLayout = QVBoxLayout()
        self.__selectedPatternLayout = QVBoxLayout()
        self.__intensityLayout = QVBoxLayout()
        self.__presetButtonLayout = QVBoxLayout()
        
        presetLabelLayout = QHBoxLayout()
        presetLabelLayout.addStretch(1)
        presetPatternLabel = QLabel("Preset Patterns")
        self.__setFont(presetPatternLabel,PAGE_INFO_LABEL_SIZE)
        presetLabelLayout.addWidget(presetPatternLabel)
        presetLabelLayout.addStretch(1)
        self.__presetButtonLayout.addLayout(presetLabelLayout)
        
        if len(self.__savedPresets) <= 0:
            return
        numOfButtons = len(self.__savedPresets)
        
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
                pattern = self.__savedPresets[patternId]
                name = pattern.GetName()
                desc = ",".join(pattern.GetColorList())
                #print "Name %s"%name
                newLabel = QLabel(desc)
                self.__setFont(newLabel,PATTERN_LABEL_FONT_SIZE)
                newButton = IDPushButton(self,name, patternId)
                newButton.setMinimumSize(MIN_BUTTON_WIDTH,MIN_BUTTON_HEIGHT)
                self.__setFont(newButton, PATTERN_BUTTON_FONT_SIZE)
                self.__buttons.append(newButton)
                newButtonLayout = QVBoxLayout()
                newButtonLayout.addWidget(newButton)
                labelLayout = QHBoxLayout()
                labelLayout.addStretch(1)
                labelLayout.addWidget(newLabel)
                labelLayout.addStretch(1)
                newButtonLayout.addLayout(labelLayout)
                newRow.addLayout(newButtonLayout)
                
            # Iflast row and < full, add stretch to left and right side (left done above)
            if lastRowStretch and i == numOfRows-1:
                newRow.addStretch(1)
            self.__presetButtonLayout.addLayout(newRow)
            
        
        
        
        
        
