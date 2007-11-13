# contact: blaz.zupan@fri.uni-lj.si

import sys, os, cPickle, orange, orngSignalManager, orngRegistry
DEBUG_MODE = 0   #set to 1 to output debugging info to file 'signalManagerOutput.txt'
orngRegistry.addWidgetDirectories()
from OWFile import *
from OWClassificationTree import *
from OWClassificationTreeGraph import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        caption = 'classificationtree'
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
        self.owClassification_Tree = OWClassificationTree (self.tabs, signalManager = self.signalManager)
        self.owClassification_Tree_Graph = OWClassificationTreeGraph (self.tabs, signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owClassification_Tree.setEventHandler(self.eventHandler)
        self.owClassification_Tree.setProgressBarHandler(self.progressHandler)
        self.owClassification_Tree_Graph.setEventHandler(self.eventHandler)
        self.owClassification_Tree_Graph.setProgressBarHandler(self.progressHandler)
        
        #list of widget instances
        self.widgets = [self.owFile, self.owClassification_Tree, self.owClassification_Tree_Graph, ]
        
        statusBar = QStatusBar(self)
        self.progress = QProgressBar(100, statusBar)
        self.progress.setMaximumWidth(100)
        self.progress.setCenterIndicator(1)
        self.status = QLabel("", statusBar)
        self.status.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        statusBar.addWidget(self.progress, 1)
        statusBar.addWidget(self.status, 1)
        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owClassification_Tree)
        self.signalManager.addWidget(self.owClassification_Tree_Graph)
        
        # add tabs
        self.tabs.insertTab (self.owFile, "File")
        self.owFile.captionTitle = 'File'
        self.owFile.setCaption(self.owFile.captionTitle)
        self.tabs.insertTab (self.owClassification_Tree, "Classification Tree")
        self.owClassification_Tree.captionTitle = 'Classification Tree'
        self.owClassification_Tree.setCaption(self.owClassification_Tree.captionTitle)
        self.tabs.insertTab (self.owClassification_Tree_Graph, "Classification Tree Graph")
        self.owClassification_Tree_Graph.captionTitle = 'Classification Tree Graph'
        self.owClassification_Tree_Graph.setCaption(self.owClassification_Tree_Graph.captionTitle)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owClassification_Tree, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owClassification_Tree, self.owClassification_Tree_Graph, 'Classification Tree', 'Classification Tree', 1)
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
            file = open("classificationtree.sav", "r")
        except:
            return
        strSettings = cPickle.load(file)
        file.close()
        self.owFile.loadSettingsStr(strSettings["File"])
        self.owFile.activateLoadedSettings()
        self.owClassification_Tree.loadSettingsStr(strSettings["Classification Tree"])
        self.owClassification_Tree.activateLoadedSettings()
        self.owClassification_Tree_Graph.loadSettingsStr(strSettings["Classification Tree Graph"])
        self.owClassification_Tree_Graph.activateLoadedSettings()
        

    def saveSettings(self):
        if DEBUG_MODE: return
        self.owClassification_Tree_Graph.synchronizeContexts()
        self.owClassification_Tree.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Classification Tree"] = self.owClassification_Tree.saveSettingsStr()
        strSettings["Classification Tree Graph"] = self.owClassification_Tree_Graph.saveSettingsStr()
        
        file = open("classificationtree.sav", "w")
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
