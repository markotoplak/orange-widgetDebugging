#This is automatically created file containing an Orange schema
        
import orngOrangeFoldersQt4
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI

from OWFile import *
from OWDataDomain import *
from OWDataSampler import *
from OWRank import *
from OWDiscretize import *
from OWContinuize import *
from OWPurgeDomain import *
from OWSelectData import *
from OWImpute import *
from OWDataTable import *



class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'data', signalManager = self.signalManager)
        self.widgets = []
        
        self.setLayout(QVBoxLayout())
        self.box = OWGUI.widgetBox(self, 'Widgets')

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owRank = OWRank(signalManager = self.signalManager)
        self.owDiscretize = OWDiscretize(signalManager = self.signalManager)
        self.owContinuize = OWContinuize(signalManager = self.signalManager)
        self.owPurge_Domain = OWPurgeDomain(signalManager = self.signalManager)
        self.owSelect_Data = OWSelectData(signalManager = self.signalManager)
        self.owImpute = OWImpute(signalManager = self.signalManager)
        self.owData_Table = OWDataTable(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owSelect_Attributes, 'icons/SelectAttributes.png', 'Select Attributes', 1)
        self.setWidgetParameters(self.owData_Sampler, 'icons/DataSampler.png', 'Data Sampler', 1)
        self.setWidgetParameters(self.owRank, 'icons/Rank.png', 'Rank', 1)
        self.setWidgetParameters(self.owDiscretize, 'icons/Discretize.png', 'Discretize', 1)
        self.setWidgetParameters(self.owContinuize, 'icons/Continuize.png', 'Continuize', 1)
        self.setWidgetParameters(self.owPurge_Domain, 'icons/PurgeDomain.png', 'Purge Domain', 1)
        self.setWidgetParameters(self.owSelect_Data, 'icons/SelectData.png', 'Select Data', 1)
        self.setWidgetParameters(self.owImpute, 'icons/Impute.png', 'Impute', 1)
        self.setWidgetParameters(self.owData_Table, 'icons/DataTable.png', 'Data Table', 1)
        
        box2 = OWGUI.widgetBox(self, 1)
        exitButton = OWGUI.button(box2, self, "Exit", callback = self.accept)
        self.layout().addStretch(100)
        
        statusBar = QStatusBar(self)
        self.layout().addWidget(statusBar)
        self.caption = QLabel('', statusBar)
        self.caption.setMaximumWidth(230)
        self.progress = QProgressBar(statusBar)
        self.progress.setMaximumWidth(100)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.progress)
        statusBar.addWidget(self.caption)
        statusBar.addWidget(self.status)
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owRank, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owDiscretize, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owContinuize, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owPurge_Domain, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owSelect_Data, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owImpute, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owData_Table, 'Examples', 'Examples', 1)
        self.signalManager.setFreeze(0)
        

    def setWidgetParameters(self, widget, iconName, caption, shown):
        widget.setEventHandler(self.eventHandler)
        widget.setProgressBarHandler(self.progressHandler)
        widget.setWidgetIcon(iconName)
        widget.setWindowTitle(caption)
        self.signalManager.addWidget(widget)
        self.widgets.append(widget)
        if shown: OWGUI.button(self.box, self, caption, callback = widget.reshow)
        for dlg in getattr(widget, "wdChildDialogs", []):
            self.widgets.append(dlg)
            dlg.setEventHandler(self.eventHandler)
            dlg.setProgressBarHandler(self.progressHandler)
        
    def eventHandler(self, text, eventVerbosity = 1):
        if orngDebugging.orngVerbosity >= eventVerbosity:
            self.status.setText(text)

    def progressHandler(self, widget, val):
        if val < 0:
            self.caption.setText("<nobr>Processing: <b>" + str(widget.captionTitle) + "</b></nobr>")
            self.progress.setValue(0)
        elif val >100:
            self.caption.setText("")
            self.progress.reset()
        else:
            self.progress.setValue(val)
            self.update()

    def loadSettings(self):
        try:
            file = open("data.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"]); self.owSelect_Attributes.activateLoadedSettings()
            self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"]); self.owData_Sampler.activateLoadedSettings()
            self.owRank.loadSettingsStr(strSettings["Rank"]); self.owRank.activateLoadedSettings()
            self.owDiscretize.loadSettingsStr(strSettings["Discretize"]); self.owDiscretize.activateLoadedSettings()
            self.owContinuize.loadSettingsStr(strSettings["Continuize"]); self.owContinuize.activateLoadedSettings()
            self.owPurge_Domain.loadSettingsStr(strSettings["Purge Domain"]); self.owPurge_Domain.activateLoadedSettings()
            self.owSelect_Data.loadSettingsStr(strSettings["Select Data"]); self.owSelect_Data.activateLoadedSettings()
            self.owImpute.loadSettingsStr(strSettings["Impute"]); self.owImpute.activateLoadedSettings()
            self.owData_Table.loadSettingsStr(strSettings["Data Table"]); self.owData_Table.activateLoadedSettings()
            
        except:
            print "unable to load settings" 
            pass

    def closeEvent(self, ev):
        OWBaseWidget.closeEvent(self, ev)
        if orngDebugging.orngDebuggingEnabled: return
        for widget in self.widgets[::-1]:
            widget.synchronizeContexts()
            widget.close()
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Rank"] = self.owRank.saveSettingsStr()
        strSettings["Discretize"] = self.owDiscretize.saveSettingsStr()
        strSettings["Continuize"] = self.owContinuize.saveSettingsStr()
        strSettings["Purge Domain"] = self.owPurge_Domain.saveSettingsStr()
        strSettings["Select Data"] = self.owSelect_Data.saveSettingsStr()
        strSettings["Impute"] = self.owImpute.saveSettingsStr()
        strSettings["Data Table"] = self.owData_Table.saveSettingsStr()
        
        file = open("data.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        