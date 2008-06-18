# contact: ales.erjavec@fri.uni-lj.si
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
from OWSVM import *
from OWDataTable import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt SVM")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.tabs = QTabWidget(self, 'tabWidget')
        self.resize(800,600)
        self.verbosity = verbosity

        # create widget instances
        self.owFile = OWFile (self.tabs, signalManager = self.signalManager)
        self.owSVM = OWSVM (self.tabs, signalManager = self.signalManager)
        self.owData_Table = OWDataTable (self.tabs, signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owSVM.setEventHandler(self.eventHandler)
        self.owSVM.setProgressBarHandler(self.progressHandler)
        self.owData_Table.setEventHandler(self.eventHandler)
        self.owData_Table.setProgressBarHandler(self.progressHandler)
        
        #list of widget instances
        self.widgets = [self.owFile, self.owSVM, self.owData_Table, ]
        
        statusBar = QStatusBar(self)
        self.progress = QProgressBar(100, statusBar)
        self.progress.setMaximumWidth(80)
        self.progress.setMinimumWidth(80)
        self.progress.setCenterIndicator(1)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.progress, 1)
        statusBar.addWidget(self.status, 1)
        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owSVM)
        self.signalManager.addWidget(self.owData_Table)
        
        # add tabs
        self.tabs.insertTab (self.owFile, "File")
        self.owFile.captionTitle = 'File'
        self.owFile.setCaption(self.owFile.captionTitle)
        self.tabs.insertTab (self.owSVM, "SVM")
        self.owSVM.captionTitle = 'SVM'
        self.owSVM.setCaption(self.owSVM.captionTitle)
        self.tabs.insertTab (self.owData_Table, "Data Table")
        self.owData_Table.captionTitle = 'Data Table'
        self.owData_Table.setCaption(self.owData_Table.captionTitle)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owSVM, 'Examples', 'Example Table', 1)
        self.signalManager.addLink( self.owSVM, self.owData_Table, 'Support Vectors', 'Examples', 1)
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
            file = open("SVM.sav", "r")
        except:
            return
        strSettings = cPickle.load(file)
        file.close()
        self.owFile.loadSettingsStr(strSettings["File"])
        self.owFile.activateLoadedSettings()
        self.owSVM.loadSettingsStr(strSettings["SVM"])
        self.owSVM.activateLoadedSettings()
        self.owData_Table.loadSettingsStr(strSettings["Data Table"])
        self.owData_Table.activateLoadedSettings()
        
        
    def saveSettings(self):
        if DEBUG_MODE: return
        self.owData_Table.synchronizeContexts()
        self.owSVM.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["SVM"] = self.owSVM.saveSettingsStr()
        strSettings["Data Table"] = self.owData_Table.saveSettingsStr()
        
        file = open("SVM.sav", "w")
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
