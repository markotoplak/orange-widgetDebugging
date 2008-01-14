#This is automatically created file containing an Orange schema
# contact: tomaz.curk@fri.uni-lj.si blaz.zupan@fri.uni-lj.si
        
import sys, os, cPickle, orange, orngSignalManager, orngRegistry, OWGUI
import orngDebugging
orngRegistry.addWidgetDirectories()

from OWFile import *
from OWDataDomain import *
from OWDataSampler import *
from OWNaiveBayes import *
from OWKNN import *
from OWClassificationTree import *
from OWTestLearners import *
from OWROC import *
from OWLiftCurve import *
from OWCalibrationPlot import *
from OWConfusionMatrix import *



class GUIApplication(QVBox):
    def __init__(self,parent=None):
        QVBox.__init__(self,parent)
        self.setCaption("Qt Evaluate2")
        self.signalManager = orngSignalManager.SignalManager()
        self.widgets = []
        

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owNaive_Bayes = OWNaiveBayes(signalManager = self.signalManager)
        self.owk_Nearest_Neighbours = OWKNN(signalManager = self.signalManager)
        self.owClassification_Tree = OWClassificationTree(signalManager = self.signalManager)
        self.owTest_Learners = OWTestLearners(signalManager = self.signalManager)
        self.owROC_Analysis = OWROC(signalManager = self.signalManager)
        self.owLift_Curve = OWLiftCurve(signalManager = self.signalManager)
        self.owCalibration_Plot = OWCalibrationPlot(signalManager = self.signalManager)
        self.owConfusion_Matrix = OWConfusionMatrix(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owSelect_Attributes, 'icons/SelectAttributes.png', 'Select Attributes', 1)
        self.setWidgetParameters(self.owData_Sampler, 'icons/DataSampler.png', 'Data Sampler', 1)
        self.setWidgetParameters(self.owNaive_Bayes, 'icons/NaiveBayes.png', 'Naive Bayes', 1)
        self.setWidgetParameters(self.owk_Nearest_Neighbours, 'icons/kNearestNeighbours.png', 'k Nearest Neighbours', 1)
        self.setWidgetParameters(self.owClassification_Tree, 'icons/ClassificationTree.png', 'Classification Tree', 1)
        self.setWidgetParameters(self.owTest_Learners, 'icons/TestLearners.png', 'Test Learners', 1)
        self.setWidgetParameters(self.owROC_Analysis, 'ROCAnalysis.png', 'ROC Analysis', 1)
        self.setWidgetParameters(self.owLift_Curve, 'LiftCurve.png', 'Lift Curve', 1)
        self.setWidgetParameters(self.owCalibration_Plot, 'CalibrationPlot.png', 'Calibration Plot', 1)
        self.setWidgetParameters(self.owConfusion_Matrix, 'ConfusionMatrix.png', 'Confusion Matrix', 1)
        
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
        self.signalManager.addLink( self.owFile, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owNaive_Bayes, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owTest_Learners, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owk_Nearest_Neighbours, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owClassification_Tree, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owROC_Analysis, 'Evaluation Results', 'Evaluation Results', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owLift_Curve, 'Evaluation Results', 'Evaluation Results', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owCalibration_Plot, 'Evaluation Results', 'Evaluation Results', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owConfusion_Matrix, 'Evaluation Results', 'Evaluation Results', 1)
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
            file = open("Evaluate2.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"]); self.owSelect_Attributes.activateLoadedSettings()
            self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"]); self.owData_Sampler.activateLoadedSettings()
            self.owNaive_Bayes.loadSettingsStr(strSettings["Naive Bayes"]); self.owNaive_Bayes.activateLoadedSettings()
            self.owk_Nearest_Neighbours.loadSettingsStr(strSettings["k Nearest Neighbours"]); self.owk_Nearest_Neighbours.activateLoadedSettings()
            self.owClassification_Tree.loadSettingsStr(strSettings["Classification Tree"]); self.owClassification_Tree.activateLoadedSettings()
            self.owTest_Learners.loadSettingsStr(strSettings["Test Learners"]); self.owTest_Learners.activateLoadedSettings()
            self.owROC_Analysis.loadSettingsStr(strSettings["ROC Analysis"]); self.owROC_Analysis.activateLoadedSettings()
            self.owLift_Curve.loadSettingsStr(strSettings["Lift Curve"]); self.owLift_Curve.activateLoadedSettings()
            self.owCalibration_Plot.loadSettingsStr(strSettings["Calibration Plot"]); self.owCalibration_Plot.activateLoadedSettings()
            self.owConfusion_Matrix.loadSettingsStr(strSettings["Confusion Matrix"]); self.owConfusion_Matrix.activateLoadedSettings()
            
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
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Naive Bayes"] = self.owNaive_Bayes.saveSettingsStr()
        strSettings["k Nearest Neighbours"] = self.owk_Nearest_Neighbours.saveSettingsStr()
        strSettings["Classification Tree"] = self.owClassification_Tree.saveSettingsStr()
        strSettings["Test Learners"] = self.owTest_Learners.saveSettingsStr()
        strSettings["ROC Analysis"] = self.owROC_Analysis.saveSettingsStr()
        strSettings["Lift Curve"] = self.owLift_Curve.saveSettingsStr()
        strSettings["Calibration Plot"] = self.owCalibration_Plot.saveSettingsStr()
        strSettings["Confusion Matrix"] = self.owConfusion_Matrix.saveSettingsStr()
        
        file = open("Evaluate2.sav", "w")
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
        