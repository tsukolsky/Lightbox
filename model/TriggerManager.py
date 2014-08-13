import os, sys
from util.Events import Event
from util.Triggers import DurationTrigger

## Types of triggers --------------------
FIELD_TYPE = "FieldType"
DURATION_TRIGGER = "DurationTrigger"

## Types of actions for those triggers ---
FIELD_ACTIONTYPE = "FieldActionType"
ACTIONTYPE_START = "ActionStart"
ACTIONTYPE_STOP = "ActionStop"

## Params for actions -------------------
FIELD_DURATION = "FieldDuration"

## TAG -------------------------------
TAG = "Tag"
START_DURATION_UPDATE = "StartDurationUpdate"
STOP_DURATION_UPDATE = "StopDurationUpdate"
START_TRIGGER_ACTIVATED = "StartTriggerActivated"
STOP_TRIGGER_ACTIVATED = "StopTriggerActivated"

class TriggerManager():
    def __init__(self, log = None):
        self.log = log
        self.CALLING_CLASS = "TriggerManager"
        self.__triggerHandlers = dict()
        self.__triggerHandlers[DURATION_TRIGGER] = self.__handleDurationTrigger
        self.__activeTriggers = list()
        self.__startTriggers = dict()
        self.__stopTriggers = dict()
        self.__log("Initialized")
        
        self.StopEvent = Event()
        self.StartEvent = Event()
        
    def __log(self, message):
        if self.log != None:
            self.log.LOG(self.CALLING_CLASS, message)
         
    def HasStartTrigger(self):
        if len(self.__startTriggers) > 0:
            return True
        else:
            return False
        
    def GlobalStart(self):   
        self.__log("Starting start triggers.")
        for tag, trigger in self.__startTriggers.iteritems():
            if not trigger.IsRunning():
                trigger.start()
            else:
                trigger.Resume()
        
    def InitializeStopTriggers(self):
        self.__log("Initializing stop triggers")
        for tag, trigger in self.__stopTriggers.iteritems():
            if trigger.IsRunning():
                trigger.Resume()
            else:
                trigger.start()
                
    def GlobalStop(self):
        self.__log("Stopping all triggers.")
        for tag, trigger in self.__startTriggers.iteritems():
            if trigger.IsRunning():
                trigger.Pause()
            
        for tag, trigger in self.__stopTriggers.iteritems():
            if trigger.IsRunning():
                trigger.Pause()
        
    def CreateTrigger(self, optDict):
        self.__log("Got a request for new trigger")
        triggerType = optDict[FIELD_TYPE]
        if (triggerType in self.__triggerHandlers):
            handler = self.__triggerHandlers[triggerType]
            created = handler(optDict)
            return created
        else:
            return False
        
    def DeleteTrigger(self, triggerId):
        self.__log("Got a request to delete trigger with ID %d"%int(triggerId))
        if triggerId <= (len(self.__activeTriggers) - 1):
            del self.__activeTriggers[triggerId]
            return True
        else:
            return False
        
    def __handleDurationTrigger(self, optDict):
        self.__log("Request for new Duration Trigger")
        retBool = False
        if FIELD_DURATION in optDict:
            duration = optDict[FIELD_DURATION]
            ## Check to see if we have a start duration trigger already
            retBool = True
            triggerAction = optDict[FIELD_ACTIONTYPE]
            if triggerAction == ACTIONTYPE_START:
                trigger = DurationTrigger(duration)
                if DURATION_TRIGGER in self.__startTriggers:
                    oldTrigger = self.__startTriggers[DURATION_TRIGGER]
                    oldTrigger.DurationTimeUpdated.unsubscribe()
                    oldTrigger.join()
                self.__startTriggers[DURATION_TRIGGER] = trigger
                trigger.DurationTimeUpdated.subscribe(self.__handleStartDurationTriggerUpdated)
                self.__handleStartDurationTriggerUpdated(duration)
                self.__log("Start Trigger: Duration is now added.")
            elif triggerAction == ACTIONTYPE_STOP:
                trigger = DurationTrigger(duration)
                if DURATION_TRIGGER in self.__stopTriggers:
                    oldTrigger = self.__stopTriggers[DURATION_TRIGGER]
                    oldTrigger.DurationTimeUpdated.unsubscribe()
                    oldTrigger.join()
                self.__stopTriggers[DURATION_TRIGGER] = trigger
                trigger.DurationTimeUpdated.subscribe(self.__handleStopDurationTriggerUpdated)
                # Update the trigger now because we just added it
                self.__handleStopDurationTriggerUpdated(duration)
                self.__log("Stop Trigger: Duration is now added.")
            else:
                self.__log("Invalid action type")
                retBool = False
        return retBool
            
    def __handleStartDurationTriggerUpdated(self, timeUpdate):
        if timeUpdate > 0:
            bundle = dict()
            bundle[TAG] = START_DURATION_UPDATE
            bundle[FIELD_DURATION] = timeUpdate
            self.__log("Duration time updated to %d"%timeUpdate)
            self.StartEvent(bundle)
        else:
            bundle = dict()
            bundle[TAG] = START_TRIGGER_ACTIVATED
            bundle[FIELD_DURATION] = timeUpdate
            self.__log("Duration time updated to 0, start task.")
            self.StartEvent(bundle)
        
    def __handleStopDurationTriggerUpdated(self, timeUpdate):
        bundle = dict()
        if timeUpdate > 0:
            bundle[TAG] = STOP_DURATION_UPDATE
            bundle[FIELD_DURATION] = timeUpdate
            self.StopEvent(bundle)
        else:
            bundle[TAG] = STOP_TRIGGER_ACTIVATED
            bundle[FIELD_DURATION] = timeUpdate
            self.__log("Duration time updated to 0, stop task.")
            self.StopEvent(bundle)
    
            

