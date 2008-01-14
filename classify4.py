#This is automatically created file containing an Orange schema
# contact: marko.toplak@fri.uni-lj.si
        
import sys, os, cPickle, orange, orngSignalManager, orngRegistry, OWGUI
import orngDebugging
orngRegistry.addWidgetDirectories()

from OWFile import *
from OWRandomForest import *
from OWTestLearners import *
from OWROC import *
from OWLiftCurve import *



class GUIApplication(QVBox):
    def __init__(self,parent=None):
        QVBox.__init__(self,parent)
        self.setCaption("Qt random forest")
        self.signalManager = orngSignalManager.SignalManager()
        self.widgets = []
        

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owRandom_Forest = OWRandomForest(signalManager = self.signalManager)
        self.owTest_Learners = OWTestLearners(signalManager = self.signalManager)
        self.owROC_Analysis = OWROC(signalManager = self.signalManager)
        self.owLift_Curve = OWLiftCurve(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owRandom_Forest, 'icons/RandomForest.png', 'Random Forest', 1)
        self.setWidgetParameters(self.owTest_Learners, 'icons/TestLearners.png', 'Test Learners', 1)
        self.setWidgetParameters(self.owROC_Analysis, 'ROCAnalysis.png', 'ROC Analysis', 1)
        self.setWidgetParameters(self.owLift_Curve, 'LiftCurve.png', 'Lift Curve', 1)
        
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
        self.signalManager.addLink( self.owFile, self.owTest_Learners, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owRandom_Forest, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owLift_Curve, 'Evaluation Results', 'Evaluation Results', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owROC_Analysis, 'Evaluation Results', 'Evaluation Results', 1)
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
            file = open("random forest.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owRandom_Forest.loadSettingsStr(strSettings["Random Forest"]); self.owRandom_Forest.activateLoadedSettings()
            self.owTest_Learners.loadSettingsStr(strSettings["Test Learners"]); self.owTest_Learners.activateLoadedSettings()
            self.owROC_Analysis.loadSettingsStr(strSettings["ROC Analysis"]); self.owROC_Analysis.activateLoadedSettings()
            self.owLift_Curve.loadSettingsStr(strSettings["Lift Curve"]); self.owLift_Curve.activateLoadedSettings()
            
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
        strSettings["Random Forest"] = self.owRandom_Forest.saveSettingsStr()
        strSettings["Test Learners"] = self.owTest_Learners.saveSettingsStr()
        strSettings["ROC Analysis"] = self.owROC_Analysis.saveSettingsStr()
        strSettings["Lift Curve"] = self.owLift_Curve.saveSettingsStr()
        
        file = open("random forest.sav", "w")
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
        