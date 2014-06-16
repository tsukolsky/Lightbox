class Event():
    def __init__(self):
        self.__delegates = list()
        
    def subscribe(self,delegate):
        self.__delegates.append(delegate)
        
    def __call__(self, *args):
        rmv = []
        delegates = list(self.__delegates)
        for delegate in delegates:
            delegate(*args)
            
    def unsubscribe(self,delegate):
        if (self.__delegates.__contains__(delegate)):
            self.__delegates.remove(delegate)
            
    def __iadd__(self,delegate):
        self.subscribe(delegate)
        return self
    
    def __isub__(self, delgate):
        self.unsubscribe(delgate)
        return self