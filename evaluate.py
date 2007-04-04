# contact: tomaz.curk@fri.uni-lj.si blaz.zupan@fri.uni-lj.si

import sys, os, cPickle, orange, orngSignalManager, orngRegistry
DEBUG_MODE = 0   #set to 1 to output debugging info to file 'signalManagerOutput.txt'
orngRegistry.addWidgetDirectories()
from OWFile import *
from OWDataDomain import *
from OWDataSampler import *
from OWNaiveBayes import *
from OWLogisticRegression import *
from OWMajority import *
from OWKNN import *
from OWClassificationTree import *
from OWC45Tree import *
from OWSVM import *
from OWCN2 import *
from OWTestLearners import *
from OWROC import *
from OWLiftCurve import *
from OWResultTable import *


class GUIApplication(QVBox):
    def __init__(self,parent=None, debugMode = DEBUG_MODE, debugFileName = "signalManagerOutput.txt", verbosity = 1):
        QVBox.__init__(self,parent)
        self.setCaption("Qt evaluate")
        self.signalManager = orngSignalManager.SignalManager(debugMode, debugFileName, verbosity)
        self.verbosity = verbosity

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owNaive_Bayes = OWNaiveBayes(signalManager = self.signalManager)
        self.owLogistic_Regression = OWLogisticRegression(signalManager = self.signalManager)
        self.owMajority = OWMajority(signalManager = self.signalManager)
        self.owk_Nearest_Neighbours = OWKNN(signalManager = self.signalManager)
        self.owClassification_Tree = OWClassificationTree(signalManager = self.signalManager)
        self.owC4.5 = OWC45Tree(signalManager = self.signalManager)
        self.owSVM = OWSVM(signalManager = self.signalManager)
        self.owCN2 = OWCN2(signalManager = self.signalManager)
        self.owTest_Learners = OWTestLearners(signalManager = self.signalManager)
        self.owROC_Analysis = OWROC(signalManager = self.signalManager)
        self.owLift_Curve = OWLiftCurve(signalManager = self.signalManager)
        self.owResult_Table = OWResultTable(signalManager = self.signalManager)
        
        # create instances of hidden widgets

        #set event and progress handler
        self.owFile.setEventHandler(self.eventHandler)
        self.owFile.setProgressBarHandler(self.progressHandler)
        self.owSelect_Attributes.setEventHandler(self.eventHandler)
        self.owSelect_Attributes.setProgressBarHandler(self.progressHandler)
        self.owData_Sampler.setEventHandler(self.eventHandler)
        self.owData_Sampler.setProgressBarHandler(self.progressHandler)
        self.owNaive_Bayes.setEventHandler(self.eventHandler)
        self.owNaive_Bayes.setProgressBarHandler(self.progressHandler)
        self.owLogistic_Regression.setEventHandler(self.eventHandler)
        self.owLogistic_Regression.setProgressBarHandler(self.progressHandler)
        self.owMajority.setEventHandler(self.eventHandler)
        self.owMajority.setProgressBarHandler(self.progressHandler)
        self.owk_Nearest_Neighbours.setEventHandler(self.eventHandler)
        self.owk_Nearest_Neighbours.setProgressBarHandler(self.progressHandler)
        self.owClassification_Tree.setEventHandler(self.eventHandler)
        self.owClassification_Tree.setProgressBarHandler(self.progressHandler)
        self.owC4.5.setEventHandler(self.eventHandler)
        self.owC4.5.setProgressBarHandler(self.progressHandler)
        self.owSVM.setEventHandler(self.eventHandler)
        self.owSVM.setProgressBarHandler(self.progressHandler)
        self.owCN2.setEventHandler(self.eventHandler)
        self.owCN2.setProgressBarHandler(self.progressHandler)
        self.owTest_Learners.setEventHandler(self.eventHandler)
        self.owTest_Learners.setProgressBarHandler(self.progressHandler)
        self.owROC_Analysis.setEventHandler(self.eventHandler)
        self.owROC_Analysis.setProgressBarHandler(self.progressHandler)
        self.owLift_Curve.setEventHandler(self.eventHandler)
        self.owLift_Curve.setProgressBarHandler(self.progressHandler)
        self.owResult_Table.setEventHandler(self.eventHandler)
        self.owResult_Table.setProgressBarHandler(self.progressHandler)
        

        #list of widget instances
        self.widgets = [self.owFile, self.owSelect_Attributes, self.owData_Sampler, self.owNaive_Bayes, self.owLogistic_Regression, self.owMajority, self.owk_Nearest_Neighbours, self.owClassification_Tree, self.owC4.5, self.owSVM, self.owCN2, self.owTest_Learners, self.owROC_Analysis, self.owLift_Curve, self.owResult_Table, ]
        # set widget captions
        self.owFile.setCaptionTitle('Qt File')
        self.owSelect_Attributes.setCaptionTitle('Qt Select Attributes')
        self.owData_Sampler.setCaptionTitle('Qt Data Sampler')
        self.owNaive_Bayes.setCaptionTitle('Qt Naive Bayes')
        self.owLogistic_Regression.setCaptionTitle('Qt Logistic Regression')
        self.owMajority.setCaptionTitle('Qt Majority')
        self.owk_Nearest_Neighbours.setCaptionTitle('Qt k Nearest Neighbours')
        self.owClassification_Tree.setCaptionTitle('Qt Classification Tree')
        self.owC4.5.setCaptionTitle('Qt C4.5')
        self.owSVM.setCaptionTitle('Qt SVM')
        self.owCN2.setCaptionTitle('Qt CN2')
        self.owTest_Learners.setCaptionTitle('Qt Test Learners')
        self.owROC_Analysis.setCaptionTitle('Qt ROC Analysis')
        self.owLift_Curve.setCaptionTitle('Qt Lift Curve')
        self.owResult_Table.setCaptionTitle('Qt Result Table')
        
        # set icons
        self.owFile.setWidgetIcon('icons/File.png')
        self.owSelect_Attributes.setWidgetIcon('icons/SelectAttributes.png')
        self.owData_Sampler.setWidgetIcon('icons/DataSampler.png')
        self.owNaive_Bayes.setWidgetIcon('icons/NaiveBayes.png')
        self.owLogistic_Regression.setWidgetIcon('icons/LogisticRegression.png')
        self.owMajority.setWidgetIcon('icons/Majority.png')
        self.owk_Nearest_Neighbours.setWidgetIcon('icons/kNearestNeighbours.png')
        self.owClassification_Tree.setWidgetIcon('icons/ClassificationTree.png')
        self.owC4.5.setWidgetIcon('icons/C45.png')
        self.owSVM.setWidgetIcon('icons/BasicSVM.png')
        self.owCN2.setWidgetIcon('CN2.png')
        self.owTest_Learners.setWidgetIcon('icons/TestLearners.png')
        self.owROC_Analysis.setWidgetIcon('ROCAnalysis.png')
        self.owLift_Curve.setWidgetIcon('LiftCurve.png')
        self.owResult_Table.setWidgetIcon('icons/DataTable.png')
        
        self.signalManager.addWidget(self.owFile)
        self.signalManager.addWidget(self.owSelect_Attributes)
        self.signalManager.addWidget(self.owData_Sampler)
        self.signalManager.addWidget(self.owNaive_Bayes)
        self.signalManager.addWidget(self.owLogistic_Regression)
        self.signalManager.addWidget(self.owMajority)
        self.signalManager.addWidget(self.owk_Nearest_Neighbours)
        self.signalManager.addWidget(self.owClassification_Tree)
        self.signalManager.addWidget(self.owC4.5)
        self.signalManager.addWidget(self.owSVM)
        self.signalManager.addWidget(self.owCN2)
        self.signalManager.addWidget(self.owTest_Learners)
        self.signalManager.addWidget(self.owROC_Analysis)
        self.signalManager.addWidget(self.owLift_Curve)
        self.signalManager.addWidget(self.owResult_Table)
        
        # create widget buttons
        owButtonFile = QPushButton("File", self)
        owButtonSelect_Attributes = QPushButton("Select Attributes", self)
        owButtonData_Sampler = QPushButton("Data Sampler", self)
        owButtonNaive_Bayes = QPushButton("Naive Bayes", self)
        owButtonLogistic_Regression = QPushButton("Logistic Regression", self)
        owButtonMajority = QPushButton("Majority", self)
        owButtonk_Nearest_Neighbours = QPushButton("k Nearest Neighbours", self)
        owButtonClassification_Tree = QPushButton("Classification Tree", self)
        owButtonC4.5 = QPushButton("C4.5", self)
        owButtonSVM = QPushButton("SVM", self)
        owButtonCN2 = QPushButton("CN2", self)
        owButtonTest_Learners = QPushButton("Test Learners", self)
        owButtonROC_Analysis = QPushButton("ROC Analysis", self)
        owButtonLift_Curve = QPushButton("Lift Curve", self)
        owButtonResult_Table = QPushButton("Result Table", self)
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
        self.connect(owButtonNaive_Bayes ,SIGNAL("clicked()"), self.owNaive_Bayes.reshow)
        self.connect(owButtonLogistic_Regression ,SIGNAL("clicked()"), self.owLogistic_Regression.reshow)
        self.connect(owButtonMajority ,SIGNAL("clicked()"), self.owMajority.reshow)
        self.connect(owButtonk_Nearest_Neighbours ,SIGNAL("clicked()"), self.owk_Nearest_Neighbours.reshow)
        self.connect(owButtonClassification_Tree ,SIGNAL("clicked()"), self.owClassification_Tree.reshow)
        self.connect(owButtonC4.5 ,SIGNAL("clicked()"), self.owC4.5.reshow)
        self.connect(owButtonSVM ,SIGNAL("clicked()"), self.owSVM.reshow)
        self.connect(owButtonCN2 ,SIGNAL("clicked()"), self.owCN2.reshow)
        self.connect(owButtonTest_Learners ,SIGNAL("clicked()"), self.owTest_Learners.reshow)
        self.connect(owButtonROC_Analysis ,SIGNAL("clicked()"), self.owROC_Analysis.reshow)
        self.connect(owButtonLift_Curve ,SIGNAL("clicked()"), self.owLift_Curve.reshow)
        self.connect(owButtonResult_Table ,SIGNAL("clicked()"), self.owResult_Table.reshow)
        
        #load settings before we connect widgets
        self.loadSettings()

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.owFile, self.owSelect_Attributes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owSelect_Attributes, self.owData_Sampler, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owNaive_Bayes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owLogistic_Regression, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owMajority, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owk_Nearest_Neighbours, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owClassification_Tree, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owC4.5, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owCN2, 'Examples', 'Example Table', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owSVM, 'Examples', 'Example Table', 1)
        self.signalManager.addLink( self.owNaive_Bayes, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owLogistic_Regression, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owMajority, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owTest_Learners, 'Examples', 'Data', 1)
        self.signalManager.addLink( self.owSVM, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owk_Nearest_Neighbours, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owClassification_Tree, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owC4.5, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owCN2, self.owTest_Learners, 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owROC_Analysis, 'Evaluation Results', 'Evaluation Results', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owLift_Curve, 'Evaluation Results', 'Evaluation Results', 1)
        self.signalManager.addLink( self.owTest_Learners, self.owResult_Table, 'Evaluation Results', 'Evaluation Results', 1)
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
            file = open("evaluate.sav", "r")
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
        self.owNaive_Bayes.loadSettingsStr(strSettings["Naive Bayes"])
        self.owNaive_Bayes.activateLoadedSettings()
        self.owLogistic_Regression.loadSettingsStr(strSettings["Logistic Regression"])
        self.owLogistic_Regression.activateLoadedSettings()
        self.owMajority.loadSettingsStr(strSettings["Majority"])
        self.owMajority.activateLoadedSettings()
        self.owk_Nearest_Neighbours.loadSettingsStr(strSettings["k Nearest Neighbours"])
        self.owk_Nearest_Neighbours.activateLoadedSettings()
        self.owClassification_Tree.loadSettingsStr(strSettings["Classification Tree"])
        self.owClassification_Tree.activateLoadedSettings()
        self.owC4.5.loadSettingsStr(strSettings["C4.5"])
        self.owC4.5.activateLoadedSettings()
        self.owSVM.loadSettingsStr(strSettings["SVM"])
        self.owSVM.activateLoadedSettings()
        self.owCN2.loadSettingsStr(strSettings["CN2"])
        self.owCN2.activateLoadedSettings()
        self.owTest_Learners.loadSettingsStr(strSettings["Test Learners"])
        self.owTest_Learners.activateLoadedSettings()
        self.owROC_Analysis.loadSettingsStr(strSettings["ROC Analysis"])
        self.owROC_Analysis.activateLoadedSettings()
        self.owLift_Curve.loadSettingsStr(strSettings["Lift Curve"])
        self.owLift_Curve.activateLoadedSettings()
        self.owResult_Table.loadSettingsStr(strSettings["Result Table"])
        self.owResult_Table.activateLoadedSettings()
        

    def saveSettings(self):
        if DEBUG_MODE: return
        self.owResult_Table.synchronizeContexts()
        self.owLift_Curve.synchronizeContexts()
        self.owROC_Analysis.synchronizeContexts()
        self.owTest_Learners.synchronizeContexts()
        self.owCN2.synchronizeContexts()
        self.owSVM.synchronizeContexts()
        self.owC4.5.synchronizeContexts()
        self.owClassification_Tree.synchronizeContexts()
        self.owk_Nearest_Neighbours.synchronizeContexts()
        self.owMajority.synchronizeContexts()
        self.owLogistic_Regression.synchronizeContexts()
        self.owNaive_Bayes.synchronizeContexts()
        self.owData_Sampler.synchronizeContexts()
        self.owSelect_Attributes.synchronizeContexts()
        self.owFile.synchronizeContexts()
        
        strSettings = {}
        strSettings["File"] = self.owFile.saveSettingsStr()
        strSettings["Select Attributes"] = self.owSelect_Attributes.saveSettingsStr()
        strSettings["Data Sampler"] = self.owData_Sampler.saveSettingsStr()
        strSettings["Naive Bayes"] = self.owNaive_Bayes.saveSettingsStr()
        strSettings["Logistic Regression"] = self.owLogistic_Regression.saveSettingsStr()
        strSettings["Majority"] = self.owMajority.saveSettingsStr()
        strSettings["k Nearest Neighbours"] = self.owk_Nearest_Neighbours.saveSettingsStr()
        strSettings["Classification Tree"] = self.owClassification_Tree.saveSettingsStr()
        strSettings["C4.5"] = self.owC4.5.saveSettingsStr()
        strSettings["SVM"] = self.owSVM.saveSettingsStr()
        strSettings["CN2"] = self.owCN2.saveSettingsStr()
        strSettings["Test Learners"] = self.owTest_Learners.saveSettingsStr()
        strSettings["ROC Analysis"] = self.owROC_Analysis.saveSettingsStr()
        strSettings["Lift Curve"] = self.owLift_Curve.saveSettingsStr()
        strSettings["Result Table"] = self.owResult_Table.saveSettingsStr()
        
        file = open("evaluate.sav", "w")
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
