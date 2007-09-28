# contact: blaz.zupan@fri.uni-lj.si
import sys, os, cPickle, orange, orngSignalManager, orngRegistry
DEBUG_MODE = 0   #set to 1 to output debugging info to file 'signalManagerOutput.txt'
orngRegistry.addWidgetDirectories()
from OWFile import *
from OWNaiveBayes import *
from OWTestLearners import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        caption = 'simple-evaluate and bayes'
        if (int(qVersion()[0]) >= 3):
            self.setCaption(caption)
        else:
            self.setCaption("Qt " + caption)
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.verbosity = verbosity
        self.tabs = QTabWidget(self, 'tabWidget')
        self.resize(800,600)

        # create widget instances
        self.owFile = OWFile (self.tabs, signalManager = self.signalManager)
        self.owNaive_Bayes = OWNaiveBayes (self.tabs, signalManager = self.signalManager)
        self.owTest_Learners = OWTestLearners (self.tabs, signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owNaive_Bayes.setEventHandler(self.eventHandler)
        self.owNaive_Bayes.setProgressBarHandler(self.progressHandler)
        self.owTest_Learners.setEventHandler(self.eventHandler)
        self.owTest_Learners.setProgressBarHandler(self.progressHandler)
        
        #list of widget instances
        self.widgets = [self.owFile, self.owNaive_Bayes, self.owTest_Learners, ]
        
        statusBar = QStatusBar(self)
        self.progress = QProgressBar(100, statusBar)
        self.progress.setMaximumWidth(100)
        self.progress.setCenterIndicator(1)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.progress, 1)
        statusBar.addWidget(self.status, 1)
        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owNaive_Bayes)
        self.signalManager.addWidget(self.owTest_Learners)
        
        # add tabs
        self.tabs.insertTab (self.owFile, "File")
        self.owFile.captionTitle = 'File'
        self.owFile.setCaption(self.owFile.captionTitle)
        self.tabs.insertTab (self.owNaive_Bayes, "Naive Bayes")
        self.owNaive_Bayes.captionTitle = 'Naive Bayes'
        self.owNaive_Bayes.setCaption(self.owNaive_Bayes.captionTitle)
        self.tabs.insertTab (self.owTest_Learners, "Test Learners")
        self.owTest_Learners.captionTitle = 'Test Learners'
        self.owTest_Learners.setCaption(self.owTest_Learners.captionTitle)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owTest_Learners, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owNaive_Bayes, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.setFreeze(0)
        

    def eventHandler(self, text, eventVerbosity = 1):
        if self.verbosity >= eventVerbosity:
            self.status.setText(text)

    def progressHandler(self, widget, val):
        if val < 0:
            self.status.setText("<nobr>Processing: <b>" + str(widget.captionTitle) + "</b></nobr>")
            self.progress.setProgress(0)
        elif val >100:
            self.status.setText("")
            self.progress.reset()
        else:
            self.progress.setProgress(val)
            self.update()



    def loadSettings(self):
        try:
            file = open("simple-evaluate and bayes.sav", "r")
        except:
            return
        strSettings = cPickle.load(file)
        file.close()
        self.owFile.loadSettingsStr(strSettings["File"])
        self.owFile.activateLoadedSettings()
        self.owNaive_Bayes.loadSettingsStr(strSettings["Naive Bayes"])
        self.owNaive_Bayes.activateLoadedSettings()
        self.owTest_Learners.loadSettingsStr(strSettings["Test Learners"])
        self.owTest_Learners.activateLoadedSettings()
        

    def saveSettings(self):
        if DEBUG_MODE: return
        self.owTest_Learners.synchronizeContexts()
        self.owNaive_Bayes.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Naive Bayes"] = self.owNaive_Bayes.saveSettingsStr()
        strSettings["Test Learners"] = self.owTest_Learners.saveSettingsStr()
        
        file = open("simple-evaluate and bayes.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()
        


if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    application.setMainWidget(ow)
    ow.show()

    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_loop()
    ow.saveSettings()
