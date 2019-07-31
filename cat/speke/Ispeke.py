from abc import ABCMeta, abstractmethod

class ISpeke:
    __metaclass__ = ABCMeta


    @abstractmethod
    def initialize(self, userNumber, id):
        pass

    @abstractmethod
    def setPassword(self, userNumber, id, password):
        pass

    @abstractmethod
    def initializeUserInstance(self, userInstance):
        pass

    @abstractmethod
    def terminateUserInstance(self, userInstance):
        pass

    @abstractmethod
    def testInstancePassword(self, userInstance, passwordGuess):
        pass

    @abstractmethod
    def getKey(self, userInstance):
        pass

    @abstractmethod
    def sendKey(self, userInstance, key):
        pass

    @abstractmethod
    def getChallenge(self, userInstance):
        pass

    @abstractmethod
    def sendChallenge(self, userInstance, challenge):
        pass

    @abstractmethod
    def application(self):
        pass
