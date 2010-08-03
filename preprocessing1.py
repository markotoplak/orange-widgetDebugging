#This file is automatically created by Orange Canvas and containing an Orange schema
#ignore:breastcancer2004.tab
import orngEnviron
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI
from OWBaseWidget import *

class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'preprocessing1', signalManager = self.signalManager)
        self.widgets = {}
        self.loadSettings()
        
        self.setLayout(QVBoxLayout())
        self.box = OWGUI.widgetBox(self, 'Widgets')

        self.createWidget('OWFile', 'icons/File.png', 'File', 1, self.signalManager)
        self.createWidget('OWPreprocess', 'icons/Preprocess.png', 'Preprocess', 1, self.signalManager)
        self.createWidget('OWNaiveBayes', 'icons/NaiveBayes.png', 'Naive Bayes', 1, self.signalManager)
        self.createWidget('OWLogisticRegression', 'icons/LogisticRegression.png', 'Logistic Regression', 1, self.signalManager)
        self.createWidget('OWMajority', 'icons/Majority.png', 'Majority', 1, self.signalManager)
        self.createWidget('OWKNN', 'icons/kNearestNeighbours.png', 'k Nearest Neighbours', 1, self.signalManager)
        self.createWidget('OWClassificationTree', 'icons/ClassificationTree.png', 'Classification Tree', 1, self.signalManager)
        self.createWidget('OWSVM', 'icons/BasicSVM.png', 'SVM', 1, self.signalManager)
        self.createWidget('OWCN2', 'icons/CN2.png', 'CN2', 1, self.signalManager)
        self.createWidget('OWRandomForest', 'icons/RandomForest.png', 'Random Forest', 1, self.signalManager)
        self.createWidget('OWTestLearners', 'icons/TestLearners.png', 'Test Learners', 1, self.signalManager)
        
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

        # add widget signals
        self.signalManager.setFreeze(1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['Test Learners'], 'Examples', 'Data', 1)
        self.signalManager.addLink( self.widgets['Preprocess'], self.widgets['Naive Bayes'], 'Preprocessing', 'Preprocessing', 1)
        self.signalManager.addLink( self.widgets['Preprocess'], self.widgets['Logistic Regression'], 'Preprocessing', 'Preprocessing', 1)
        self.signalManager.addLink( self.widgets['Preprocess'], self.widgets['Majority'], 'Preprocessing', 'Preprocessing', 1)
        self.signalManager.addLink( self.widgets['Preprocess'], self.widgets['k Nearest Neighbours'], 'Preprocessing', 'Preprocessing', 1)
        self.signalManager.addLink( self.widgets['Preprocess'], self.widgets['Classification Tree'], 'Preprocessing', 'Preprocessing', 1)
        self.signalManager.addLink( self.widgets['Preprocess'], self.widgets['CN2'], 'Preprocessing', 'Preprocessing', 1)
        self.signalManager.addLink( self.widgets['Preprocess'], self.widgets['SVM'], 'Preprocessing', 'Preprocessing', 1)
        self.signalManager.addLink( self.widgets['Preprocess'], self.widgets['Random Forest'], 'Preprocessing', 'Preprocessing', 1)
        self.signalManager.addLink( self.widgets['Naive Bayes'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.widgets['Majority'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.widgets['Logistic Regression'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.widgets['k Nearest Neighbours'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.widgets['Classification Tree'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.widgets['CN2'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.widgets['SVM'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.widgets['Random Forest'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.setFreeze(0)
        

    def createWidget(self, fname, iconName, caption, shown, signalManager):
        widgetSettings = cPickle.loads(self.strSettings[caption])
        m = __import__(fname)
        widget = m.__dict__[fname].__new__(m.__dict__[fname], _settingsFromSchema = widgetSettings)
        widget.__init__(signalManager=signalManager)
        widget.setEventHandler(self.eventHandler)
        widget.setProgressBarHandler(self.progressHandler)
        widget.setWidgetIcon(iconName)
        widget.setWindowTitle(caption)
        self.signalManager.addWidget(widget)
        self.widgets[caption] = widget
        if shown: OWGUI.button(self.box, self, caption, callback = widget.reshow)
        for dlg in getattr(widget, "wdChildDialogs", []):
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
            file = open("preprocessing1.sav", "r")
            self.strSettings = cPickle.load(file)
            file.close()

        except:
            print "unable to load settings"
            pass

    def closeEvent(self, ev):
        OWBaseWidget.closeEvent(self, ev)
        if orngDebugging.orngDebuggingEnabled: return
        strSettings = {}
        for (name, widget) in self.widgets.items():
            widget.synchronizeContexts()
            strSettings[name] = widget.saveSettingsStr()
            widget.close()
        file = open("preprocessing1.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()

if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        