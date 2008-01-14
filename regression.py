#This is automatically created file containing an Orange schema
# contact: jure.zabkar@fri.uni-lj.si janez.demsar@fri.uni-lj.si
# useonly: imports-85.tab
        
import sys, os, cPickle, orange, orngSignalManager, orngRegistry, OWGUI
import orngDebugging
orngRegistry.addWidgetDirectories()

from OWFile import *
from OWRegressionTree import *
from OWRegressionTreeViewer2D import *
from OWPade import *



class GUIApplication(QVBox):
    def __init__(self,parent=None):
        QVBox.__init__(self,parent)
        self.setCaption("Qt regression")
        self.signalManager = orngSignalManager.SignalManager()
        self.widgets = []
        

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owRegression_Tree = OWRegressionTree(signalManager = self.signalManager)
        self.owRegression_Tree_Graph = OWRegressionTreeViewer2D(signalManager = self.signalManager)
        self.owPade = OWPade(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owRegression_Tree, 'RegressionTree.png', 'Regression Tree', 1)
        self.setWidgetParameters(self.owRegression_Tree_Graph, 'icons/RegressionTreeGraph.png', 'Regression Tree Graph', 1)
        self.setWidgetParameters(self.owPade, 'icons/Pade.png', 'Pade', 1)
        
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
        self.signalManager.addLink( self.owFile, self.owRegression_Tree, 'Examples', 'Example Table', 1)
        self.signalManager.addLink( self.owRegression_Tree, self.owRegression_Tree_Graph, 'Regression Tree', 'Classification Tree', 1)
        self.signalManager.addLink( self.owFile, self.owPade, 'Examples', 'Examples', 1)
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
            file = open("regression.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owRegression_Tree.loadSettingsStr(strSettings["Regression Tree"]); self.owRegression_Tree.activateLoadedSettings()
            self.owRegression_Tree_Graph.loadSettingsStr(strSettings["Regression Tree Graph"]); self.owRegression_Tree_Graph.activateLoadedSettings()
            self.owPade.loadSettingsStr(strSettings["Pade"]); self.owPade.activateLoadedSettings()
            
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
        strSettings["Regression Tree"] = self.owRegression_Tree.saveSettingsStr()
        strSettings["Regression Tree Graph"] = self.owRegression_Tree_Graph.saveSettingsStr()
        strSettings["Pade"] = self.owPade.saveSettingsStr()
        
        file = open("regression.sav", "w")
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
        