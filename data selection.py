# contact: gregor.leban@fri.uni-lj.si

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
from OWDataDomain import *
from OWDataSampler import *
from OWSelectData import *
from OWCategorize import *
from OWContinuize import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt data selection")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.tabs = QTabWidget(self, 'tabWidget')
        self.resize(800,600)

        # create widget instances
        self.owFile = OWFile (self.tabs, signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain (self.tabs, signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler (self.tabs, signalManager = self.signalManager)
        self.owSelect_Data = OWSelectData (self.tabs, signalManager = self.signalManager)
        self.owDiscretize = OWCategorize (self.tabs, signalManager = self.signalManager)
        self.owContinuize = OWContinuize (self.tabs, signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owSelect_Attributes.setEventHandler(self.eventHandler)
        self.owSelect_Attributes.setProgressBarHandler(self.progressHandler)
        self.owData_Sampler.setEventHandler(self.eventHandler)
        self.owData_Sampler.setProgressBarHandler(self.progressHandler)
        self.owSelect_Data.setEventHandler(self.eventHandler)
        self.owSelect_Data.setProgressBarHandler(self.progressHandler)
        self.owDiscretize.setEventHandler(self.eventHandler)
        self.owDiscretize.setProgressBarHandler(self.progressHandler)
        self.owContinuize.setEventHandler(self.eventHandler)
        self.owContinuize.setProgressBarHandler(self.progressHandler)
        
        #list of widget instances
        self.widgets = [self.owFile, self.owSelect_Attributes, self.owData_Sampler, self.owSelect_Data, self.owDiscretize, self.owContinuize, ]
        
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
        self.signalManager.addWidget(self.owSelect_Attributes)
        self.signalManager.addWidget(self.owData_Sampler)
        self.signalManager.addWidget(self.owSelect_Data)
        self.signalManager.addWidget(self.owDiscretize)
        self.signalManager.addWidget(self.owContinuize)
        
        # add tabs
        self.tabs.insertTab (self.owFile, "File")
        self.owFile.captionTitle = 'File'
        self.owFile.setCaption(self.owFile.captionTitle)
        self.tabs.insertTab (self.owSelect_Attributes, "Select Attributes")
        self.owSelect_Attributes.captionTitle = 'Select Attributes'
        self.owSelect_Attributes.setCaption(self.owSelect_Attributes.captionTitle)
        self.tabs.insertTab (self.owData_Sampler, "Data Sampler")
        self.owData_Sampler.captionTitle = 'Data Sampler'
        self.owData_Sampler.setCaption(self.owData_Sampler.captionTitle)
        self.tabs.insertTab (self.owSelect_Data, "Select Data")
        self.owSelect_Data.captionTitle = 'Select Data'
        self.owSelect_Data.setCaption(self.owSelect_Data.captionTitle)
        self.tabs.insertTab (self.owDiscretize, "Discretize")
        self.owDiscretize.captionTitle = 'Discretize'
        self.owDiscretize.setCaption(self.owDiscretize.captionTitle)
        self.tabs.insertTab (self.owContinuize, "Continuize")
        self.owContinuize.captionTitle = 'Continuize'
        self.owContinuize.setCaption(self.owContinuize.captionTitle)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owFile, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owFile, self.owSelect_Data, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owContinuize, 'Classified Sampled Data', 'Classified Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owDiscretize, 'Classified Remaining Data', 'Classified Examples', 1)
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
            file = open("data selection.sav", "r")
        except:
            return
        strSettings = cPickle.load(file)
        file.close()
        self.owFile.loadSettingsStr(strSettings["File"])
        self.owFile.activateLoadedSettings()
        self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"])
        self.owSelect_Attributes.activateLoadedSettings()
        self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"])
        self.owData_Sampler.activateLoadedSettings()
        self.owSelect_Data.loadSettingsStr(strSettings["Select Data"])
        self.owSelect_Data.activateLoadedSettings()
        self.owDiscretize.loadSettingsStr(strSettings["Discretize"])
        self.owDiscretize.activateLoadedSettings()
        self.owContinuize.loadSettingsStr(strSettings["Continuize"])
        self.owContinuize.activateLoadedSettings()
        
        
    def saveSettings(self):
        if DEBUG_MODE: return
        self.owContinuize.synchronizeContexts()
        self.owDiscretize.synchronizeContexts()
        self.owSelect_Data.synchronizeContexts()
        self.owData_Sampler.synchronizeContexts()
        self.owSelect_Attributes.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Select Data"] = self.owSelect_Data.saveSettingsStr()
        strSettings["Discretize"] = self.owDiscretize.saveSettingsStr()
        strSettings["Continuize"] = self.owContinuize.saveSettingsStr()
        
        file = open("data selection.sav", "w")
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
