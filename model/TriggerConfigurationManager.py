import os, sys, time
from util.Events import Event
from util.MyPushButton import TagPushButton, IdPushButton
from PyQt4.QtGui import QSlideBar

SAVE    = "Save Triggers"
RESET   = "Reset Triggers"
BACK    = "Back"

class ConfigurationManager():
    def __init__(self, parent, log = None):
        self.log = log
        self.__parent = parent
        self.CALLING_CLASS = "ConfigurationManager"
        self.ConfigurationReset = Event()
        self.ConfigurationSaved = Event()
        self.ConfigurationAborted = Event()
        
    def __log(self, message, callingClass = None):
        if self.log != None:
            callingClassprint = self.CALLING_CLASS
            if callingClass != None:
                callingClassprint = callingClass
            self.log.LOG(callingClassprint, message)
    
    def __setFont(self, object, size):
        font = QFont(object.font())
        font.setPointSize(size)
        object.setFont(font)
          
########################################
## Class: Trigger Configuraiton Manager
## Should dislay two sets of options: 
## 1) start trigger based on time duration
## 2) stop trigger base
## For this to work, the MianWindow needs a few Events that the managers can access
## in order to post the correct GUI
########################################

class TriggerConfigurationManager(ConfigurationManager):
    def __init__(self, parent, log = None):
        super(TargetConfigurationManager, self).__init__(parent, log)
        self.CALLING_CLASS = "TriggerConfigurationManager"
        
    def setupLayout(self):
        self.__parent.ClearLayouts()
        
        triggerConfigLayout = QVBoxLayout()
        triggerConfigLabel = QLabel("Start & Stop Configuration")
        
        backButton = TagPushButton(self, BACK)
        saveButton = TagPushButton(self, SAVE)
        resetButton = TagPushButton(self, RESET)
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(resetButton)
        controlLayout.addStretch(1)
        controlLayout.addWidget(saveButton)
        controlLayout.addWidget(backButton)
        
        # Should be a slider between 0-60 seconds
        sliderLayout = QVBoxLayout()
        startTriggerSliderLayout = QHBoxLayout()
        stopTriggerSliderLayout = QHBoxLayout()
        
        startLabel = QLabel("Start Trigger Duration (s)")
        stopLabel = QLabel("Stop Trigger Duration (s)")
        
        startTriggerSlider = QSlider(range(0,61))
        stopTriggerSlider = QSlider(range(0,61))
        
        startTriggerSliderLayout.addWidget(startLabel)
        startTriggerSliderLayout.addStretch(1)
        startTriggerSliderLayout.addWidget(startTriggerSlider)
        
        stopTriggerSliderLayout.addWidget(stopLabel)
        stopTriggerSliderLayout.addStretch(1)
        stopTriggerSliderLayout.addWidget(stopTriggerSlider)
         
        sliderLayout.addLayout(startTriggerSliderLayout)
        sliderLayout.addLayout(stopTriggerSliderLayout)
        
        triggerConfigLayout.addWidget(triggerConfigLabel)
        triggerConfigLayout.addLayout(startTriggerSliderLayout)
        triggerConfigLayout.addLayout(stopTriggerSliderLayout)
        triggerConfigLayout.addLayout(controlLayout)
        
        self.__parent.AssignMainLayout(triggerConfigLayout)
        
         