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
from OWInteractiveDiscretization import *
from OWDataTable import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt InteractiveDiscretization")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.tabs = QTabWidget(self, 'tabWidget')
        self.resize(800,600)

        # create widget instances
        self.owFile = OWFile (self.tabs, signalManager = self.signalManager)
        self.owInteractive_Discretization = OWInteractiveDiscretization (self.tabs, signalManager = self.signalManager)
        self.owData_Table = OWDataTable (self.tabs, signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owInteractive_Discretization.setEventHandler(self.eventHandler)
        self.owInteractive_Discretization.setProgressBarHandler(self.progressHandler)
        self.owData_Table.setEventHandler(self.eventHandler)
        self.owData_Table.setProgressBarHandler(self.progressHandler)
        
        #list of widget instances
        self.widgets = [self.owFile, self.owInteractive_Discretization, self.owData_Table, ]
        
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
        self.signalManager.addWidget(self.owInteractive_Discretization)
        self.signalManager.addWidget(self.owData_Table)
        
        # add tabs
        self.tabs.insertTab (self.owFile, "File")
        self.owFile.captionTitle = 'File'
        self.owFile.setCaption(self.owFile.captionTitle)
        self.tabs.insertTab (self.owInteractive_Discretization, "Interactive Discretization")
        self.owInteractive_Discretization.captionTitle = 'Interactive Discretization'
        self.owInteractive_Discretization.setCaption(self.owInteractive_Discretization.captionTitle)
        self.tabs.insertTab (self.owData_Table, "Data Table")
        self.owData_Table.captionTitle = 'Data Table'
        self.owData_Table.setCaption(self.owData_Table.captionTitle)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owInteractive_Discretization, 'Classified Examples', 'Examples', 1)
        self.signalManager.addLink( self.owInteractive_Discretization, self.owData_Table, 'Examples', 'Examples', 1)
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
            file = open("InteractiveDiscretization.sav", "r")
        except:
            return
        strSettings = cPickle.load(file)
        file.close()
        self.owFile.loadSettingsStr(strSettings["File"])
        self.owFile.activateLoadedSettings()
        self.owInteractive_Discretization.loadSettingsStr(strSettings["Interactive Discretization"])
        self.owInteractive_Discretization.activateLoadedSettings()
        self.owData_Table.loadSettingsStr(strSettings["Data Table"])
        self.owData_Table.activateLoadedSettings()
        
        
    def saveSettings(self):
        if DEBUG_MODE: return
        self.owData_Table.synchronizeContexts()
        self.owInteractive_Discretization.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Interactive Discretization"] = self.owInteractive_Discretization.saveSettingsStr()
        strSettings["Data Table"] = self.owData_Table.saveSettingsStr()
        
        file = open("InteractiveDiscretization.sav", "w")
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
