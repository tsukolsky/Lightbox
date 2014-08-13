import os, sys
from util.Events import Event
from util.Triggers import DurationTrigger

DURATION_TRIGGER = "DurationTrigger"
FIELD_DURATION = "FieldDuration"

class TriggerManager():
    def __init__(self, log = None):
        self.log = log
        self.CALLING_CLASS = "TriggerManager"
        self.__triggerHandlers = dict()
        self.__triggerHandlers[DURATION_TRIGGER] = self.__handleDurationTrigger
        self.__activeTriggers = list()
        self.__log("Initialized")
        
    def __log(self, message):
        if self.log != None:
            self.log.LOG(self.CALLING_CLASS, message)
            
    def CreateTrigger(self, triggerType, optDict = None):
        self.__log("Got a request for new trigger with type %s"%str(triggerType))
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
        
    def __handleDurationTrigger(self, optDict = None):
        self.__log("Request for new Duration Trigger")
        if FIELD_DURATION in optDict:
            duration = optDict[FIELD_DURATION]
            id = len(self.__activeTriggers)
            trigger = DurationTrigger(id,duration)
            self.__activeTriggers += [trigger]
            self.__log("Successfully made the duration trigger.")
            return True
        else:
            return False
            
    
            

