#This is automatically created file containing an Orange schema
# contact: gregor.leban@fri.uni-lj.si
        
import sys, os, cPickle, orange, orngSignalManager, orngRegistry, OWGUI
import orngDebugging
orngRegistry.addWidgetDirectories()

from OWFile import *
from OWDataSampler import *
from OWDataDomain import *
from OWDiscretize import *
from OWContinuize import *
from OWSelectData import *



class GUIApplication(QVBox):
    def __init__(self,parent=None):
        QVBox.__init__(self,parent)
        self.setCaption("Qt data selection")
        self.signalManager = orngSignalManager.SignalManager()
        self.widgets = []
        

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owDiscretize = OWDiscretize(signalManager = self.signalManager)
        self.owContinuize = OWContinuize(signalManager = self.signalManager)
        self.owSelect_Data = OWSelectData(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owData_Sampler, 'icons/DataSampler.png', 'Data Sampler', 1)
        self.setWidgetParameters(self.owSelect_Attributes, 'icons/SelectAttributes.png', 'Select Attributes', 1)
        self.setWidgetParameters(self.owDiscretize, 'icons/Discretize.png', 'Discretize', 1)
        self.setWidgetParameters(self.owContinuize, 'icons/Continuize.png', 'Continuize', 1)
        self.setWidgetParameters(self.owSelect_Data, 'icons/SelectData.png', 'Select Data', 1)
        
        frameSpace = QFrame(self);  frameSpace.setMinimumHeight(20); frameSpace.setMaximumHeight(20)
        exitButton = QPushButton("E&xit",self)
        self.connect(exitButton,SIGNAL("clicked()"), application, SLOT("quit()"))
        
        
        statusBar = QStatusBar(self)
        self.progress = QProgressBar(100, statusBar)
        self.progress.setMaximumWidth(100)
        self.progress.setCenterIndicator(1)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.progress, 1)
        statusBar.addWidget(self.status, 1)
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owFile, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owDiscretize, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owContinuize, 'Remaining Examples', 'Examples', 1)
        self.signalManager.addLink( self.owFile, self.owSelect_Data, 'Examples', 'Examples', 1)
        self.signalManager.setFreeze(0)
        

    def setWidgetParameters(self, widget, iconName, caption, shown):
        self.signalManager.addWidget(widget)
        self.widgets.append(widget)
        widget.setEventHandler(self.eventHandler)
        widget.setProgressBarHandler(self.progressHandler)
        widget.setWidgetIcon(iconName)
        widget.setCaption(caption)
        if shown: OWGUI.button(self, self, caption, callback = widget.reshow)
        for dlg in getattr(widget, "wdChildDialogs", []):
            self.widgets.append(dlg)
            dlg.setEventHandler(self.eventHandler)
            dlg.setProgressBarHandler(self.progressHandler)
        
    def eventHandler(self, text, eventVerbosity = 1):
        if orngDebugging.orngVerbosity >= eventVerbosity:
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
            file = open("data selection.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"]); self.owData_Sampler.activateLoadedSettings()
            self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"]); self.owSelect_Attributes.activateLoadedSettings()
            self.owDiscretize.loadSettingsStr(strSettings["Discretize"]); self.owDiscretize.activateLoadedSettings()
            self.owContinuize.loadSettingsStr(strSettings["Continuize"]); self.owContinuize.activateLoadedSettings()
            self.owSelect_Data.loadSettingsStr(strSettings["Select Data"]); self.owSelect_Data.activateLoadedSettings()
            
        except:
            print "unable to load settings" 
            pass

    def saveSettings(self):
        if orngDebugging.orngDebuggingEnabled: return
        for widget in self.widgets[::-1]:
            widget.synchronizeContexts()
            widget.close()
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Discretize"] = self.owDiscretize.saveSettingsStr()
        strSettings["Continuize"] = self.owContinuize.saveSettingsStr()
        strSettings["Select Data"] = self.owSelect_Data.saveSettingsStr()
        
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
        