#This is automatically created file containing an Orange schema
        
import orngOrangeFoldersQt4
import orngDebugging
import sys, os, cPickle, orange, orngSignalManager, OWGUI

from OWFile import *
from OWDataDomain import *
from OWDataSampler import *
from OWNaiveBayes import *
from OWLogisticRegression import *
from OWNomogram import *
from OWNomogram import *
from OWCN2 import *
from OWCN2RulesViewer import *



class GUIApplication(OWBaseWidget):
    def __init__(self,parent=None):
        self.signalManager = orngSignalManager.SignalManager()
        OWBaseWidget.__init__(self, title = 'classify2', signalManager = self.signalManager)
        self.widgets = []
        
        self.setLayout(QVBoxLayout())
        self.box = OWGUI.widgetBox(self, 'Widgets')

        # create widget instances
        self.owFile = OWFile(signalManager = self.signalManager)
        self.owSelect_Attributes = OWDataDomain(signalManager = self.signalManager)
        self.owData_Sampler = OWDataSampler(signalManager = self.signalManager)
        self.owNaive_Bayes = OWNaiveBayes(signalManager = self.signalManager)
        self.owLogistic_Regression = OWLogisticRegression(signalManager = self.signalManager)
        self.owNomogram = OWNomogram(signalManager = self.signalManager)
        self.owNomogram_2 = OWNomogram(signalManager = self.signalManager)
        self.owCN2 = OWCN2(signalManager = self.signalManager)
        self.owCN2_Rules_Viewer = OWCN2RulesViewer(signalManager = self.signalManager)
        
        self.setWidgetParameters(self.owFile, 'icons/File.png', 'File', 1)
        self.setWidgetParameters(self.owSelect_Attributes, 'icons/SelectAttributes.png', 'Select Attributes', 1)
        self.setWidgetParameters(self.owData_Sampler, 'icons/DataSampler.png', 'Data Sampler', 1)
        self.setWidgetParameters(self.owNaive_Bayes, 'icons/NaiveBayes.png', 'Naive Bayes', 1)
        self.setWidgetParameters(self.owLogistic_Regression, 'icons/LogisticRegression.png', 'Logistic Regression', 1)
        self.setWidgetParameters(self.owNomogram, 'icons/Nomogram.png', 'Nomogram', 1)
        self.setWidgetParameters(self.owNomogram_2, 'icons/Nomogram.png', 'Nomogram (2)', 1)
        self.setWidgetParameters(self.owCN2, 'CN2.png', 'CN2', 1)
        self.setWidgetParameters(self.owCN2_Rules_Viewer, 'CN2RulesViewer.png', 'CN2 Rules Viewer', 1)
        
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
        self.signalManager.addLink( self.owLogistic_Regression, self.owNomogram, 'Classifier', 'Classifier', 1)
        self.signalManager.addLink( self.owNaive_Bayes, self.owNomogram_2, 'Naive Bayesian Classifier', 'Classifier', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owNaive_Bayes, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owLogistic_Regression, 'Examples', 'Examples', 1)
        self.signalManager.addLink( self.owCN2, self.owCN2_Rules_Viewer, 'Unordered CN2 Classifier', 'Rule Classifier', 1)
        self.signalManager.addLink( self.owData_Sampler, self.owCN2, 'Examples', 'Example Table', 1)
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
            file = open("classify2.sav", "r")
            strSettings = cPickle.load(file)
            file.close()

            self.owFile.loadSettingsStr(strSettings["File"]); self.owFile.activateLoadedSettings()
            self.owSelect_Attributes.loadSettingsStr(strSettings["Select Attributes"]); self.owSelect_Attributes.activateLoadedSettings()
            self.owData_Sampler.loadSettingsStr(strSettings["Data Sampler"]); self.owData_Sampler.activateLoadedSettings()
            self.owNaive_Bayes.loadSettingsStr(strSettings["Naive Bayes"]); self.owNaive_Bayes.activateLoadedSettings()
            self.owLogistic_Regression.loadSettingsStr(strSettings["Logistic Regression"]); self.owLogistic_Regression.activateLoadedSettings()
            self.owNomogram.loadSettingsStr(strSettings["Nomogram"]); self.owNomogram.activateLoadedSettings()
            self.owNomogram_2.loadSettingsStr(strSettings["Nomogram (2)"]); self.owNomogram_2.activateLoadedSettings()
            self.owCN2.loadSettingsStr(strSettings["CN2"]); self.owCN2.activateLoadedSettings()
            self.owCN2_Rules_Viewer.loadSettingsStr(strSettings["CN2 Rules Viewer"]); self.owCN2_Rules_Viewer.activateLoadedSettings()
            
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
        strSettings["Naive Bayes"] = self.owNaive_Bayes.saveSettingsStr()
        strSettings["Logistic Regression"] = self.owLogistic_Regression.saveSettingsStr()
        strSettings["Nomogram"] = self.owNomogram.saveSettingsStr()
        strSettings["Nomogram (2)"] = self.owNomogram_2.saveSettingsStr()
        strSettings["CN2"] = self.owCN2.saveSettingsStr()
        strSettings["CN2 Rules Viewer"] = self.owCN2_Rules_Viewer.saveSettingsStr()
        
        file = open("classify2.sav", "w")
        cPickle.dump(strSettings, file)
        file.close()
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    ow = GUIApplication()
    ow.show()
    # comment the next line if in debugging mode and are interested only in output text in 'signalManagerOutput.txt' file
    application.exec_()
        