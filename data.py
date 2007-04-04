# contact: ales.erjavec@fri.uni-lj.si janez.demsar@fri.uni-lj.si blaz.zupan@fri.uni-lj.si

import sys, os, cPickle, orange, orngSignalManager, orngRegistry
DEBUG_MODE = 0   #set to 1 to output debugging info to file 'signalManagerOutput.txt'
orngRegistry.addWidgetDirectories()
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


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt data")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.verbosity = verbosity

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
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owSelect_Attributes.setEventHandler(self.eventHandler)
        self.owSelect_Attributes.setProgressBarHandler(self.progressHandler)
        self.owData_Sampler.setEventHandler(self.eventHandler)
        self.owData_Sampler.setProgressBarHandler(self.progressHandler)
        self.owRank.setEventHandler(self.eventHandler)
        self.owRank.setProgressBarHandler(self.progressHandler)
        self.owDiscretize.setEventHandler(self.eventHandler)
        self.owDiscretize.setProgressBarHandler(self.progressHandler)
        self.owContinuize.setEventHandler(self.eventHandler)
        self.owContinuize.setProgressBarHandler(self.progressHandler)
        self.owPurge_Domain.setEventHandler(self.eventHandler)
        self.owPurge_Domain.setProgressBarHandler(self.progressHandler)
        self.owSelect_Data.setEventHandler(self.eventHandler)
        self.owSelect_Data.setProgressBarHandler(self.progressHandler)
        self.owImpute.setEventHandler(self.eventHandler)
        self.owImpute.setProgressBarHandler(self.progressHandler)
        self.owData_Table.setEventHandler(self.eventHandler)
        self.owData_Table.setProgressBarHandler(self.progressHandler)
        

        #list of widget instances
        self.widgets = [self.owFile, self.owSelect_Attributes, self.owData_Sampler, self.owRank, self.owDiscretize, self.owContinuize, self.owPurge_Domain, self.owSelect_Data, self.owImpute, self.owData_Table, ]
        # set widget captions
        self.owFile.setCaptionTitle('Qt File')
        self.owSelect_Attributes.setCaptionTitle('Qt Select Attributes')
        self.owData_Sampler.setCaptionTitle('Qt Data Sampler')
        self.owRank.setCaptionTitle('Qt Rank')
        self.owDiscretize.setCaptionTitle('Qt Discretize')
        self.owContinuize.setCaptionTitle('Qt Continuize')
        self.owPurge_Domain.setCaptionTitle('Qt Purge Domain')
        self.owSelect_Data.setCaptionTitle('Qt Select Data')
        self.owImpute.setCaptionTitle('Qt Impute')
        self.owData_Table.setCaptionTitle('Qt Data Table')
        
        # set icons
        self.owFile.setWidgetIcon('icons/File.png')
        self.owSelect_Attributes.setWidgetIcon('icons/SelectAttributes.png')
        self.owData_Sampler.setWidgetIcon('icons/DataSampler.png')
        self.owRank.setWidgetIcon('icons/Rank.png')
        self.owDiscretize.setWidgetIcon('icons/Discretize.png')
        self.owContinuize.setWidgetIcon('icons/Continuize.png')
        self.owPurge_Domain.setWidgetIcon('icons/PurgeDomain.png')
        self.owSelect_Data.setWidgetIcon('icons/SelectData.png')
        self.owImpute.setWidgetIcon('icons/Impute.png')
        self.owData_Table.setWidgetIcon('icons/DataTable.png')
        
        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owSelect_Attributes)
        self.signalManager.addWidget(self.owData_Sampler)
        self.signalManager.addWidget(self.owRank)
        self.signalManager.addWidget(self.owDiscretize)
        self.signalManager.addWidget(self.owContinuize)
        self.signalManager.addWidget(self.owPurge_Domain)
        self.signalManager.addWidget(self.owSelect_Data)
        self.signalManager.addWidget(self.owImpute)
        self.signalManager.addWidget(self.owData_Table)
        
        # create widget buttons
        owButtonFile = QPushButton("File", self)
        owButtonSelect_Attributes = QPushButton("Select Attributes", self)
        owButtonData_Sampler = QPushButton("Data Sampler", self)
        owButtonRank = QPushButton("Rank", self)
        owButtonDiscretize = QPushButton("Discretize", self)
        owButtonContinuize = QPushButton("Continuize", self)
        owButtonPurge_Domain = QPushButton("Purge Domain", self)
        owButtonSelect_Data = QPushButton("Select Data", self)
        owButtonImpute = QPushButton("Impute", self)
        owButtonData_Table = QPushButton("Data Table", self)
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
        #connect GUI buttons to show widgets
        self.connect(owButtonFile ,SIGNAL("clicked()"), self.owFile.reshow)
        self.connect(owButtonSelect_Attributes ,SIGNAL("clicked()"), self.owSelect_Attributes.reshow)
        self.connect(owButtonData_Sampler ,SIGNAL("clicked()"), self.owData_Sampler.reshow)
        self.connect(owButtonRank ,SIGNAL("clicked()"), self.owRank.reshow)
        self.connect(owButtonDiscretize ,SIGNAL("clicked()"), self.owDiscretize.reshow)
        self.connect(owButtonContinuize ,SIGNAL("clicked()"), self.owContinuize.reshow)
        self.connect(owButtonPurge_Domain ,SIGNAL("clicked()"), self.owPurge_Domain.reshow)
        self.connect(owButtonSelect_Data ,SIGNAL("clicked()"), self.owSelect_Data.reshow)
        self.connect(owButtonImpute ,SIGNAL("clicked()"), self.owImpute.reshow)
        self.connect(owButtonData_Table ,SIGNAL("clicked()"), self.owData_Table.reshow)
        
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
            file = open("data.sav", "r")
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
        self.owRank.loadSettingsStr(strSettings["Rank"])
        self.owRank.activateLoadedSettings()
        self.owDiscretize.loadSettingsStr(strSettings["Discretize"])
        self.owDiscretize.activateLoadedSettings()
        self.owContinuize.loadSettingsStr(strSettings["Continuize"])
        self.owContinuize.activateLoadedSettings()
        self.owPurge_Domain.loadSettingsStr(strSettings["Purge Domain"])
        self.owPurge_Domain.activateLoadedSettings()
        self.owSelect_Data.loadSettingsStr(strSettings["Select Data"])
        self.owSelect_Data.activateLoadedSettings()
        self.owImpute.loadSettingsStr(strSettings["Impute"])
        self.owImpute.activateLoadedSettings()
        self.owData_Table.loadSettingsStr(strSettings["Data Table"])
        self.owData_Table.activateLoadedSettings()
        

    def saveSettings(self):
        if DEBUG_MODE: return
        self.owData_Table.synchronizeContexts()
        self.owImpute.synchronizeContexts()
        self.owSelect_Data.synchronizeContexts()
        self.owPurge_Domain.synchronizeContexts()
        self.owContinuize.synchronizeContexts()
        self.owDiscretize.synchronizeContexts()
        self.owRank.synchronizeContexts()
        self.owData_Sampler.synchronizeContexts()
        self.owSelect_Attributes.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
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
    application.setMainWidget(ow)
    ow.show()

    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_loop()
    ow.saveSettings()
