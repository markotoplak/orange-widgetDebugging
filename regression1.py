#This file is automatically created by Orange Canvas and containing an Orange schema

import orngEnviron
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI
from OWBaseWidget import *

class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'regression1', signalManager = self.signalManager)
        self.widgets = {}
        self.loadSettings()
        
        self.setLayout(QVBoxLayout())
        self.box = OWGUI.widgetBox(self, 'Widgets')

        self.createWidget('OWFile', 'icons/File.png', 'File', 1, self.signalManager)
        self.createWidget('OWDataDomain', 'icons/SelectAttributes.png', 'Select Attributes', 1, self.signalManager)
        self.createWidget('OWDataSampler', 'icons/DataSampler.png', 'Data Sampler', 1, self.signalManager)
        self.createWidget('OWRegressionTree', 'RegressionTree.png', 'Regression Tree', 1, self.signalManager)
        self.createWidget('OWTestLearners', 'icons/TestLearners.png', 'Test Learners', 1, self.signalManager)
        self.createWidget('OWRegressionTreeViewer2D', 'icons/RegressionTreeGraph.png', 'Regression Tree Graph', 1, self.signalManager)
        self.createWidget('OWPredictions', 'icons/Predictions.png', 'Predictions', 1, self.signalManager)
        self.createWidget('OWPade', 'icons/Pade.png', 'Pade', 1, self.signalManager)
        
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
        self.signalManager.addLink( self.widgets['Regression Tree'], self.widgets['Test Learners'], 'Learner', 'Learner', 1)
        self.signalManager.addLink( self.widgets['Regression Tree'], self.widgets['Regression Tree Graph'], 'Regression Tree', 'Classification Tree', 1)
        self.signalManager.addLink( self.widgets['Regression Tree'], self.widgets['Predictions'], 'Regressor', 'Predictors', 1)
        self.signalManager.addLink( self.widgets['Data Sampler'], self.widgets['Regression Tree'], 'Sample', 'Example Table', 1)
        self.signalManager.addLink( self.widgets['File'], self.widgets['Select Attributes'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Select Attributes'], self.widgets['Data Sampler'], 'Examples', 'Data', 1)
        self.signalManager.addLink( self.widgets['Select Attributes'], self.widgets['Predictions'], 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.widgets['Select Attributes'], self.widgets['Test Learners'], 'Examples', 'Data', 1)
        self.signalManager.addLink( self.widgets['Select Attributes'], self.widgets['Pade'], 'Examples', 'Examples', 1)
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
            file = open("regression1.sav", "r")
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
        file = open("regression1.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()

if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        