# contact: ales.erjavec324@email.si
import sys, os, cPickle, orange
import orngSignalManager

#set value in next line to 1 if want to output debugging info to file 'signalManagerOutput.txt'
DEBUG_MODE = 0

widgetDir = os.path.join(os.path.split(orange.__file__)[0], "OrangeWidgets")
if os.path.exists(widgetDir):
        for name in os.listdir(widgetDir):
            fullName = os.path.join(widgetDir, name)
            if os.path.isdir(fullName): sys.path.append(fullName)

from OWFile import *
from OWSOM import *
from OWSOMVisualizer import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt SOM")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.tabs = QTabWidget(self, 'tabWidget')
        self.resize(800,600)

        # create widget instances
        self.owFile = OWFile (self.tabs, signalManager = self.signalManager)
        self.owSOM = OWSOM (self.tabs, signalManager = self.signalManager)
        self.owSOMVisualizer = OWSOMVisualizer (self.tabs, signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owSOM.setEventHandler(self.eventHandler)
        self.owSOM.setProgressBarHandler(self.progressHandler)
        self.owSOMVisualizer.setEventHandler(self.eventHandler)
        self.owSOMVisualizer.setProgressBarHandler(self.progressHandler)
        
        #list of widget instances
        self.widgets = [self.owFile, self.owSOM, self.owSOMVisualizer, ]
        
        statusBar = QStatusBar(self)
        self.caption = QLabel('', statusBar)
        self.caption.setMaximumWidth(230)
        self.progress = QProgressBar(100, statusBar)
        self.progress.setMaximumWidth(100)
        self.progress.setCenterIndicator(1)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.caption, 1)
        statusBar.addWidget(self.progress, 1)
        statusBar.addWidget(self.status, 1)
        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owSOM)
        self.signalManager.addWidget(self.owSOMVisualizer)
        
        # add tabs
        self.tabs.insertTab (self.owFile, "File")
        self.owFile.captionTitle = 'File'
        self.owFile.setCaption(self.owFile.captionTitle)
        self.tabs.insertTab (self.owSOM, "SOM")
        self.owSOM.captionTitle = 'SOM'
        self.owSOM.setCaption(self.owSOM.captionTitle)
        self.tabs.insertTab (self.owSOMVisualizer, "SOMVisualizer")
        self.owSOMVisualizer.captionTitle = 'SOMVisualizer'
        self.owSOMVisualizer.setCaption(self.owSOMVisualizer.captionTitle)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owSOM, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSOM, self.owSOMVisualizer, 'SOMMap', 'SOMMap', 1)
        self.signalManager.setFreeze(0)
        

    def eventHandler(self, text):
        self.status.setText(text)
        
    def progressHandler(self, widget, val):
        if val < 0:
            self.caption.setText("<nobr>Processing: <b>" + str(widget.captionTitle) + "</b></nobr>")
            self.progress.setProgress(0)
        elif val >100:
            self.caption.setText("")
            self.progress.reset()
        else:
            self.progress.setProgress(val)
            self.update()


        
    def loadSettings(self):
        try:
            file = open("SOM.sav", "r")
        except:
            return
        strSettings = cPickle.load(file)
        file.close()
        self.owFile.loadSettingsStr(strSettings["File"])
        self.owFile.activateLoadedSettings()
        self.owSOM.loadSettingsStr(strSettings["SOM"])
        self.owSOM.activateLoadedSettings()
        self.owSOMVisualizer.loadSettingsStr(strSettings["SOMVisualizer"])
        self.owSOMVisualizer.activateLoadedSettings()
        
        
    def saveSettings(self):
        if DEBUG_MODE: return
        self.owSOMVisualizer.synchronizeContexts()
        self.owSOM.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["SOM"] = self.owSOM.saveSettingsStr()
        strSettings["SOMVisualizer"] = self.owSOMVisualizer.saveSettingsStr()
        
        file = open("SOM.sav", "w")
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
